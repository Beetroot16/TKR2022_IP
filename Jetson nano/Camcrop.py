import cv2
import numpy as np

def nothing():
    pass
cap = cv2.VideoCapture(0)

img = np.zeros((300,512,3),dtype = np.uint8)
cv2.namedWindow('image')

roi = np.zeros((720,1280,3),dtype= np.uint8)

cv2.createTrackbar('X1','image',0,1000,nothing)
cv2.createTrackbar('X2','image',0,1000,nothing)
cv2.createTrackbar('Y1','image',0,1000,nothing)
cv2.createTrackbar('Y2','image',0,1000,nothing)

while True:
    _, frame = cap.read()

    x1 = cv2.getTrackbarPos('X1','image')
    x2 = cv2.getTrackbarPos('X2','image')
    y1 = cv2.getTrackbarPos('Y1','image')
    y2 = cv2.getTrackbarPos('Y2','image')

    if x2>x1 and y2>y1:
        roi = frame[y1:y2,x1:x2]
        cv2.imshow("frame",frame)
        try:
            cv2.imshow("roi",roi)
        except:
            pass
        

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()


    


