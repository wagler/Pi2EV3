import cv2
import numpy as np

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

def getCommand(x,y):
    if x < 107:
        #left
        return "L"
    elif x > 213:
        #right
        return "R"
    elif (y > 80):
        #grab
        return "G"
    else:
        #forward
        return "F"

try:
    #make sure camera initialized
    if cap.isOpened() == True:
        #take 10 dummy images to adjust camera
        for i in xrange(10):
            ret, frame = cap.read()
        while True:
            ret, frame = cap.read()
            #if a frame was captured successfully 
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
                        command = getCommand(i[0],i[1])
                        coord = "x: "+str(i[0])+"y: "+str(i[1])
                        cv2.putText(frame,coord,(10,30), font, 2,(0,0,255),2)
                        cv2.putText(frame,command,(10,50), font, 2,(0,0,255),2)
                else:
                    coord = "no circle found"
                    cv2.putText(frame,coord,(10,30), font, 2,(0,0,255),2)
                    #keep turning if no balls seen
                    command = "R"
                    cv2.putText(frame,command,(10,50), font, 2,(0,0,255),2)
                
            cv2.imshow('detected circles',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    else:
        print "Camera Failed To Initialize"

except Exception,e:
    print "Fatal Error Occured:"
    print str(e)
          

       

