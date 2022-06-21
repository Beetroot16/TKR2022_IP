import keyboard
import cv2
cap = cv2.VideoCapture(0)
while True:
     ret, frame = cap.read()
     hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
     cv2.imshow("frame",frame)
     if keyboard.is_pressed('e'):
        cv2.imshow("e",hsv)
     
     if cv2.waitKey(1) and 0xFF == ('q'):
        break
cap.release()
cv2.destroyAllWindows()


