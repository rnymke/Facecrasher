# python 3
import cv2
import urllib.request
import numpy as np
import io

stream = urllib.request.urlopen('http://192.168.1.101:8000/stream.mjpg')
byte_array = b''

while True:
    byte_array += stream.read(1024)
    a = byte_array.find(b'\xff\xd8')
    b = byte_array.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = byte_array[a:b+2]
        byte_array = byte_array[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('i',i)
        if cv2.waitKey(1) == 27:
            exit(0)
