# Whole ML project here

import socket
import serial
import io
import picamera
import logging
import socketserver
import threading
from threading import Condition
from http import server
from stream_to_web import start_streaming
from server import start_server

class cameraThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
       start_streaming()

class commandThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
       start_server(8003)


thread_camera = cameraThread(1, "Camera", 1)
thread_commands = commandThread(2, "Commands", 2)

thread_camera.start()
thread_commands.start()
