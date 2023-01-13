import os
from tensorflow import keras
import cv2

# Load the model
model = keras.models.load_model(os.path.join(
    "evd_3", "deep_learning", "cnn_notebook", "best_model"))

class_names = ['hangloose', 'paper', 'rock', 'scissors']

cam = cv2.VideoCapture(3)
print("Cam is opend:" + str(cam.isOpened()))
while cv2.waitKey(1) != 27:
    ret, frame = cam.read()

    if frame is None:
        print('No frame')
        continue

    cv2.imshow("Frame", frame)
    frame = cv2.resize(frame, (320, 180)).reshape(1, 180, 320, 3)

    prediction = model.predict(frame)
    print(class_names[prediction.argmax()])
