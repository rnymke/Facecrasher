import socket
import serial

def start_server(port = 8002):
    s = socket.socket()
    host = '192.168.1.101' 
    print(host)
    s.bind((host, port))
    ser = serial.Serial('/dev/ttyACM0', 4800)
    s.listen(9999)
    while True:
        c, addr = s.accept()
        print ('Got connection from',addr)
        while True:
            rec = c.recv(1024)
            if not rec:
                break
            ser.flushInput()
            ser.write(rec)
            print(rec.decode())
        c.close()


if __name__ == '__main__':
    start_server()
