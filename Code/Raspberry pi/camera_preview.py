from picamera2 import Picamera2, Preview
import time


# Create a PiCamera object
picam2 = Picamera2()
#  Create a new object, camera_config and use it to set the still image resolution (main) to 1920 x 1080. and a lowres image with a size of 640 x 480. This lowres image is used as the preview image when framing a shot.
camera_config = picam2.create_still_configuration(main={"size": (1920 , 1080)}, lores={"size": (320 , 180)}, display="lores")
#Load the configuration.
picam2.configure(camera_config)
#Start the preview window and then start the camera.
picam2.start_preview(Preview.QTGL)
picam2.start()
# pause for 2 seconds
time.sleep(2)

im = picam2.capture_array()

im.dtype

#picam2.stop()
#picam2.stop_preview()


