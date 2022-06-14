import cv2
from cv2 import WINDOW_AUTOSIZE
import numpy as np
import matplotlib.pyplot as plt
#import serial
import time

#GLOBAL VARIABLES

x1=0
x2=0
x3=0
x4=0
y1=0
y2=0
y3=0
y4 = 0
midX = 0
midY = 0

coordinates = 0
box = 0

#Range of mask
lower_blue = np.array([90,80,80])
upper_blue = np.array([120,255,200])

#Area thresholds
lowerarea = 300
upperarea = None

#Length threshhold
lenthresh = 12

#arduino = serial.Serial(port='COM6',baudrate = 9600, timeout = .1)

cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_COMPLEX

#OUTPUT GLOBAL VARIABLES
mask = None
edges = None
res = None
opening = None

#KERNELS
kernel1 = np.ones((15,15), np.float32)/225
kernel2 = np.ones((5,5), np.uint8)

def bounding_box():
    #GETTING THE GLOBAL VARIABLES

    global x1,y1,x2,y2,x3,y3,x4,y4
    global midX,midY
    global box 
    #global arudino

    #STORING VALUES OF THE CONTOUR EDGES IN CO_ORDINATES
    x1 = int(box[0][0]) #leftbottom
    y1 = int(box[0][1]) #leftbottom
    x2 = int(box[1][0]) #lefttop
    y2 = int(box[1][1]) #lefttop
    x3 = int(box[2][0]) #righttop
    y3 = int(box[2][1]) #righttop
    x4 = int(box[3][0]) #rightbottom
    y4 = int(box[3][1]) #rightbottom

    #FINDING THE CENTER CO-ORDINATE
    midx1 = int((x1 + x3)/2)
    midx2 = int((x2 + x4)/2)
    midy1 = int((y2 + x4)/2)
    midy2 = int((y1 + y3)/2)
    midX = int((midx1 + midx2)/2)
    midY = int((midy1 + midy2)/2)

    coordinates = (midX,midY) #final co-ordinates to be sent to arduino in int form

    #MAKING THE BOUNDING BOX
    width = x4-x1
    height = y4-y3

    #FACTORS FOR THE BOUNDING BOX
    width_factor = int(width)
    height_factor = int(2*height)

    #COORDINATES FOR THE BOUNDING BOX
    x1b = int(box[0][0]) - width_factor
    y1b = int(box[0][1]) 
    x2b = int(box[1][0]) - width_factor
    y2b = int(box[1][1]) - height_factor
    x3b = int(box[2][0]) + width_factor
    y3b = int(box[2][1]) - height_factor
    x4b = int(box[3][0]) + width_factor
    y4b = int(box[3][1])

    #FINAL COORDINATES TO DRAW THE BOUNDING BOX
    start = [x1b,y1b]
    end = [x3b,y3b]

    #DRAWING ONLY THE NESSARRY BOUNDING BOXES 
    if width > 10 and height >10:
        rect = cv2.rectangle(frame,start,end,(0,0,255),2) #Drawing the red bounding box on the frame.

def filters(frame,kernel1,kernel2,lower_blue,upper_blue):

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #converting BGR to HSV

    mask = cv2.inRange(hsv,lower_blue,upper_blue) #making the mask

    #blur = cv2.GaussianBlur(frame, (15,15), 0) #applying a Gausian filer on the frame

    res = cv2.bitwise_and(frame,frame,mask = mask) #Showing only the blue pixels

    opening = cv2.morphologyEx(res, cv2.MORPH_OPEN,kernel2) #morph on blue pixels to remove background noise

    edges = cv2.Canny(opening,150,100) #canny edge detection on the final blue

def contour_detection(edges):
    #FOR DIFFRENT OPENCV VERSIONS 
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #MAIN CONTOURS FOR LOOP
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
    
    #FILTER VIA AREA
    if area > 300 and area < 900:
        cv2.circle(frame,(midX,midY),1,(0,0,0),2) #Points out the co-ordinate given to Arduino

        #FILTER VIA SIDES OF CONTOUR
        if len(approx) < lenthresh:
            cv2.drawContours(frame, [approx], 0, (0, 255, 0),5) #Draws Contours
            cv2.putText(frame, "CHAL RHA HAI BC", (x, y), font, 0.5, (0, 0, 0)) #Adds text next to the object
            rc = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rc)

def output(frame,mask,edges,res,opening):
    cv2.imshow("Frame",frame)
    #cv2.imshow("Mask", mask)
    #cv2.imshow("Canny", edges)
    cv2.imshow("res", res)
    cv2.imshow("Opening",opening)

while True:

    _, frame = cap.read()

    filters(frame,kernel1,kernel2,lower_blue,upper_blue)

    contour_detection(edges)

    bounding_box(box)

    output(frame,mask,edges,res,opening)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()