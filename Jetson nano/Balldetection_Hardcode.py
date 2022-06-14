import cv2
import numpy as np

# DEFINITIONS 

cap = cv2.VideoCapture(0)

# defining color variables for checker
red = True # defualt value is red 
yellow = False
green = False

# defining main roi
roimain = np.zeros((720,1280,3),dtype= np.uint8)

start = None
end = None

# defining contour coordinates
x_coordinates_contour = [0,0,0,0]
y_coordinates_contour = [0,0,0,0]

# defining bounding box  coordinates
x_coordinates_bbox = [0,0,0,0]
y_coordinates_bbox = [0,0,0,0]
 
# defining blank rois
roi = np.zeros((720,1280,3),dtype= np.uint8)
rgbaroi = np.zeros((720,1280,3),dtype= np.uint8)
roiedges = np.zeros((720,1280,3),dtype= np.uint8)
roi_gray = np.zeros((720,1280,3),dtype= np.uint8)

# defining frame
frame = np.zeros((100,100,3),dtype=np.uint8)

midx = 0
midy = 0

# THRESHOLD VALUES  

area_threshold = 20
length_threshold = 40

def boundingbox(box):
    #GLOBAL VARIABLES

    # (2).----------.(3)
    #   |           |
    #   |           |
    #   |           |
    #   |           |
    #   |           |
    # (1).----------.(4)

    global roi , roi_gray , x_coordinates_contour, y_coordinates_contour,frame,start,end,rgbaroi,roiedges,x1roi,x2roi,y1roi,y2roi,red,yellow,green,midx,midy,list
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

    # weidth and height of contours
    width = x_coordinates_contour[3]-x_coordinates_contour[0]
    height = y_coordinates_contour[3]- y_coordinates_contour[2]

    # x1 bounding box
    # x_coordinates_bbox[0] = int(x_coordinates_contour[0]-width)
    # x2 bounding box
    x_coordinates_bbox[1] = int(x_coordinates_contour[1]-width)
    # x3 bounding box
    # x_coordinates_bbox[2] = int(x_coordinates_contour[2]+width)
    # x4 bounding box
    x_coordinates_bbox[3] = int(x_coordinates_contour[3]+width)

    # y1 bounding box
    # y_coordinates_bbox[0] = int(y_coordinates_contour[0])
    # y2 bounding box
    y_coordinates_bbox[1] = int(y_coordinates_contour[1]-(height*2))
    # y3 bounding box
    # y_coordinates_bbox[2] = int(y_coordinates_contour[2]-(height*2))
    # y4 bounding box
    y_coordinates_bbox[3] = int(y_coordinates_contour[3])

    start = ( x_coordinates_bbox[1] + x1roi,y_coordinates_bbox[1] + y1roi)
    end = (x_coordinates_bbox[3] + x1roi,y_coordinates_bbox[3] + y1roi)

    rect = cv2.rectangle(frame,start,end,(0,0,255),3)
    # if rect:
    #     count += 1
    # else:

    # defining roi
    roi = frame[y_coordinates_bbox[1]+y1roi:y_coordinates_bbox[3]+y1roi,x_coordinates_bbox[1]+x1roi:x_coordinates_bbox[3]+x1roi]

def haarcascade(roi,roi_gray):
    global red,yellow,green
    ball_cascade  = cv2.CascadeClassifier(r"C:\Users\Vishr\Desktop\TKR2022_IP\Jetson nano\ball_cascade.xml")
    ball = ball_cascade.detectMultiScale(roi,1,2)
    if ball != ():
        red = False
        yellow = False
        green = True
    
    for (x,y,w,h) in ball:
        circle_centre_x = (x+w//2)
        circle_centre_y = (y+h//2)

        cv2.circle(roi,(circle_centre_x,circle_centre_y),1,(0,0,0),4)

        rect = cv2.rectangle(frame,start,end,(0,255,255),2)

def image_checker(width, height, rgb_color=(0, 0, 0)):
    # Create black blank image
    checkerimage = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    checkerimage[:] = color

    return checkerimage

def E():
    roitrackbar = frame[170:295,237:394]
    hsv = cv2.cvtColor(roitrackbar,cv2.COLOR_BGR2HSV)
    rgba = cv2.cvtColor(roitrackbar, cv2.COLOR_BGR2RGBA)
    gray = cv2.cvtColor(roitrackbar,cv2.COLOR_BGR2GRAY)

while True:
    _, frame = cap.read()


