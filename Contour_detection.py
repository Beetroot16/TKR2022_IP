import cv2
import numpy as np
import matplotlib.pyplot as plt


def nothing(x):
    # any operation
    pass

def bounding_box(p):
    xbbox = int(p[0])
    ybbox = int(p[0])



cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_COMPLEX
    
while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90,180,120])
    upper_blue = np.array([120,255,255])

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

        if area > 250:
            #cv2.drawContours(frame, [approx], 0, (0, 255, 0), 5)

            #if len(approx) == 3:
            #    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
            if len(approx) == 4 or len(approx) == 5:
                cv2.drawContours(frame, [approx], 0, (0, 255, 0),5)
                print("Points Approx")
                print(approx)
                #cv2.putText(frame, "CHAL RHA HAI BC", (x, y), font, 0.5, (0, 0, 0))
                print("Approx ends")
                rc = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rc)
                print("Box starts")
                
                for p in box:
                    pt = (int(p[0]),int(p[1]))
                    print(pt)
                    cv2.circle(frame,pt,2,(0,0,0),2)
                print("Box Ends")
                



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