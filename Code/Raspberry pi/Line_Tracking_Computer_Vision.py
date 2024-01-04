# I needed to slow this one down to compansate for the slowness of responding due to the extra data collection activities in the code

import time
from Motor import *
import RPi.GPIO as GPIO
from datetime import datetime
from picamera2 import Picamera2, Preview
import pandas as pd
from servo import Servo
import numpy as np
import json
import cv2
import tensorflow as tf

class Line_Tracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)

        # configure the camera
        self.picam2 = Picamera2()
        #  Create a new object, camera_config and use it to set the still image resolution (main) to 1920 x 1080. and a lowres image with a size of 640 x 480. This lowres image is used as the preview image when framing a shot.
        camera_config = self.picam2.create_still_configuration(main={"size": (162, 90)}, lores={"size": (162, 90)}, display="lores")
        #Load the configuration.
        self.picam2.configure(camera_config)
        self.picam2.start_preview(Preview.QTGL)
        self.picam2.start()
        # pause for 2 seconds
#         time.sleep(2)   

    def run(self):
        self.data = []
        i = 0
        while True:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            
            # capture time stamp
            timestamp = datetime.now()

            # Capture image
            im = self.picam2.capture_array()
            resized_image = cv2.resize(im, (54, 30))
            greyed_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            img_as_array = np.array(greyed_image, dtype=np.float32)/255
            # Reshape the array to match Tensorflow expectations
            img_as_array = img_as_array.reshape(1, 30, 54, 1)

            # Use CNN to predict the suitable driving action
            interpreter.set_tensor(input_details[0]['index'], img_as_array)
            interpreter.invoke()
            model_prediction = interpreter.get_tensor(output_details[0]['index'])
            self.model_prediction = np.argmax(model_prediction)

            if self.model_prediction==0:
                PWM.setMotorModel(500,500,500,500)
                motion = 'SlowForward'
            elif self.model_prediction==1:
                PWM.setMotorModel(-1000,-1000,1750,1750)
                motion = 'SoftLeft'
            elif self.model_prediction==6: # doesn't exist for now
                PWM.setMotorModel(-1500,-1500,2500,2500)
                motion = 'HardLeft'
            elif self.model_prediction==2:
                PWM.setMotorModel(1750,1750,-1000,-1000)
                motion = 'SoftRight'
            elif self.model_prediction==3:
                PWM.setMotorModel(2500,2500,-1500,-1500)
                motion = 'HardRight'
            elif self.model_prediction==7: # doesn't exist for now
                #pass
                PWM.setMotorModel(0,0,0,0)
                motion = 'Stop'
            
            img_as_list = greyed_image.tolist()
            img_as_json = json.dumps(img_as_list)
            self.data.append({'motion': motion, 'timestamp': timestamp, 'i':i, 'LMR':self.LMR,'model_prediction': self.model_prediction ,'img': img_as_json })
            i = i+1


computer_vision=Line_Tracking()

# set the camera direction in the middle using servo
pwm=Servo()
pwm.setServoPwm('0',98) # I observed this is the value of the exact middle

# load the model file using TensorFlow lite
interpreter = tf.lite.Interpreter('computer_vision_driver_v2.tflite')
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()



# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        computer_vision.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)
        output = pd.DataFrame(computer_vision.data)
        timestamp_file = datetime.now().strftime("%Y-%m-%d %H_%M_%S.%f")
        output.to_csv(f'data_output{timestamp_file}.csv', index = False)
