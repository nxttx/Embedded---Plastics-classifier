'''
  The removeCables script removes the cables from the images.
    The script is called from the labelFileGenerator script.
    The script is called for every image in the dataset.
'''
# imports
import os
import cv2
import numpy as np


def removeCable(src):
    '''
    Remove the cables from the image by adding a black square of 73px x 73px.

    Arguments: 
        {Mat} src: The source image. 
    Returns:
        {Mat} The image with the cables removed.
    '''

    # add black square to the image
    cv2.rectangle(src, (567, 407), (640, 480), (25, 24, 24), -1)
    
    return src



if __name__ == "__main__":
    root_dir = os.path.join("blok2", "conveyerAcquisition", "datasets")

    knife_dir = os.path.join(root_dir, "bag")

    knife_images = os.listdir(knife_dir)

    for image in knife_images:
        img = cv2.imread(os.path.join(knife_dir, image))
        cv2.imshow("org", img)
        img = removeCable(img)
        cv2.imshow("WB", img)
        cv2.waitKey(0)