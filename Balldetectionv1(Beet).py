import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    col_lower = [90,150,80]
    col_higher = [120,255,255]

    lowercol = np.array(col_lower)
    uppercol = np.array(col_higher)


    kernel1 = np.ones((15,15), np.float32)/225
    kernel2 = np.ones((5,5), np.uint8)

    mask = cv2.inRange(hsv, lowercol, uppercol)
    #smooth = cv2.filter2D(frame, -1 , kernel1)
    blur = cv2.GaussianBlur(frame, (15,15), 0)
    res = cv2.bitwise_and(blur ,blur , mask = mask)
    opening = cv2.morphologyEx(res, cv2.MORPH_OPEN,kernel2)
    opening2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN,kernel2)


    median = cv2.medianBlur(res ,15)
    bi = cv2.bilateralFilter(res,15,75,75)
    edges = cv2.Canny(opening2, 200 , 200)

    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #cv2.imshow('smooth',smooth)
    #cv2.imshow('blur',blur)
    #cv2.imshow('median',median)
    #cv2.imshow('bi',bi)
    cv2.imshow('edges',edges)
    cv2.imshow('opening',opening)
    cv2.imshow('opening2',opening2)

    k = cv2.waitKey(5) and 0xFF
    if k ==27:
        break

cv2.destroyAllWindows
cap.release()