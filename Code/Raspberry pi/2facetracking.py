from picamera2 import Picamera2, Preview
import time

# import Servo modules
from PCA9685 import PCA9685

# for face detection and motion
import math
import cv2

# buzzer
from Buzzer import *
buzzer=Buzzer()

# the servo class
class Servo:
    def __init__(self):
        self.PwmServo = PCA9685(0x40, debug=True)
        self.PwmServo.setPWMFreq(50)
        self.PwmServo.setServoPulse(8,1500)
        self.PwmServo.setServoPulse(9,1500)
    def setServoPwm(self,channel,angle,error=10):
        angle=int(angle)
        if channel=='0':
            self.PwmServo.setServoPulse(8,2500-int((angle+error)/0.09))
        elif channel=='1':
            self.PwmServo.setServoPulse(9,500+int((angle+error)/0.09))
        elif channel=='2':
            self.PwmServo.setServoPulse(10,500+int((angle+error)/0.09))
        elif channel=='3':
            self.PwmServo.setServoPulse(11,500+int((angle+error)/0.09))
        elif channel=='4':
            self.PwmServo.setServoPulse(12,500+int((angle+error)/0.09))
        elif channel=='5':
            self.PwmServo.setServoPulse(13,500+int((angle+error)/0.09))
        elif channel=='6':
            self.PwmServo.setServoPulse(14,500+int((angle+error)/0.09))
        elif channel=='7':
            self.PwmServo.setServoPulse(15,500+int((angle+error)/0.09))

# create the servo object
pwm=Servo()


# Create a PiCamera object
picam2 = Picamera2()
#picam2.start_and_capture_file("image.jpg")

#  Create a new object, camera_config and use it to set the still image resolution (main) to 1920 x 1080. and a lowres image with a size of 640 x 480. This lowres image is used as the preview image when framing a shot.
camera_config = picam2.create_still_configuration(main={"size": (320, 180)}, lores={"size": (320, 180)}, display="lores")

#Load the configuration.
picam2.configure(camera_config)

#Start the preview window and then start the camera.
#picam2.start_preview(Preview.QTGL)
picam2.start()

# pause for 2 seconds
time.sleep(2)

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

servo_angle = 90

# indicate program start
buzzer.run('1')
time.sleep(0.2)
buzzer.run('0')

# ___ code to detect & follow face___________________

for i in range(100):
    time.sleep(0.1)

    faces_detected = 0
    while faces_detected <1 :
        # take an image
        picam2.capture_file(f"test.jpg")

        # Read the image in open cv
        image = cv2.imread('test.jpg')

        # Convert the image to grayscale for better processing
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        faces_detected = len(faces)
    # use print to understand some functions:

    print(f'faces detected: {len(faces)}')

    #save image with frame
    cv2.imwrite("output_image_with_faces.jpg", image)


    ## Calculate the motion
    # get the x value for face centre (in pixels)
    x_face = int(x+(w/2))

    # get the x value for image centre (in pixels)
    x_centre = 160 # since this is have the pixel value for the image

    print(f'X face centre: {x_face}')

    # Calculate the difference
    x_diff = x_face - x_centre

    #calculate the Sin value
    sin_value = x_diff/226.27  # calculated value using a case with the angle = 45 degrees

    # determine the angle the servo needs to move
    angle_in_radians = math.asin(sin_value)
    # Convert radians to degrees for the result
    angle_in_degrees = math.degrees(angle_in_radians)
    angle_in_degrees = int(angle_in_degrees)

    # calculate new servo angle based on previous angle and new difference
    servo_angle = servo_angle + angle_in_degrees
    
    print(f'angle to move {angle_in_degrees}')
    print(f'Servo Angle {servo_angle}')

    ## move the Servo
    pwm.setServoPwm('0',servo_angle)


picam2.stop()
picam2.stop_preview()
pwm.setServoPwm('0',90)
# indicate program end
buzzer.run('1')
time.sleep(0.1)
buzzer.run('0')
time.sleep(0.1)
buzzer.run('1')
time.sleep(0.1)
buzzer.run('0')

