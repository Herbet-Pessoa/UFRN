#pip install Pillow
#pip install opencv-python
import PIL
import cv2
import numpy as np

# erosion
def erode(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(img, kernel, iterations=1)

#Dilation
def dilation(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(img,kernel,iterations = 1)

# opening -- erosion followed by a dilation
def opening(img):
    kernel = np.ones((5,5), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def grayScale(self, img):
    img_escala_cinza = cv2.imread(img, 0)
    cv2_imshow(img_escala_cinza)

    return 