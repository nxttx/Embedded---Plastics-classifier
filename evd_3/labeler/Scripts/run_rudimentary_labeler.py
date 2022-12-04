import os
import sys

# hacky way to import from parent directory
sys.path.insert(0, os.path.join('evd_3', 'pre_processing'))
from removing_background import remove_background
from inspect import getsourcefile
from os.path import abspath
import cv2
import glob


classes = ["hangloose", "ignore", "paper", "rock", "scissors"]

current_dir = os.path.dirname(abspath(getsourcefile(lambda: 0)))

dataPath = os.path.join(current_dir, "..", "dataset")

for label in classes:
    print("processing {}".format(label))
    classPath = os.path.join(dataPath, label)
    image_filenames = glob.glob(classPath + "/*.jpg")

    for image_filename in image_filenames:

        if "_binary" in image_filename:
            os.remove(image_filename)
            continue

        image = cv2.imread(image_filename)

        binary_image = remove_background(image)

        cv2.imshow("image", image)
        cv2.imshow("binary_image", binary_image)

        (fileName, fileExtension) = os.path.splitext(image_filename)

        cv2.imwrite(fileName + "_binary" + ".bmp", binary_image)

        cv2.waitKey(1)

        print(image_filename)
