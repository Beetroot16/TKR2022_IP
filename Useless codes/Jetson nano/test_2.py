import cv2
from cv2 import COLOR_BGR2HSV
import numpy as np
import serial
import keyboard 

cap = cv2.VideoCapture(1)

roimain = np.zeros((720,1280,3),dtype= np.uint8)

key = None

while True:
    ret , frame = cap.read()

    if keyboard.is_pressed('1'):  # if key 'q' is pressed 
        key = 1
    if keyboard.is_pressed('2'):  # if key 'q' is pressed 
        key = 2
    if key == 1:
        roimain = frame[200:500,200:500]
    if key == 2:
        roimain = frame[100:500,100:500]

    # cv2.imshow('frame',frame)
    cv2.imshow('roimain',roimain)
    # cv2.imshow('gray',gray)

    if cv2.waitKey(1) and 0xFF == ('q'):
        break
cap.release()
cv2.destroyAllWindows()