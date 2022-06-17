import cv2
from cv2 import COLOR_BGR2HSV
import numpy as np

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

img = np.zeros((300,400,3),dtype = np.uint8)
cv2.namedWindow('image',cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar('1','image',0,1000,nothing)
cv2.createTrackbar('2','image',0,1000,nothing)
cv2.createTrackbar('s','image',0,255,nothing)
cv2.createTrackbar('v','image',0,255,nothing)
cv2.createTrackbar('s1','image',0,255,nothing)
cv2.createTrackbar('v1','image',0,255,nothing)

while True:
    ret , frame = cap.read()

    # gray = cv2.cvtColor(frame,COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(frame,COLOR_BGR2HSV)

    s = cv2.getTrackbarPos('s','image')
    v = cv2.getTrackbarPos('v','image')
    s1 = cv2.getTrackbarPos('s1','image')
    v1 = cv2.getTrackbarPos('v1','image')

    kernel = np.ones((10,10),np.uint8)


    mask = cv2.inRange(hsv,(0,s,v),(360,s1,v1))
    res = cv2.bitwise_and(frame,frame,mask=mask)

    opening = cv2.morphologyEx(res,cv2.MORPH_OPEN,kernel)

    t1 = cv2.getTrackbarPos('1','image')
    t2 = cv2.getTrackbarPos('2','image')

    # blur = cv2.GaussianBlur(frame, (15,15), 0)
    edges = cv2.Canny(opening,t1,t2)
    
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        # print(x,y)
        if area >50 and len(approx)<30:
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 5)
    
    cv2.imshow('frame',frame)
    cv2.imshow('edges',edges)
    cv2.imshow('opening',opening)
    # cv2.imshow('gray',gray)

    if cv2.waitKey(1) and 0xFF == ('q'):
        break

cap.release()
cv2.destroyAllWindows()