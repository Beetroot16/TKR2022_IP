import cv2
from cv2 import COLOR_BGR2HSV
import numpy as np
import keyboard 

cap = cv2.VideoCapture(1)

#defining main roi
roimain = np.zeros((480,480,3))

key = None

#defining blue for mask
lower_blue = np.array([90,100,100])
upper_blue = np.array([120,355,355])

#kernel
kernel = np.ones((10,10),np.uint8)

#For imchecker
red = True
yellow = False
green = False

def image_operations(roimain,kernel):
    hsv = cv2.cvtColor(roimain,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    res = cv2.bitwise_and(roimain,roimain,mask=mask)

    opening = cv2.morphologyEx(res,cv2.MORPH_OPEN,kernel)
    edges = cv2.Canny(opening,150,100)

    cv2.imshow('opening',opening) #for debugging
    
    return edges

def contour_detection(roimain,edges):
    global red,yellow,green
    if int(cv2.__version__[0])>3:
            contours,_=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    else :
        _,contours,_=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    if contours == ():
        red = True
        yellow = False
        green = False
    else:
        red = False
        yellow = True
        green = False

    for count in contours :
            area = cv2.contourArea(count)
            approx = cv2.approxPolyDP(count,0.02*cv2.arcLength(count,True),True)
            cv2.drawContours(roimain, [approx], 0, (0, 0, 0), 5)

while True:
    ret, frame = cap.read()

    roimain = frame #defaultroi 

    if keyboard.is_pressed('1'):  # if key 'q' is pressed 
        key = 1
    if keyboard.is_pressed('2'):  # if key 'q' is pressed 
        key = 2
    if key == 1:
        roimain = frame[200:500,200:500]
    if key == 2:
        roimain = frame[100:500,100:500]

    edges = image_operations(roimain,kernel)
    contour_detection(roimain,edges)

    # cv2.imshow('frame',frame)
    cv2.imshow('roimain',roimain)

    if cv2.waitKey(1) and 0xFF == ('q'):
        break
cap.release()
cv2.destroyAllWindows()