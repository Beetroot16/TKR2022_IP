import cv2
import numpy as np
import requests

cap = cv2.VideoCapture(0)

url = r"http://192.168.211.122:8080/shot.jpg"

#defining main roi
roimain = np.zeros((480,480,3))

key = None

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


#for roi 
def nothing(x):
    pass

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

def bounding_box(roimain,box,x2,x1):
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
    cv2.circle(frame,(xtest + x1roi,ytest + y1roi),5,(0,0,255))
    # cv2.circle(frame,((int((x2-x1)/2 + x1),ytest + y1roi)),2,(255,255,255))
    cv2.circle(frame,(320,ytest + y1roi),2,(0,255,255))

    difference = xtest + x1roi - 320

    print(difference)

def r2(image):
    cv2.rectangle(image, (125,-10), (200,550), (0,0,255), 5)
    cv2.rectangle(image, (275,-10), (350,550), (0,0,255), 5)
    cv2.rectangle(image, (425,-10), (500,550), (0,0,255), 5)

while True:
    ret, frame = cap.read()

    online_vid = requests.get(url)
    online_vid_arr = np.array(bytearray(online_vid.content),dtype = np.uint8)
    online_img = cv2.imdecode(online_vid_arr, -1)

    img = online_img
    image = img

    r2(image)
            
    cv2.imshow('image_window',image)

    #defining blue for mask
    # lower_blue = np.array([hue_s,sat_thres,val_thres])
    # upper_blue = np.array([hue_e,355,355])

    lower_blue = np.array([90,50,50])
    upper_blue = np.array([120,355,355])

    roimain = frame #defaultroi

    # roimain = frame[y1roi:y2roi,x1roi:x2roi]

    edges = image_operations(roimain,kernel)
    box = contour_detection(roimain,edges)
    try:
        bounding_box(roimain,box,x2roi,x1roi)
    except:
        pass

    # cv2.imshow('frame',frame)
    cv2.imshow('roimain',roimain)
    # cv2.imshow('edges',edges)

    if cv2.waitKey(1) and 0xFF == ('q'):
        break
cap.release()
cv2.destroyAllWindows()