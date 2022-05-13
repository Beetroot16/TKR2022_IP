import cv2
from cv2 import WINDOW_AUTOSIZE
import numpy as np
import matplotlib.pyplot as plt
import time

x1 = 0
x2 = 0
x3 = 0
x4 = 0
y1 = 0
y2 = 0
y3 = 0
y4 = 0
x1b = 0
x3b = 0
y1b = 0
y3b = 0

width = 0
height = 0

width_factor = 0
height_factor = 0

coordinates = 0 
frame = np.zeros((100,100,3), dtype=np.uint8)
mida = 0
midb = 0
roi = np.zeros((720,1280,3), dtype=np.uint8)

def bounding_box(box):
    global roi, frame
    global x1
    x1 = int(box[0][0])
    global y1
    y1 = int(box[0][1])
    global x2
    x2 = int(box[1][0])
    global y2
    y2 = int(box[1][1])
    global x3 
    x3 = int(box[2][0])
    global y3
    y3 = int(box[2][1])
    global x4
    x4 = int(box[3][0])
    global y4
    y4 = int(box[3][1])
    midx2 = (x1 + x3) / 2
    midx1 = (x2 + x4) / 2
    midx = (midx1 + midx2) / 2
    global mida
    mida = int(midx)
    midX = str(mida)
    midy1 = (y2 + y4) / 2
    midy2 = (y1 + y3) / 2
    midy = (midy1 + midy2) / 2
    global midb
    midb = int(midy)
    midY = str(midy)
    global coordinates
    coordinates = (mida,midb)

    global width,height
    width = x4-x1
    height = y4-y3

    global width_factor
    global height_factor

    width_factor = int(width)
    height_factor = int(2*height)

    global x1b , y1b , x2b , y2b , x3b , y3b , x4b , y4b

    x1b = int(box[0][0]) - width_factor
    y1b = int(box[0][1]) 
    x2b = int(box[1][0]) - width_factor
    y2b = int(box[1][1]) - height_factor
    x3b = int(box[2][0]) + width_factor
    y3b = int(box[2][1]) - height_factor
    x4b = int(box[3][0]) + width_factor
    y4b = int(box[3][1])

    print(x2,y2) 

    start =[x2b,y2b]
    end = [x4b,y4b]

    if width > 3 and height > 3:
        rect = cv2.rectangle(frame,start,end,(0,0,255),2)
        cv2.putText(frame, "Ball", (end), font, 0.5, (0, 0, 0))
        cv2.circle(frame,(mida ,midb - int((height_factor)/2)),1,(0,0,0),2)

    # BOUNDING BOX ENDS
    roi = frame[y2b:y4b, x2b:x4b]


cap = cv2.VideoCapture(2)

blank_image = np.zeros((720,1280,3), np.uint8) 

font = cv2.FONT_HERSHEY_COMPLEX
    
while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    lower_blue = np.array([90,100,100])
    upper_blue = np.array([120,355,355])

    #kernels
    kernel1 = np.ones((15,15), np.float32)/225
    kernel2 = np.ones((10,10), np.uint8)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #blur = cv2.GaussianBlur(frame, (15,15), 0)
    res = cv2.bitwise_and(frame ,frame , mask = mask)
    opening = cv2.morphologyEx(res, cv2.MORPH_OPEN,kernel2)
    edges = cv2.Canny(opening, 150 , 100)


    # Contours detection
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

        #print(x,y)

        #print(x,y)


        if area > 100:
            #cv2.drawContours(frame, [approx], 0, (0, 255, 0), 5)

            # cv2.circle(frame,(mida ,midb - int((height_factor)/2)),1,(0,0,0),2)

            #if len(approx) == 3:
            #    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
            if len(approx) < 30:
                #cv2.drawContours(frame, [approx], 0, (0, 255, 0),5)
                rc = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rc)

                bounding_box(box)

    #OPEN CV IMSHOW

    cv2.imshow("Frame", frame)
    #cv2.imshow("hsv", hsv)
    #cv2.imshow("Canny", edges)
    #cv2.imshow("res", res)
    cv2.imshow("Opening",opening)
    #cv2.imshow("test",blank_image)
    #cv2.imshow("test2",box_new)
    try:
        cv2.imshow("Blank",roi)
    except:
        pass

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()