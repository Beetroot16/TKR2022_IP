import cv2
import numpy as np
import matplotlib.pyplot as plt


def nothing(x):
    # any operation
    pass

def bounding_box(box):
    x1 = int(box[0][0])
    y1 = int(box[0][1])
    x2 = int(box[1][0])
    y2 = int(box[1][1])
    x3 = int(box[2][0])
    y3 = int(box[2][1])
    x4 = int(box[3][0])
    y4 = int(box[3][1])

    width = x4-x1
    height = y4-y3

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

    #print("x1,y1")
    #print(x1,y1)
    #print("x2,y2")
    #print(x2,y2)
    #print("x3,y3")
    #print(x3,y3)
    #print("x4,y4")
    #print(x4,y4)
    if width > 10 and height > 10:
     #print("start")
     #print(start)
     #print("end")
     #print(end)

     rect = cv2.rectangle(frame,start,end,(0,0,255),2)



cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_COMPLEX
    
while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    lower_blue = np.array([90,120,100])


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

        if area > 100 and area < 900:
            #cv2.drawContours(frame, [approx], 0, (0, 255, 0), 5)

            #if len(approx) == 3:
            #    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
            if len(approx) < 12:
                #cv2.drawContours(frame, [approx], 0, (0, 255, 0),5)
                #print("Points Approx")
                #print(approx)
                #cv2.putText(frame, "CHAL RHA HAI BC", (x, y), font, 0.5, (0, 0, 0))
                #print("Approx ends")
                rc = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rc)

                for p in box:
                    pt = (int(p[0]),int(p[1]))
                    #cv2.circle(frame,pt,2,(0,0,0),2)

                #print("start")
                #print(box)
                #print("end")

                bounding_box(box)
            
            #print(len(approx))
                



            #elif 10 < len(approx) < 20:
            #    cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))

            #print(len(approx))
        

    #OPEN CV IMSHOW

    cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)
    cv2.imshow("Canny", edges)
    #cv2.imshow("res", res)
    cv2.imshow("Opening",opening)


    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()