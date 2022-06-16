import numpy as np 
import cv2 

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.rectangle(frame, (125,-10), (200,550), (0,0,255), 5)
    cv2.rectangle(frame, (275,-10), (350,550), (0,0,255), 5)
    cv2.rectangle(frame, (425,-10), (500,550), (0,0,255), 5)
    cv2.imshow('Video Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 