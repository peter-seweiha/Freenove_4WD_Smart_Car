import time
from Motor import *
import RPi.GPIO as GPIO
from datetime import datetime
from picamera2 import Picamera2, Preview
import pandas as pd

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
        camera_config = self.picam2.create_still_configuration(main={"size": (320, 180)}, lores={"size": (320, 180)}, display="lores")
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
            timestamp = datetime.now()
            self.picam2.capture_file(f"{i}-{timestamp}.jpg")
            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
                motion = 'SlowForward'
            elif self.LMR==4:
                PWM.setMotorModel(-1500,-1500,2500,2500)
                motion = 'SoftLeft'
            elif self.LMR==6:
                PWM.setMotorModel(-2000,-2000,4000,4000)
                motion = 'HardLeft'
            elif self.LMR==1:
                PWM.setMotorModel(2500,2500,-1500,-1500)
                motion = 'SoftRight'
            elif self.LMR==3:
                PWM.setMotorModel(4000,4000,-2000,-2000)
                motion = 'HardRight'
            elif self.LMR==7:
                #pass
                PWM.setMotorModel(0,0,0,0)
                motion = 'Stop'
            self.data.append({'motion': motion, 'timestamp': timestamp, 'i':i, 'LMR':self.LMR })
            i = i+1


infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)
        output = pd.DataFrame(infrared.data)
        output.to_csv('data_output.csv', index = False)
