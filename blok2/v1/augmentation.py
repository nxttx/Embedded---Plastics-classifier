# import libraries
import cv2
import numpy as np
import os
import glob
import random
from skimage import color
from skimage import data, exposure, img_as_float
import matplotlib.pyplot as plt

# scale the images
def scale_image_random(img):
    '''
        function that scales the image randomly
        input: image (Mat object)
        output: translated image (Mat object)
    '''
    a = random.randint(1, 640)
    # resolution: 640 x 480
    size = (a, round(0.75*a)) # (width, height) and 0.75 is the aspect ratio
    output = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return output


# flip the images horizontally
def flip_image_random(img):
    '''
        function that flips the image randomly
        input: image (Mat object)
        output: flipped image (Mat object)
    '''
    output = cv2.flip(img, random.randint(-2, 1))
    return output

# rotate the images
def rotate_image_random(img):
    '''
        function that rotates the image randomly
        input: image (Mat object)
        output: rotated image (Mat object)
    '''
    a = random.randint(0, 3)
    if a == 3:
        return img

    return cv2.rotate(img, a)

# translate the images
def translate_image_random(img):
    '''
        function that translates the image randomly
        input: image (Mat object)
        output: translated image (Mat object)
    '''
    # Store height and width of the image
    height, width = img.shape[:2]
    # for the new height, take a random number between -height and height
    new_height = random.randint(-height/4, height/4)
    # for the new width, take a random number between -width and width
    new_width = random.randint(-width/4, width/4)
    # Create translation matrix
    M = np.float32([[1, 0, new_width], [0, 1, new_height]])  # type: ignore
    # Apply translation
    output = cv2.warpAffine(img, M, (width, height))
    return output

# higher contrast
def higher_contrast_random(img):
    '''
        function that highers the contrast of the image randomly
        input: image (Mat object)
        output: contrast highered image (Mat object)
    '''
    # convert to LAB
    LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # split the channels
    L, A, B = cv2.split(LAB)
    # create random float contrast
    contrast = random.uniform(0.0, 1.8)
    # apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=contrast, tileGridSize=(8,8))
    cl = clahe.apply(L)
    # merge the channels
    Limg = cv2.merge((cl,A,B))
    # convert back to BGR
    output = cv2.cvtColor(Limg, cv2.COLOR_LAB2BGR)
    return output

# change brightness
def change_brightness_random(img):
    '''
        function that changes the brightness of the image randomly
        input: image (Mat object)
        output: image with changed brightness (Mat object)
    '''
    # convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # change the brightness
    brightness = random.randint(-50, 50)
    h,s,v = cv2.split(hsv)

    vnew = np.mod(v + brightness, 255).astype(np.uint8)

    hsv_new = cv2.merge([h,s,vnew])

    # convert back to bgr
    output = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)

    # normalize the image
    output = cv2.normalize(output, output, 10, 200, cv2.NORM_MINMAX) 

        
    return output
    

# rotate on hsv values
def rotate_hsv_random(img):
    '''
        function that rotates the image randomly
        input: image (Mat object)
        output: rotated image (Mat object)
    '''
    # convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # rotate the hue channel
    rotation = random.randint(-10, 10)
    h,s,v = cv2.split(hsv)

    hnew = np.mod(h + rotation, 180).astype(np.uint8)

    hsv_new = cv2.merge([hnew,s,v])

    # convert back to bgr
    output = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
    return output






# import image
img = cv2.imread('C:\\Users\\nadin\\Documents\\GitHub\\Embedded---Plastics-classifier\\blok2\\v1\\data\\test_img.jpg')
cv2.imshow("original", img)
# scale image
while(cv2.waitKey(500) != 27):
    img2 = change_brightness_random(img)
    # show image
    cv2.imshow("image", img2)

# cv2.waitKey(0)
cv2.destroyAllWindows()