import cv2
from cv2 import WINDOW_AUTOSIZE
import numpy as np
import matplotlib.pyplot as plt
import serial
import time

x1 = 0
x2 = 0
x3 = 0
x4 = 0
y1 = 0
y2 = 0
y3 = 0
y4 = 0

width_factor = 0
height_factor = 0

coordinates = 0 
frame = np.zeros((100,100,3), dtype=np.uint8)
mida = 0
midb = 0
roi = np.zeros((100,100,3), dtype=np.uint8)

arduino = serial.Serial(port='COM10', baudrate=9600, timeout=1) 

def bounding_box(box):
    #global arduino  
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
    #print(midX,",", midY , "\n")
    global coordinates
    coordinates = (mida,midb) 
    #print(coordinates)


    width = x4-x1
    height = y4-y3

    global width_factor
    global height_factor

    width_factor = int(width)
    height_factor = int(2*height)



    x1b = int(box[0][0]) - width_factor
    y1b = int(box[0][1]) 
    x2b = int(box[1][0]) - width_factor
    y2b = int(box[1][1]) - height_factor
    x3b = int(box[2][0]) + width_factor
    y3b = int(box[2][1]) - height_factor
    x4b = int(box[3][0]) + width_factor
    y4b = int(box[3][1])

    start =[x1b,y1b]
    end = [x3b,y3b]

    # print("x1,y1")
    # print(x1,y1)
    # print("x2,y2")
    # print(x2,y2)
    # print("x3,y3")
    # print(x3,y3)
    # print("x4,y4")
    # print(x4,y4)
    if width > 10 and height > 10:
     #print("start")
     #print(start)
     #print("end")
     #print(end)

        rect = cv2.rectangle(frame,start,end,(0,0,255),2)
        cv2.putText(frame, "Ball", (end), font, 0.5, (0, 0, 0))

    arduino.write((midX+","+midY+"\n").encode())
    # time.sleep(0.5)
    message = arduino.readline().rstrip().decode('utf-8')
    print(message)

    # BOUNDING BOX ENDS
    roi = frame[x1b:x3b, y3b:y1b]
    #print("ROI Starts")
    #print(roi)

    print(x2b,y2b)

cap = cv2.VideoCapture(1)

font = cv2.FONT_HERSHEY_COMPLEX
    
while True:

    _, frame = cap.read()

    
    # print(y1,y2,y3,y4)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    lower_blue = np.array([90,100,140])
    upper_blue = np.array([120,255,200])

    #kernels
    kernel1 = np.ones((15,15), np.float32)/225
    kernel2 = np.ones((5,5), np.uint8)

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


        if area > 300:
            #cv2.drawContours(frame, [approx], 0, (0, 255, 0), 5)

            #print(mida,midb)

            cv2.circle(frame,(mida ,midb - int((height_factor)/2)),10,(0,0,0),2)

            #if len(approx) == 3:
            #    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
            if len(approx) < 20:
                cv2.drawContours(frame, [approx], 0, (0, 255, 0),5)
                #print("Points Approx")
                #print(approx)
                #cv2.putText(frame, "CHAL RHA HAI BC", (x, y), font, 0.5, (0, 0, 0))
                #print("Approx ends")
                rc = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rc)

                #print("start")
                #print(box)
                #print("end")

                bounding_box(box)
            
            #print(len(approx))
                



            #elif 10 < len(approx) < 20:
            #    cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))

            #print(len(approx))
        
    # vidcroped = frame[x1:x4,y2:y1]

    #OPEN CV IMSHOW

    cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)
    #cv2.imshow("Canny", edges)
    #cv2.imshow("res", res)
    cv2.imshow("Opening",opening)

    #cv2.namedWindow("cropped",WINDOW_AUTOSIZE)

    #if x1 == 0 and x4 == 0 and y2 == 0 and y1 == 0:
        #cv2.imshow("cropped",roi)
    # else:
    #     cv2.destroyWindow("cropped")


    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()