from cv2 import VideoCapture,cvtColor,COLOR_BGR2HSV,inRange,bitwise_and,morphologyEx,MORPH_OPEN,Canny,__version__,findContours,RETR_TREE,CHAIN_APPROX_SIMPLE,contourArea,approxPolyDP,arcLength,minAreaRect,boxPoints,rectangle,circle,imdecode,imshow,waitKey,destroyAllWindows,moveWindow,namedWindow
import numpy as np
import requests
from serial import Serial

cap = VideoCapture(0)

arduino = Serial(port='COM20', baudrate=115200, timeout=1) 

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
    hsv = cvtColor(roimain,COLOR_BGR2HSV)
    mask = inRange(hsv,lower_blue,upper_blue)
    res = bitwise_and(roimain,roimain,mask=mask)

    opening = morphologyEx(res,MORPH_OPEN,kernel)
    edges = Canny(opening,150,100)


    # cv2.imshow('opening',opening) #for debugging
    
    return edges

def contour_detection(roimain,edges):
    global red,yellow,green,box
    if int(__version__[0])>3:
            contours,_=findContours(edges,RETR_TREE,CHAIN_APPROX_SIMPLE)
    else :
        _,contours,_=findContours(edges,RETR_TREE,CHAIN_APPROX_SIMPLE)
    
    if contours == ():
        red = True
        yellow = False
        green = False
    else:
        red = False
        yellow = True
        green = False

    for count in contours :
        area = contourArea(count)
        approx = approxPolyDP(count,0.02*arcLength(count,True),True)
        # cv2.drawContours(roimain, [approx], 0, (0, 0, 0), 5)
    
        rc = minAreaRect(count)
        box = boxPoints(rc)

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
    rect = rectangle(roimain,end,start,(0,0,255),3)
    circle(frame,(xtest + x1roi,ytest + y1roi),5,(0,0,255))
    # cv2.circle(frame,((int((x2-x1)/2 + x1),ytest + y1roi)),2,(255,255,255))
    circle(frame,(320,ytest + y1roi),2,(0,255,255))

    difference = xtest + x1roi - 320

    # print(difference)

    data = str(difference)+"\n"
    data = data.encode('utf-8')
    arduino.write(data)

    line = arduino.read_all().decode()
    print(line)

def r2(url):
    online_vid = requests.get(url)
    online_vid_arr = np.array(bytearray(online_vid.content),dtype = np.uint8)
    online_img = imdecode(online_vid_arr, -1)

    img = online_img
    image = img

    rectangle(image, (140,-10), (210,250), (0,0,0), 5)
    rectangle(image, (310,-10), (385,250), (0,0,0), 5)
    rectangle(image, (475,-10), (555,250), (0,0,0), 5)
    circle(image,(174,130),35,(0,0,0),5)
    circle(image,(345,130),35,(0,0,0),5)
    circle(image,(515,132),35,(0,0,0),5)

    imshow('image_window',image)

while True:
    ret, frame = cap.read()

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
    
    winname = "frame"
    namedWindow(winname)  
    moveWindow(winname, 200,300)
    imshow(winname,frame)
    r2(url)
    # cv2.imshow('roimain',roimain)
    # cv2.imshow('edges',edges)

    if waitKey(1) and 0xFF == ('q'):
        break
cap.release()
destroyAllWindows()