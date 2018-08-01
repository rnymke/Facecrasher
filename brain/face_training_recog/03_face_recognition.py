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
import urllib.request
import socket               

# Create socket shit
s = socket.socket()        
host = '192.168.1.101'
port = 8003
s.connect((host, port))

recognizer = cv2.face.LBPHFaceRecognizer_create()
trainerPath = "../../resources/models/haar_frontal/trainer.yml"
recognizer.read(trainerPath)
cascadePath = "../../resources/models/haar_frontal/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

# Open stream
stream = urllib.request.urlopen('http://192.168.1.101:8000/stream.mjpg')

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

# Define min window size to be recognized as a face
minW = 0.05*videoFrameWidth
minH = 0.05*videoFrameHeight


bytes = b''
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
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
                    s.send(b'3')
                    #ser.flushInput()
                    #ser.write(('3').encode())
                elif ((videoFrameWidthMiddle - xFaceMiddle) < ((-1)*faceHyst)):
                    print("Face is to the right, move to the left")
                    s.send(b'4')
                    #ser.flushInput()
                    #ser.write(('4').encode())             
                elif ((videoFrameHeight - h) < (round(videoFrameHeight/1.5))):
                    print("Too close, move back")
                    s.send(b'1')
                    #ser.flushInput()
                    #ser.write(('1').encode())
                elif ((videoFrameHeight - h) > (round(videoFrameHeight/1.2))):
                    print("Too far, move closer")
                    s.send(b'2')
                    #ser.flushInput()
                    #ser.write(('2').encode())
            
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
s.close()
