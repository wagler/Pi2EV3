import cv2
import numpy as np
import time
import sys
from socket import socket, AF_INET, SOCK_DGRAM

SERVER_IP   = '192.168.137.145'
PORT_NUMBER = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket( AF_INET, SOCK_DGRAM )

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)


Motor = enum('A', 'B', 'C')
motorlocation = ['cd /sys/class/tacho-motor/tacho-motor0;',
                 'cd /sys/class/tacho-motor/tacho-motor1;',
                 'cd /sys/class/tacho-motor/tacho-motor2;']

mySocket.sendto(motorlocation[0] + 'echo brake > stop_mode',(SERVER_IP,PORT_NUMBER))

def moveMotor(motor, speed):
    mySocket.sendto(motorlocation[motor] +
                                             'echo ' + str(-speed) +
                                             ' > duty_cycle_sp;' + 
                                             'echo 1 > run', (SERVER_IP,PORT_NUMBER))


cap = cv2.VideoCapture(1)

def getCommand(x, y):
    if y > 1:
        speedR = 0.1*(160-x) + 30
        speedL = 30 - 0.1*(160-x)
        print 'speedL: ' + str(speedL)
        print 'speedR: ' + str(speedR)
        moveMotor(Motor.A, speedL)
        moveMotor(Motor.B, speedR)

    else:
        moveMotor(Motor.A, 0)
        moveMotor(Motor.B, 0)

def moveBack():
    moveMotor(Motor.A, -30)
    moveMotor(Motor.B, -30)
    time.sleep(1.5)
    moveMotor(Motor.A, 0)
    moveMotor(Motor.B, 0)

def noBallFound():
    moveMotor(Motor.A, 30)
    time.sleep(1.5)
    moveMotor(Motor.A, 0)

def grab():
    moveMotor(Motor.A, 30)
    moveMotor(Motor.B, 30)
    time.sleep(3)
    moveMotor(Motor.A, 0)
    moveMotor(Motor.B, 0)
    moveMotor(Motor.C, 70)
    time.sleep(2)
    moveMotor(Motor.C, 0)

try:

    if cap.isOpened() == True:
        for i in xrange(10):
            ret, frame = cap.read()

        framesfound = 0
        while True:
            print 'new frame'
            ret,frame = cap.read()
            frame = cv2.resize(frame, (640, 480))
            cv2.imshow('frame', frame)
            #convert to gray
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #smooth it a bit
            blur = cv2.GaussianBlur(gray,(5,5),0)
            #convert to binary threshold 
            ret,th = cv2.threshold(blur,200,255,cv2.THRESH_BINARY)
            # find contours in the threshold image
            contours,hierarchy = cv2.findContours(th,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            # finding contour with maximum area and store it as best_cnt
            if contours is not None:
                best_cnt = []
                max_area = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area > max_area:
                        max_area = area
                        best_cnt = cnt
               
                # finding centroids of best_cnt and draw a circle there
                if len(best_cnt) != 0:
                    M = cv2.moments(best_cnt)
                    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                    getCommand(cx,cy)
                else:
                    moveMotor(Motor.A, 0)
                    moveMotor(Motor.B, 0)
            else:
                moveMotor(Motor.A, 0)
                moveMotor(Motor.B, 0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                

        moveMotor(Motor.A, 0)
        moveMotor(Motor.B, 0)
        moveMotor(Motor.C, 0)
        cap.release()
        cv2.destroyAllWindows()

    else:
        print 'Camera failed to initialize'
        cap.release()
        cv2.destroyAllWindows()

except Exception,e:
    print "Fatal Error Occured:"
    print str(e)
    cap.release()
