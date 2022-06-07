import cv2
import numpy as np

def create_blank(width, height, rgb_color=(0, 0, 0)):
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

# Create new blank 300x300 red image
width, height = 300, 300

red = (255, 0, 0)
image = create_blank(width, height, rgb_color=(100,100,255))
while True:
    cv2.imshow('red.jpg', image)

    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()