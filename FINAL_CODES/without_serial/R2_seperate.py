import requests
import cv2
from numpy import array,uint8

url = r"http://192.168.186.254:8080/shot.jpg"
while True:
    online_vid = requests.get(url)
    online_vid_arr = array(bytearray(online_vid.content),dtype = uint8)
    online_img = cv2.imdecode(online_vid_arr, -1)

    img = online_img
    image = img

    cv2.rectangle(image, (130,240), (230,600), (0,0,255), 5)
    cv2.rectangle(image, (330,240), (420,600), (0,0,255), 5)
    cv2.rectangle(image, (520,240), (610,600), (0,0,255), 5)
    # cv2.circle(image,(174,130),35,(0,0,0),5)
    # cv2.circle(image,(345,130),35,(0,0,0),5)
    # cv2.circle(image,(515,132),35,(0,0,0),5)

    cv2.imshow('image_window',image)
    if cv2.waitKey(1) and 0xFF == ('q'):
        break
cv2.cap.release()
cv2.destroyAllWindows()