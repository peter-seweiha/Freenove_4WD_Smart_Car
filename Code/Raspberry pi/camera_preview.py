from picamera2 import Picamera2, Preview
import time
import cv2
import pandas as pd
import json


# Create a PiCamera object
picam2 = Picamera2()
#  Create a new object, camera_config and use it to set the still image resolution (main) to 1920 x 1080. and a lowres image with a size of 640 x 480. This lowres image is used as the preview image when framing a shot.
camera_config = picam2.create_still_configuration(main={"size": (80 , 45)}, lores={"size": (80 , 45)}, display="lores")
#Load the configuration.
picam2.configure(camera_config)
#Start the preview window and then start the camera.
picam2.start_preview(Preview.QTGL)
picam2.start()
# pause for 2 seconds
time.sleep(2)

rows = []
for i in range(5):
    im = picam2.capture_array()
    greyed_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    img_as_json = json.dumps(greyed_image)
    rows.append({'i': i, 'img':img_as_json  })
    
output = pd.DataFrame(rows)
output.to_csv('output.csv', index= False)


picam2.stop()
picam2.stop_preview()


