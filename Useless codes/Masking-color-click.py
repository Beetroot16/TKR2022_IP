# masking using mouse click

import cv2
import numpy as np
cap = cv2.VideoCapture(0)

# global variables
colorsB = 0
colorsG = 0
colorsR = 0


# mouse call back function
def mouseRGB(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: 
        global colorsB 
        colorsB = frame[y,x,0]

        
        global colorsG
        colorsG = frame[y,x,1]

        global colorsR
        colorsR = frame[y,x,2]

        colors = frame[y,x]

        print("Red: ",colorsR)
        print("Green: ",colorsG)
        print("Blue: ",colorsB)
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)





cv2.namedWindow('mouseRGB')
cv2.setMouseCallback('mouseRGB',mouseRGB)

capture = cv2.VideoCapture(0)

while(True):

    ret, frame = capture.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
# adjust the ranges +-10
    lower_red = np.array ([colorsB - 10,colorsG - 10,colorsR - 10])
    upper_red = np.array([colorsB + 10,colorsG + 10,colorsR + 10])

    mask =cv2.inRange(hsv,lower_red,upper_red)
    res = cv2.bitwise_and(frame,frame,mask=mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('hsv',hsv)
    cv2.imshow('mouseRGB', frame)



    


    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()