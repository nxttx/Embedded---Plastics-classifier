# go over every label file (.txt) and normalize the 2,3,4, 5 column
# default photo format is: 640x480 

import sys
import cv2
import numpy as np
import os
import glob
import random
import matplotlib.pyplot as plt
import time  # for timing

def normalize_label_file(label_file, photo_width, photo_height):
    # open the label file
    with open(label_file, 'r') as f:
        lines = f.readlines()
    # open the label file again for writing
    with open(label_file, 'w') as f:
        for line in lines:
            # split the line into columns
            columns = line.split()
            # normalize the 2,3,4,5 columns
            columns[1] = str(float(columns[1]) / photo_width)
            columns[2] = str(float(columns[2]) / photo_height)
            columns[3] = str(float(columns[3]) / photo_width)
            columns[4] = str(float(columns[4]) / photo_height)
            # write the normalized line to the label file
            f.write(str(columns[0]) + ' ' + str(columns[1]) + ' ' + str(columns[2]) + ' ' + str(columns[3]) + ' ' + str(columns[4]))
            f.close()

def main():
    root_dir = os.path.join("blok2", "conveyerAcquisition", "datasets")
    bag_dir = os.path.join(root_dir, "bag")
    bottle_dir = os.path.join(root_dir, "bottle")
    bottlecap_dir = os.path.join(root_dir, "bottlecap")
    fork_dir = os.path.join(root_dir, "fork")
    knife_dir = os.path.join(root_dir, "knife")
    pen_dir = os.path.join(root_dir, "pen")
    spoon_dir = os.path.join(root_dir, "spoon")
    styrofoam_dir = os.path.join(root_dir, "styrofoam")

    # get all .txt files in the directories
    bag_label_files = glob.glob(os.path.join(bag_dir, "*.txt"))
    bottle_label_files = glob.glob(os.path.join(bottle_dir, "*.txt"))
    bottlecap_label_files = glob.glob(os.path.join(bottlecap_dir, "*.txt"))
    fork_label_files = glob.glob(os.path.join(fork_dir, "*.txt"))
    knife_label_files = glob.glob(os.path.join(knife_dir, "*.txt"))
    pen_label_files = glob.glob(os.path.join(pen_dir, "*.txt"))
    spoon_label_files = glob.glob(os.path.join(spoon_dir, "*.txt"))
    styrofoam_label_files = glob.glob(os.path.join(styrofoam_dir, "*.txt"))
    
    # normalize the label files
    for label_file in bag_label_files:
        normalize_label_file(label_file, 640, 480)
    for label_file in bottle_label_files:
        normalize_label_file(label_file, 640, 480)
    for label_file in bottlecap_label_files:
        normalize_label_file(label_file, 640, 480)
    for label_file in fork_label_files:
        normalize_label_file(label_file, 640, 480)
    for label_file in knife_label_files:
        normalize_label_file(label_file, 640, 480)
    for label_file in pen_label_files:
        normalize_label_file(label_file, 640, 480)
    for label_file in spoon_label_files:
        normalize_label_file(label_file, 640, 480)
    for label_file in styrofoam_label_files:
        normalize_label_file(label_file, 640, 480)

if __name__ == "__main__":
    main()


