import os
import sys
import cv2
import numpy as np

# hacky way to import from parent directory
sys.path.insert(0, os.path.join('evd_3', 'pre_processing'))
from removing_background import remove_background

dataset_path = os.path.join("evd_3", "original_dataset")
custom_label_path = os.path.join("evd_3", "labeler", "dataset")


def get_augmented_and_label(type, file, M=np.eye(3)):
    '''
    Returns the augmented image and the label for the image
    '''
    image = cv2.imread(os.path.join(dataset_path, type, file))

    height, width = image.shape[:2]

    binary_image = np.zeros((1, 1, 3), np.uint8)

    (file_name, file_extension) = os.path.splitext(file)

    binary_image_path = os.path.join(
        custom_label_path, type, file_name + "_binary.bmp")
    if os.path.isfile(binary_image_path):
        binary_image = cv2.imread(binary_image_path, 0)
    else:
        binary_image = remove_background(image)

    imageMatrix = np.eye(3)

    imageMatrix = np.matmul(np.float32(
        [[1, 0, width / 2], [0, 1, height / 2], [0, 0, 1]]), M)  # type: ignore
    imageMatrix = np.matmul(imageMatrix, np.float32(
        [[1, 0, -width / 2], [0, 1, -height / 2], [0, 0, 1]]))  # type: ignore

    image = cv2.warpAffine(
        image, imageMatrix[:2], (width, height), borderMode=cv2.BORDER_REPLICATE)
    binary_image = cv2.warpAffine(
        binary_image, imageMatrix[:2], (width, height))

    # calculate the new bounding box
    top = height
    bottom = 0
    left = width
    right = 0

    for i in range(height):
        for j in range(width):
            if binary_image[i, j] > 0:
                top = min(top, i)
                bottom = max(bottom, i)
                left = min(left, j)
                right = max(right, j)

    # calculate normalized bounding box
    center_x = (left + right) / 2 / width
    center_y = (top + bottom) / 2 / height
    width = (right - left) / width
    height = (bottom - top) / height

    return image, [center_x, center_y, width, height]
