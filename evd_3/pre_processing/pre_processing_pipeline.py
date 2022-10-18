from inspect import getsourcefile
from os.path import abspath
import os
import glob
import cv2
from feature_extraction import extract_features
from removing_background import remove_background
import pandas as pd


classes = ["hangloose", "ignore", "paper", "rock", "scissors"]

current_dir = os.path.dirname(abspath(getsourcefile(lambda: 0)))

dataPath = os.path.join(current_dir, "..", "original_dataset")

dataset = []

for label in classes:
    print("processing {}".format(label))
    classPath = os.path.join(dataPath, label)
    image_filenames = glob.glob(classPath + "/*.jpg")

    for image_filename in image_filenames:
        #print("image {}".format(image_filename))
        image = cv2.imread(image_filename)

        binary_image = remove_background(image)

        features = list(extract_features(binary_image))

        row = [label]
        row.extend(features)

        frame = pd.DataFrame(row)

        dataset.append(row)

dataset = pd.DataFrame(dataset)
# columns=["label", "area", "perimeter", "aspect_ratio", "extent", "pa_ratio", "number_of_hull_defects"]
dataset.to_csv("dataset.csv")
