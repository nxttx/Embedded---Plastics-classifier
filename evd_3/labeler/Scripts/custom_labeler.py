import os
import glob
import cv2
import numpy as np
from inspect import getsourcefile
from os.path import abspath

import sys

# hacky way to import from parent directory
sys.path.insert(0, os.path.join('evd_3', 'pre_processing'))
from removing_background import remove_background

image = np.zeros((1, 1, 3), np.uint8)
binary_image = np.zeros((1, 1, 3), np.uint8)
brush_size = 5
drawing = False  # true if left mouse is pressed
deleting_toggle = False


def on_mouse(event, x, y, flags, params):
    global drawing, deleting, brush_size, image, binary_image

    if event == cv2.EVENT_LBUTTONDOWN:
        print("left button down")
        drawing = True
    if event == cv2.EVENT_LBUTTONUP:
        print("left button up")
        drawing = False

    if event == cv2.EVENT_MOUSEMOVE and drawing:
        print("drawing")
        color = (0, 0, 0) if deleting_toggle else (255, 255, 255)
        cv2.circle(binary_image, (x, y),
                   brush_size, color, -1)


def read_files_into_buffers(file):
    global image, binary_image

    print("reading {}".format(file))

    image = cv2.imread(file)
    (fileName, fileExtension) = os.path.splitext(file)

    binary_image_filename = fileName + "_binary" + ".bmp"

    binary_image = cv2.imread(binary_image_filename, 0)


def save_buffers_to_files(file):
    global binary_image

    print("saving {}".format(file))

    (fileName, fileExtension) = os.path.splitext(file)

    binary_image_filename = fileName + "_binary" + ".bmp"

    cv2.imwrite(binary_image_filename, binary_image)


classes = ["hangloose", "ignore", "paper", "rock", "scissors"]

current_dir = os.path.dirname(abspath(getsourcefile(lambda: 0)))

dataPath = os.path.join(current_dir, "..", "dataset")

image_filenames = []

for label in classes:
    classPath = os.path.join(dataPath, label)
    image_filenames += glob.glob(classPath + "/*.jpg")

# hacky way to work around wsl bug
first_key = -1
first_key_registered = False

index = 0

read_files_into_buffers(image_filenames[index])
cv2.imshow("image", image)
cv2.setMouseCallback('image', on_mouse)

while True:

    # blend image and binary_image
    temp_rgb_binary_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2RGB)
    blended_image = cv2.addWeighted(image, 0.5, temp_rgb_binary_image, 0.5, 0)
    cv2.imshow("image", blended_image)
    cv2.setMouseCallback('image', on_mouse)

    key = cv2.waitKey(16)

    if key != -1 and first_key_registered == False:
        first_key = key
        first_key_registered = True

    if key != -1:
        print("key: {}".format(key))

    if (key == ord('q') or key == 27) and key != first_key:
        break
    elif key == ord('d'):
        save_buffers_to_files(image_filenames[index])
        index += 1
        if index >= len(image_filenames):
            index = 0
        read_files_into_buffers(image_filenames[index])
    elif key == ord('a'):
        save_buffers_to_files(image_filenames[index])
        index -= 1
        if index < 0:
            index = len(image_filenames) - 1
        read_files_into_buffers(image_filenames[index])
    elif key == ord('r'):
        binary_image = remove_background(image)
    elif key == ord('t'):
        deleting_toggle = not deleting_toggle
    elif key == ord('w'):
        brush_size += 1
        print("brush size: {}".format(brush_size))
    elif key == ord('s'):
        brush_size -= 1
        print("brush size: {}".format(brush_size))

    if brush_size < 1:
        brush_size = 1
    elif brush_size > 50:
        brush_size = 50


cv2.destroyAllWindows()
