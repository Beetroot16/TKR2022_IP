import cv2
import numpy as np

# blue color value
lower_blue = np.array([90,160,80])
upper_blue = np.array([120,355,355])

#white color value
lower_white = np.array([0,355,0])
upper_white = np.array([360,360,360])

start = None
end = None

# area threshold
area_threshold = 0

# length threshold
length_threshold = 30

# defining contour coordinates
x_coordinates_contour = [0,0,0,0]
y_coordinates_contour = [0,0,0,0]

# defining bounding box  coordinates
x_coordinates_bbox = [0,0,0,0]
y_coordinates_bbox = [0,0,0,0]
 
# defining blank rois
roi = np.zeros((720,1280,3),dtype= np.uint8)
rgbaroi = np.zeros((720,1280,3),dtype= np.uint8)
roi_gray = np.zeros((720,1280,3),dtype= np.uint8)

# defining frame
frame = np.zeros((100,100,3),dtype=np.uint8)
    
def bounding_box(box):
    global roi , roi_gray , x_coordinates_contour, y_coordinates_contour,frame,start,end,rgbaroi
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

    start = ( x_coordinates_bbox[1],y_coordinates_bbox[1])
    end = (x_coordinates_bbox[3],y_coordinates_bbox[3])

    # defining roi
    roi = frame[y_coordinates_bbox[1]:y_coordinates_bbox[3],x_coordinates_bbox[1]:x_coordinates_bbox[3]]
    rgbaroi = rgba[y_coordinates_bbox[1]:y_coordinates_bbox[3],x_coordinates_bbox[1]:x_coordinates_bbox[3]]

def haarcascade(roi,rgbaroi):
    ball_cascade  = cv2.CascadeClassifier("ball_cascade.xml")
    ball = ball_cascade.detectMultiScale(rgbaroi,2,1)

    for (x,y,w,h) in ball:
        circle_centre_x = (x+w//2)
        circle_centre_y = (y+h//2)

        cv2.circle(roi,(circle_centre_x,circle_centre_y),1,(0,0,0),4)

        rect = cv2.rectangle(frame,start,end,(0,255,255),2)

cap = cv2.VideoCapture(1)

while  True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # kernels
    kernel = np.ones((10,10),np.uint8)

    # image operations
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    res = cv2.bitwise_and(frame,frame,mask=mask)

    opening = cv2.morphologyEx(res,cv2.MORPH_OPEN,kernel)
    edges = cv2.Canny(opening,150,100)

    # contourr detection
    if int(cv2.__version__[0])>3:
        contours,_=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    else :
        _,contours,_=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for count in contours :
        area = cv2.contourArea(count)
        approx = cv2.approxPolyDP(count,0.02*cv2.arcLength(count,True),True)

        if area>area_threshold and len(approx)<length_threshold:
            rc = cv2.minAreaRect(count)
            box = cv2.boxPoints(rc)

            bounding_box(box)

    # detecting white ball

    # haarcascade(roi,rgbaroi)


    cv2.imshow("frame",frame)
    try:
        cv2.imshow("roi",rgbaroi)
    except:
        pass

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()