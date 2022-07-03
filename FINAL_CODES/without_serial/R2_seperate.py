import requests
from cv2 import imdecode,rectangle,circle,imshow
from numpy import array,uint8

url = r"http://192.168.211.122:8080/shot.jpg"

online_vid = requests.get(url)
online_vid_arr = array(bytearray(online_vid.content),dtype = uint8)
online_img = imdecode(online_vid_arr, -1)

img = online_img
image = img

rectangle(image, (140,-10), (210,250), (0,0,0), 5)
rectangle(image, (310,-10), (385,250), (0,0,0), 5)
rectangle(image, (475,-10), (555,250), (0,0,0), 5)
circle(image,(174,130),35,(0,0,0),5)
circle(image,(345,130),35,(0,0,0),5)
circle(image,(515,132),35,(0,0,0),5)

imshow('image_window',image)