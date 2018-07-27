import os 
import cv2

vcap = cv2.VideoCapture('192.168.1.111:3000')

ret, img =vcap.read()

print(ret)
print(img)
#cv2.imshow('video',img) 
