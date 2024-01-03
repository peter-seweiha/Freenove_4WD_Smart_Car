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
        camera_config = self.picam2.create_still_configuration(main={"size": (54, 30)}, lores={"size": (54, 30)}, display="lores")
        #Load the configuration.
        self.picam2.configure(camera_config)
        self.picam2.start()
        # pause for 2 seconds
        time.sleep(2)   

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
            timestamp = datetime.now().strftime("%Y-%m-%d %H_%M_%S.%f")

            # Capture image
            im = self.picam2.capture_array()
            greyed_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            img_as_list = greyed_image.tolist()
            img_as_array = np.array(img_as_list)

            # Use CNN to predict the suitable driving action
            model_prediction = model.predict(np.expand_dims(img_as_array/255, 0))
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
            
            img_as_json = json.dumps(img_as_list)
            self.data.append({'motion': motion, 'timestamp': timestamp, 'i':i, 'LMR':self.LMR, 'img': img_as_json })
            i = i+1


computer_vision=Line_Tracking()

# set the camera direction in the middle using servo
pwm=Servo()
pwm.setServoPwm('0',98) # I observed this is the value of the exact middle

# load the model file using TensorFlow lite



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
