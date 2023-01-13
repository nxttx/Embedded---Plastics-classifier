import os
from tensorflow import keras
import cv2

# Load the model
model = keras.models.load_model(os.path.join(
    "evd_3", "deep_learning", "cnn_notebook", "best_model"))

cam = cv2.VideoCapture(0)
print("Cam is opend:" + str(cam.isOpened()))
while cv2.waitKey(1) != 27:
    ret, frame = cam.read()

    if frame is None:
        print('No frame')
        continue

    prediction = model(frame)

    cv2.imshow("Frame", frame)
