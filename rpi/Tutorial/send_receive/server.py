import socket
import serial
s = socket.socket()
host = '192.168.1.101' 
print(host)
port = 8002
s.bind((host, port))
ser = serial.Serial('/dev/ttyACM0', 4800)
s.listen(5)
while True:
    c, addr = s.accept()
    print ('Got connection from',addr)
    rec = c.recv(1024)
    ser.flushInput()
    ser.write(rec)
    print(rec.decode())
    c.close()
