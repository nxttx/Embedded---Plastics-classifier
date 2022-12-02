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

def normalize_label_file(label_file):
    # open the label file
    with open(label_file, 'r') as f:
        lines = f.readlines()
    # open the label file again for writing
    with open(label_file, 'w') as f:
        for line in lines:
            # open image to get the width and height
            img = cv2.imread(label_file.replace(".txt", ".png"))

            # split the line into columns
            columns = line.split()

            # turn x, y from center to top left

            x = float(columns[1]) - float(columns[3])/2
            y = float(columns[2]) - float(columns[4])/2
            w = float(columns[3])
            h = float(columns[4])

            # draw the bounding box
            cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 2)

            # normalize the x, y, w, h
            x = x / img.shape[1]
            y = y / img.shape[0]
            w = w / img.shape[1]
            h = h / img.shape[0]

            # now turn the x, y, w, h back to center
            x = x + w/2
            y = y + h/2
            w = w
            h = h


            cv2.imshow("img", img)
            x = cv2.waitKey(0)
            if x != 27: # escape key
                # exit the program
                sys.exit(0)


            # write the normalized line to the label file
            f.write(columns[0] + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) + " ")
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
        normalize_label_file(label_file)
    for label_file in bottle_label_files:
        normalize_label_file(label_file)
    for label_file in bottlecap_label_files:
        normalize_label_file(label_file)
    for label_file in fork_label_files:
        normalize_label_file(label_file)
    for label_file in knife_label_files:
        normalize_label_file(label_file)
    for label_file in pen_label_files:
        normalize_label_file(label_file)
    for label_file in spoon_label_files:
        normalize_label_file(label_file)
    for label_file in styrofoam_label_files:
        normalize_label_file(label_file)

if __name__ == "__main__":
    main()


