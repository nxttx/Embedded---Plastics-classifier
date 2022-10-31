import cv2 as cv
import numpy as np
import os
import glob

import time  # for timing


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


if __name__ == "__main__":
    # ask for the path to the folder with the images
    # path = input("Enter the path to the folder with the images: ")
    path = '/home/shinichi/dev/han/minorcvml/project/Embedded---Plastics-classifier/evd_3/original_dataset/hangloose'

    # path to the new folder where the images will be saved
    path_new = path + "_temp"

    # if folder does not exist, create it
    if not os.path.exists(path_new):
        os.makedirs(path_new)

    # create a list with all the images
    images = glob.glob(path + "/*.jpg")

    # loop over all images
    for image in images:
        # read the image
        img = cv.imread(image)
        res = remove_background(img)

        # save the image
        # cv.imwrite(path_new + "/" + os.path.basename(image), res)

        # save image with timestamp
        cv.imwrite(path_new + "/" + os.path.basename(image) +
                   str(time.time()) + ".jpg", res)

        # show the image
        cv.imshow("image", res)

        # check if the user wants to continue
        key = cv.waitKey(5)
        if key == 27:  # ESC
            break

    # clean up
    cv.destroyAllWindows()
