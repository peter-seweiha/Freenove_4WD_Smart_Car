![Footer](images.jpeg)


# Building Machine Learning applications using Freenove Smart Car Kit
In this repository, I'll be ueing Raspberry pi, python, and the Freenove car kit to explore some machine learning applications.


### Projects 
1. **Face Tracking**: Raspberry pi, Freenove car, opencv
     
   *Moving the servo to track any face along the X axis*
   - [Code Folder](link)
  
3. **Machine Learning based Line Follower**: Rasperry pi, Freenove car, opencv, TensorFlow, TensorFlow lite
     
   *The Freenove car kit comes with a program to follow a black line using the infrared sensor at the front. In this experiment I'll be using the infrared to train a Machine learning model to follow the kine based on camera feed. Afterwards I'll work to enhance the model to follow the line faster than an infrared-based system can do*
    1. Mimic infrared  
       - Gather images and navigation data while infrared is driving the car
            - learning 1: Infrared program is slowed by the data collection I had to slow down all speeds
       - Build, train, and test a Neural Network to drive the car
           - How can we inform the CNN about the aequence of images which makes sense in this scenario - thinking of changing the value of one pixel to represent the sequence or 2 revolving pixels
       - Gather more data to teach the neural network any missing skills i.e. navigating sharp corners ..etc  

    2. Enhancements  
        - Learn how to speed up  
        - Learn how to finish the track faster than infrared in a competition  

    3. Reinforcement Learning  
        - Use RL to improve track performwnce and speed
   
     
     image
     


<br/><br/>

### Ideas to try:  
- explore capture array from picamera2: https://github.com/raspberrypi/picamera2/blob/main/examples/opencv_face_detect.py
- 

