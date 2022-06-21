import cv2
import numpy as np

import time

cap = cv2.VideoCapture(0)

# arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1) 

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

x1roi = 0
x2roi = 0
y1roi = 0
y2roi = 0

key = 0

keys = [1,2,3,4,5,6,7,8,9,10,11]

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
    mid_x1 = ((x_coordinates_contour[0]+x_coordinates_contour[1])/2)
    
    # (x2+x4)/2
    mid_x2 = ((x_coordinates_contour[3]+x_coordinates_contour[2])/2)

    # (y1+y3)/2
    mid_y1 = ((y_coordinates_contour[3]+y_coordinates_contour[0])/2)
    
    # (y2+y4)/2
    mid_y2 = ((y_coordinates_contour[1]+y_coordinates_contour[2])/2)

    # final contour midpoint
    midx = (mid_x1+mid_x2)//2
    midy = (mid_y1+mid_y2)//2

    width = x_coordinates_contour[2]-x_coordinates_contour[0]
    height = y_coordinates_contour[3]- y_coordinates_contour[0]

    x_coordinates_bbox[0] = int(x_coordinates_contour[0]-width)
    x_coordinates_bbox[1] = int(x_coordinates_contour[1]-width)
    x_coordinates_bbox[2] = int(x_coordinates_contour[2]+width)
    x_coordinates_bbox[3] = int(x_coordinates_contour[3]+width)

    y_coordinates_bbox[0] = int(y_coordinates_contour[0])
    y_coordinates_bbox[1] = int(y_coordinates_contour[1]-(height*2))
    y_coordinates_bbox[2] = int(y_coordinates_contour[2]-(height*2))
    y_coordinates_bbox[3] = int(y_coordinates_contour[3])

    start = (x_coordinates_bbox[0],y_coordinates_bbox[1])
    end = (x_coordinates_bbox[2],y_coordinates_bbox[3])

    xtest = int(midx)
    ytest = int(midy)
    rect = cv2.rectangle(roimain,end,start,(0,0,255),3)
    cv2.circle(frame,((xtest + x1roi,ytest + y1roi)),5,(0,0,255))

 
# def keybinds():
#     global x1roi,y1roi,x2roi,y2roi,key
#     if keyboard.is_pressed('e'):  # if key 'q' is pressed
#         x1roi = 237
#         x2roi = 394
#         y1roi = 170
#         y2roi = 295
#         key = 1
#     if keyboard.is_pressed('c'):  # if key 'q' is pressed 
#         x1roi = 257
#         x2roi = 407
#         y1roi = 165
#         y2roi = 303
#         key = 2
#     if keyboard.is_pressed('b'):  # if key 'q' is pressed 
#         x1roi = 252
#         x2roi = 387
#         y1roi = 224
#         y2roi = 318
#         key = 3
#     if keyboard.is_pressed('d'):  # if key 'q' is pressed 
#         x1roi = 244
#         x2roi = 399
#         y1roi = 216
#         y2roi = 331
#         key = 4
#     if keyboard.is_pressed('a'):  # if key 'q' is pressed 
#         x1roi = 252
#         x2roi = 382
#         y1roi = 262
#         y2roi = 351
#         key = 5
#     if keyboard.is_pressed('f'):  # if key 'q' is pressed 
#         x1roi = 237
#         x2roi = 389
#         y1roi = 260
#         y2roi = 356
#         key = 6
#     if keyboard.is_pressed('k'):  # if key 'q' is pressed 
#         x1roi = 219
#         x2roi = 387
#         y1roi = 196
#         y2roi = 300
#         key = 7
#     if keyboard.is_pressed('h'):  # if key 'q' is pressed 
#         x1roi = 252
#         x2roi = 387
#         y1roi = 201
#         y2roi = 300
#         key = 8
#     if keyboard.is_pressed('j'):  # if key 'q' is pressed 
#         x1roi = 206
#         x2roi = 382
#         y1roi = 237
#         y2roi = 356
#         key = 9
#     if keyboard.is_pressed('g'):  # if key 'q' is pressed 
#         x1roi = 260
#         x2roi = 427
#         y1roi = 262
#         y2roi = 366
#         key = 10
#     if keyboard.is_pressed('i'):  # if key 'q' is pressed 
#         x1roi = 247
#         x2roi = 382
#         y1roi = 272
#         y2roi = 377
#         key = 11

while True:
    ret, frame = cap.read()

    roimain = frame #defaultroi
    
    # keybinds()

    if key in keys:
        roimain = frame[y1roi:y2roi,x1roi:x2roi]

    edges = image_operations(roimain,kernel)
    box = contour_detection(roimain,edges)
    try:
        bounding_box(roimain,box)
    except:
        pass

    # cv2.imshow('frame',frame)
    cv2.imshow('roimain',roimain)
    cv2.imshow('edges',edges)

    if cv2.waitKey(1) and 0xFF == ('q'):
        break
cap.release()
cv2.destroyAllWindows()