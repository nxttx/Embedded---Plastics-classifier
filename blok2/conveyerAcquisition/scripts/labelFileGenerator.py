'''
  Label file generator for the conveyer acquisition system.
  This script generates label files for every image in the dataset.
  The label files are generated in the same directory as the images.
  The label files are named the same as the image files, but with the extension .txt.
  The label files contain the class label and the bounding box coordinates.
  The bounding box coordinates are normalized to the range [0, 1].
  The class labels are:
    # 0: Ignore
    1: Bag
    2: Bottlecap
    3: Fork
    4: Knife  
    5: Pen
    6: Spoon 
    7: Styrofoam
'''
# imports
import os
import cv2
import numpy as np


def remove_background(src):
    '''
    Remove the background from the image.

    Arguments: 
        {Mat} src: The source image. 
    Returns:
        {Mat} The image with the background removed.
    '''
    return src



def get_bounding_box(src):
    '''
    Get the bounding box of the object in the image.

    Arguments:
        {Mat} src: The source image.
    Returns:
        Output: {int[]} - The bounding box coordinates.   
    '''

    return (0, 0, 0, 0)


if __name__ == "__main__":
    # dataset image directories
    root_dir = os.path.join("blok2", "conveyerAcquisition", "datasets")
    bag_dir = os.path.join(root_dir, "bag")
    bottlecap_dir = os.path.join(root_dir, "bottlecap")
    fork_dir = os.path.join(root_dir, "fork")
    knife_dir = os.path.join(root_dir, "knife")
    pen_dir = os.path.join(root_dir, "pen")
    spoon_dir = os.path.join(root_dir, "spoon")
    styrofoam_dir = os.path.join(root_dir, "styrofoam")


    # get all images in the dataset
    bag_images = os.listdir(bag_dir)
    bottlecap_images = os.listdir(bottlecap_dir)
    fork_images = os.listdir(fork_dir)
    knife_images = os.listdir(knife_dir)
    pen_images = os.listdir(pen_dir)
    spoon_images = os.listdir(spoon_dir)
    styrofoam_images = os.listdir(styrofoam_dir)

    # loop over every image and generate label file
    for image in bag_images:
        img = cv2.imread(os.path.join(bag_dir, image))
        cv2.imshow("org", img)
        img = remove_background(img)
        cv2.imshow("WB", img)
        cv2.waitKey(0)
        # x, y, w, h = get_bounding_box(img)

        # # now write label file
        # with open(os.path.join(bag_dir, image.replace('.jpg', '.txt')), 'w') as f:
        #     f.write('1 {} {} {} {}'.format(x+w/2, y+h/2, w, h))

