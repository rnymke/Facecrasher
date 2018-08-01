''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import cv2
import numpy as np
import os
import serial

ser = serial.Serial('/dev/ttyACM0', 4800)

recognizer = cv2.face.LBPHFaceRecognizer_create()
trainerPath = "../../resources/models/haar_frontal/trainer.yml"
recognizer.read(trainerPath)
cascadePath = "../../resources/models/haar_frontal/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
#names = ['None', 'Dan', 'Robin', 'Usman']
names = ['None', 'Dan']

videoFrameWidth = 640
videoFrameHeight = 480
videoFrameWidthMiddle = round(videoFrameWidth/2)
videoFrameHeightMiddle = round(videoFrameHeight/2)
faceHyst = 80

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, videoFrameWidth) # set video widht
cam.set(4, videoFrameHeight) # set video height

#CV_CAP_PROP_CONVERT_RGB = 15
CV_CAP_PROP_WHITE_BALANCE_U = 16
cam.set(CV_CAP_PROP_WHITE_BALANCE_U, 100)

# Define min window size to be recognized as a face
minW = 0.05*cam.get(3)
minH = 0.05*cam.get(4)

POS_MSEC = 0
POS_FRAMES = 1
POS_AVI_RATIO = 2
FRAME_WIDTH = 3
FRAME_HEIGHT = 4
FPS = 5
FOURCC = 6
FRAME_COUNT = 7
FORMAT = 8
MODE = 9
BRIGHTNESS = 10
CONTRAST = 11 
SATURATION =  12
HUE = 13 
GAIN = 14
EXPOSURE = 15
CONVERT_RGB = 16
WHITE_BALANCE = 17
RECTIFICATION = 18

props = [['Height', cam.get(FRAME_HEIGHT)],
         ['Brightness', cam.get(BRIGHTNESS)],
         ['Exposure', cam.get(EXPOSURE)]]


while True:

    ret, img =cam.read()
    #img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,#1.2
        minNeighbors = 5,#5
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 90):
            id = names[id]
            #confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            #confidence = "  {0}%".format(round(100 - confidence))
            
        confidence = "  {0}".format(round(confidence))
        
        #print("x=",x,"y=",y,"w=",w,"h=",h)
        xFaceMiddle = (x + (round(w/2)))
        yFaceMiddle = (y + (round(h/2)))
        
        if (id == "Dan"):
            if ((videoFrameWidthMiddle - xFaceMiddle) > faceHyst):
                print("Face is to the left, move to the right")
                ser.flushInput()
                ser.write(('3').encode())
            elif ((videoFrameWidthMiddle - xFaceMiddle) < ((-1)*faceHyst)):
                print("Face is to the right, move to the left")
                ser.flushInput()
                ser.write(('4').encode())             
            elif ((videoFrameHeight - h) < (round(videoFrameHeight/1.5))):
                print("Too close, move back")
                ser.flushInput()
                ser.write(('1').encode())
            elif ((videoFrameHeight - h) > (round(videoFrameHeight/1.2))):
                print("Too far, move closer")
                ser.flushInput()
                ser.write(('2').encode())
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
