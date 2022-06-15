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

x_coordinates_contour = [0,0,0,0]
y_coordinates_contour = [0,0,0,0]
x_coordinates_bbox = [0,0,0,0]
y_coordinates_bbox = [0,0,0,0]

midx = 0
midy = 0

box = [[0,0],[0,0],[0,0],[0,0]]

def image_operations(roimain,kernel):
    hsv = cv2.cvtColor(roimain,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    res = cv2.bitwise_and(roimain,roimain,mask=mask)

    opening = cv2.morphologyEx(res,cv2.MORPH_OPEN,kernel)
    edges = cv2.Canny(opening,150,100)

    cv2.imshow('opening',opening) #for debugging
    
    return edges

def contour_detection(roimain,edges):
    global red,yellow,green,box
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
        # cv2.drawContours(roimain, [approx], 0, (0, 0, 0), 5)
    
        rc = cv2.minAreaRect(count)
        box = cv2.boxPoints(rc)

        return box

def bounding_box(roimain,box):
    global x_coordinates_contour,x_coordinates_bbox,y_coordinates_contour,y_coordinates_bbox,midx,midy
    # x1
    x_coordinates_contour[0]= int(box[0][0])
    # x2
    x_coordinates_contour[1]= int(box[1][0])
    # x3
    x_coordinates_contour[2]= int(box[2][0])
    # x4
    x_coordinates_contour[3]= int(box[3][0])

    # y1
    y_coordinates_contour[0]= int(box[0][1])
    # y2
    y_coordinates_contour[1]= int(box[1][1])
    # y3
    y_coordinates_contour[2]= int(box[2][1])
    # y4
    y_coordinates_contour[3]= int(box[3][1])

    # (x1+x3)/2
    mid_x1 = ((x_coordinates_contour[0]+x_coordinates_contour[2])/2)
    
    # (x2+x4)/2
    mid_x2 = ((x_coordinates_contour[1]+x_coordinates_contour[3])/2)

     # (y1+y3)/2
    mid_y1 = ((y_coordinates_contour[0]+y_coordinates_contour[2])/2)
    
    # (y2+y4)/2
    mid_y2 = ((y_coordinates_contour[1]+y_coordinates_contour[3])/2)

    # final contour midpoint
    midx = (mid_x1+mid_x2)//2
    midy = (mid_y1+mid_y2)//2

    width = x_coordinates_contour[3]-x_coordinates_contour[0]
    height = y_coordinates_contour[3]- y_coordinates_contour[2]

    x_coordinates_bbox[1] = int(x_coordinates_contour[1]-width)
    x_coordinates_bbox[3] = int(x_coordinates_contour[3]+width)

    y_coordinates_bbox[1] = int(y_coordinates_contour[1]-(height*2))
    y_coordinates_bbox[3] = int(y_coordinates_contour[3])

    start = ( x_coordinates_bbox[1],y_coordinates_bbox[1])
    end = (x_coordinates_bbox[3],y_coordinates_bbox[3])

    rect = cv2.rectangle(roimain,start,end,(0,0,255),3)

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
    box = contour_detection(roimain,edges)
    try:
        bounding_box(roimain,box)
    except:
        pass

    # cv2.imshow('frame',frame)
    cv2.imshow('roimain',roimain)

    if cv2.waitKey(1) and 0xFF == ('q'):
        break
cap.release()
cv2.destroyAllWindows()