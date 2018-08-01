import socket               

s = socket.socket()        
host = '192.168.1.101'
port = 8003
s.connect((host, port))

rng = 100
for i in range(0, rng):
#while True:
    s.send(b'3')
s.close()

