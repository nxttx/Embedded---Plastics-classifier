#  import all data of dataset (rock, paper, scissors, hangloose, ignore)
#  and remove green/blue background
#  and save it in a new folder

import cv2 as cv
import numpy as np
import os
import glob

# import all data of dataset (rock, paper, scissors, hangloose, ignore)
# and remove green/blue background
# and save it in a new folder

# ask for the path to the folder with the images
path = input("Enter the path to the folder with the images: ")

# path to the new folder where the images will be saved
path_new = path + "_new"

# if folder does not exist, create it
if not os.path.exists(path_new):
    os.makedirs(path_new)

# create a list with all the images
images = glob.glob(path + "/*.jpg")

# loop over all images
for image in images:
    # read the image
    img = cv.imread(image)
    img = cv.blur(img,(3,3))

    # convert to HSV
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # # define range of blue color in HSV
    light_blue = (0,50,0)
    dark_blue = (255,255,255)

    # # Mark pixels outside background color range
    mask = cv.inRange(img_hsv, light_blue, dark_blue)
    res = mask

    # remove green sleeve
    light_green = (15, 0, 0)
    dark_green = (127, 255, 255)

    # Mark pixels outside background color range
    mask_sleeve = cv.inRange(img_hsv, light_green, dark_green)
    res2 = mask_sleeve

    # invert the mask
    res2 = cv.bitwise_not(res2)

    # combine the two masks
    res = cv.bitwise_and(res, res2)

    # save the image
    cv.imwrite(path_new + "/" + os.path.basename(image), res)

    # show the image
    cv.imshow("image", res)
    key = cv.waitKey(5)
    # if key == 27: # wait for ESC key to exit
    #     break




# # show the images
# cv.imshow('image', img)

# cv.waitKey(0)
cv.destroyAllWindows()



