# get all the images in the folder

import os
import cv2 as cv
import numpy as np
from math import sqrt
import os

def remove_background(img):
    ''' 
        function that makes image into binary image and removes background
        input: image (Mat object)
        output: binary image
    '''

    img = cv.blur(img, (3, 3))

    # convert to HSV
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # define range of blue color in HSV
    light_blue = (0, 50, 0)
    dark_blue = (255, 255, 255)

    # Mark pixels outside background color range
    mask = cv.inRange(img_hsv, light_blue, dark_blue)
    res = mask

    # remove green sleeve
    light_green = (13, 0, 0)
    dark_green = (127, 255, 255)

    # Mark pixels outside background color range
    mask_sleeve = cv.inRange(img_hsv, light_green, dark_green)
    res2 = mask_sleeve

    # invert the mask
    res2 = cv.bitwise_not(res2)

    # combine the two masks
    res = cv.bitwise_and(res, res2)

    '''
        if blob is too small, remove it
    '''
    #  find contours
    contours, hierarchy = cv.findContours(
        res.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #  find the biggest area
    max_area = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv.contourArea(cnt)
        if (area > max_area):
            max_area = area

    #  if the area is less than 100 pixels, remove it
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv.contourArea(cnt)
        if (area < 10000):
            cv.drawContours(res, contours, i, 0, -1)

    return res



def extract_features(image):
    contours, hierarchy = cv.findContours(
        image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    if (len(contours) < 1):
        return np.array((0, 0, 0, 0, 0, 0))

    contour = max(contours, key=cv.contourArea)
    boundingRect = cv.boundingRect(contour)
    # normalize boundingRect
    x, y, w, h = boundingRect
    x = x / image.shape[1]
    y = y / image.shape[0]
    w = w / image.shape[1]
    h = h / image.shape[0]



    # return the features
    return np.array((x, y, w, h))
    




hangloose_dir = 'original_dataset/hangloose'
paper_dir = 'original_dataset/paper'
rock_dir = 'original_dataset/rock'
scissors_dir = 'original_dataset/scissors'

hangloose_images = os.listdir(hangloose_dir)
paper_images = os.listdir(paper_dir)
rock_images = os.listdir(rock_dir)
scissors_images = os.listdir(scissors_dir)

# loop over every image
for image in hangloose_images:
    img = cv.imread(os.path.join(hangloose_dir, image))
    img = remove_background(img)
    x, y, w, h = extract_features(img)

    # now write label file
    with open(os.path.join('original_dataset/hangloose/', image.replace('.jpg', '.txt')), 'w') as f:
        f.write('0 {} {} {} {}'.format(x+w/2, y+h/2, w, h))

for image in paper_images:
    img = cv.imread(os.path.join(paper_dir, image))
    img = remove_background(img)
    x, y, w, h = extract_features(img)

    # now write label file
    with open(os.path.join('original_dataset/paper/', image.replace('.jpg', '.txt')), 'w') as f:
        f.write('1 {} {} {} {}'.format(x+w/2, y+h/2, w, h))

for image in rock_images:
    img = cv.imread(os.path.join(rock_dir, image))
    img = remove_background(img)
    x, y, w, h = extract_features(img)

    # now write label file
    with open(os.path.join('original_dataset/rock/', image.replace('.jpg', '.txt')), 'w') as f:
        f.write('2 {} {} {} {}'.format(x+w/2, y+h/2, w, h))

for image in scissors_images:
    img = cv.imread(os.path.join(scissors_dir, image))
    img = remove_background(img)
    x, y, w, h = extract_features(img)

    # now write label file
    with open(os.path.join('original_dataset/scissors/', image.replace('.jpg', '.txt')), 'w') as f:
        f.write('3 {} {} {} {}'.format(x+w/2, y+h/2, w, h))


