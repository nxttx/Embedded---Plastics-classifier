# import libraries
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import cv2
from imutils import paths
from scipy.ndimage import median_filter


# import the data
# don't know if you need this or the data splitted like below
pathData = list(paths.list.images("C:/Users/nadin/Afbeeldingen/data"))
pathRock = list(paths.list.images("C:/Users/nadin/Afbeeldingen/data/rock"))
pathPaper = list(paths.list.images("C:/Users/nadin/Afbeeldingen/data/paper"))
pathScissors = list(paths.list.images(
    "C:/Users/nadin/Afbeeldingen/data/scissors"))
pathHangLoose = list(paths.list.images(
    "C:/Users/nadin/Afbeeldingen/data/hangloose"))
pathIgnore = list(paths.list.images("C:/Users/nadin/Afbeeldingen/data/ignore"))

# functions to clean the data
# remove outliers                                                                      # not sure if this is the right way to do it


# limit is the number of pixels that are allowed to be different from the median
def filter(pathData, limit):
    print("Median-Filter...")
    filteredImg = np.array(median_filter(
        pathData, size=limit)).astype(np.float32)
    return filteredImg

# remove missing values                                                                  # not sure if this is the right way to do it


def removeMissingValues(pathData):
    print("Removing missing values...")
    pathData = pathData.dropna()
    return pathData

# remove duplicates                                                                      # not sure if this is the right way to do it


def removeDuplicates(pathData):
    print("Removing duplicates...")
    pathData = pathData.drop_duplicates()
    return pathData

# function to split the data into features and labels   	                          # not sure if this is the right way to do it


def splitData(pathData):
    print("Splitting data...")
    X = pathData.drop("label", axis=1)
    y = pathData["label"]
    return X, y

# function to split the data into training and testing                                     # not sure if this is the right way to do it


def splitTrainTest(pathData):
    print("Splitting data into training and testing...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# function to train the model


def trainModel(X_train, y_train):
    print("Training model...")
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model


# perform functions
pathData = filter(pathData, 3)
pathData = removeMissingValues(pathData)
pathData = removeDuplicates(pathData)
X, y = splitData(pathData)
X_train, X_test, y_train, y_test = splitTrainTest(pathData)
model = trainModel(X_train, y_train)
