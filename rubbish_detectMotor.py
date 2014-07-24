import cv2
import paramiko
import time

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN


def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

Motor = enum('A', 'B', 'C')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(192.168.2.100,username='root',password='r00tme')

motorlocation = ['cd /sys/class/tacho-motor/tacho-motor0;'
                 'cd /sys/class/tacho-motor/tacho-motor1;'
                 'cd /sys/class/tacho-motor/tacho-motor2;']

stdin, stdout, stderr = ssh.exec_command(motorlocation[0] + 'echo brake > stop_mode')
stdin, stdout, stderr = ssh.exec_command(motorlocation[1] + 'echo brake > stop_mode')
stdin, stdout, stderr = ssh.exec_command(motorlocation[2] + 'echo brake > stop_mode')

def moveMotor(motor, speed):
    stdin, stdout, stderr = ssh.exec_command(motorlocation[motor] +
                                             'echo %d > duty_cycle_sp;' + 
                                             'echo 1 > run',
                                             speed)

def getCommand(x,y):
##    if x < 107:
##        #left
##        return "L"
##    elif x > 213:
##        #right
##        return "R"
##    elif (y > 80):
##        #grab
##        return "G"
##    else:
##        #forward
##        return "F"
    if y < 80:
        #ball not in grab position yet
        moveMotor(Motor.A, (0.5*(160-x)+20))
        moveMotor(Motor.B, (0.5*(160-x)-20))
    else:
        moveMotor(Motor.A, 0)
        moveMotor(Motor.B, 0)
        moveMotor(Motor.C, 100)
        time.sleep(1)
        

try:
    #make sure camera initialized
    if cap.isOpened() == True:
        #take 10 dummy images to adjust camera
        for i in xrange(10):
            ret, frame = cap.read()
        while True:
            ret, frame = cap.read()
            #if a frame was captured successfully
            #no else to match it because it will just skip to the next frame automatically
            if ret == True:
                frame = cv2.resize(frame, (320,240))
                frame = cv2.medianBlur(frame,5)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=200)

                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for i in circles[0,:]:
                        # draw the outer circle
                        cv2.circle(frame,(i[0],i[1]),i[2],(0,0,255),2)
                        # draw the center of the circle
                        cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
                        getCommand(i[0],i[1])
                        #coord = "x: "+str(i[0])+"y: "+str(i[1])
                        #cv2.putText(frame,coord,(10,30), font, 2,(0,0,255),2)
                        #cv2.putText(frame,command,(10,50), font, 2,(0,0,255),2)
                else:
                    #coord = "no circle found"
                    #cv2.putText(frame,coord,(10,30), font, 2,(0,0,255),2)
                    #return error if no balls seen
                    #cv2.putText(frame,command,(10,50), font, 2,(0,0,255),2)

            #out of ret test because it wont pass an error outside of it    
            #cv2.imshow('detected circles',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    else:
        print "Camera Failed To Initialize"
        cap.release()
        cv2.destroyAllWindows()

except Exception,e:
    print "Fatal Error Occured:"
    print str(e)
    cap.release()
    cv2.destroyAllWindows()
