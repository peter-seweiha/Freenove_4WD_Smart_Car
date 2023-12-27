from picamera2 import Picamera2, Preview
import time

# import Servo modules
from PCA9685 import PCA9685

# for face detection and motion
import math
import cv2




# Create a PiCamera object
picam2 = Picamera2()
#picam2.start_and_capture_file("image.jpg")

#  Create a new object, camera_config and use it to set the still image resolution (main) to 1920 x 1080. and a lowres image with a size of 640 x 480. This lowres image is used as the preview image when framing a shot.
camera_config = picam2.create_still_configuration(main={"size": (320, 180)}, lores={"size": (320, 180)}, display="lores")

#Load the configuration.
picam2.configure(camera_config)

#Start the preview window and then start the camera.
picam2.start_preview(Preview.QTGL)
picam2.start()

# pause for 2 seconds
time.sleep(2)


# take an image __________________________
# Explicitly open a new file called my_image.jpg
my_file = open('my_image.jpg', 'wb')

picam2.capture_file(my_file)
# At this point my_file.flush() has been called, but the file has
# not yet been closed
my_file.close()




# ___ code to detect & follow face___________________

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

# Read the image
image = cv2.imread(my_file)

# Convert the image to grayscale for better processing
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around the detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# use print to understand some functions:

print(len(faces))

print (x)
print (y)
print (w)
print (h)

#save image with frame
cv2.imwrite("output_image_with_faces.jpg", image)


## Calculate the motion
# get the x value for face centre (in pixels)
x_face = int(x+(w/2))

# get the x value for image centre (in pixels)
x_centre = 160 # since this is have the pixel value for the image

# Calculate the difference
x_diff = x_face - x_centre

#calculate the Sin value
sin_value = x_diff/226.27  # calculated value using a case with the angle = 45 degrees

# determine the angle the servo needs to move
angle_in_radians = math.asin(sin_value)
# Convert radians to degrees for the result
angle_in_degrees = math.degrees(angle_in_radians)

angle_in_degrees = int(angle_in_degrees)
print(f'angle to move {angle_in_degrees}')

## move the Servo
pwm.setServoPwm('0',(90 + angle_in_degrees))



time.sleep(5)
picam2.stop()
picam2.stop_preview()


