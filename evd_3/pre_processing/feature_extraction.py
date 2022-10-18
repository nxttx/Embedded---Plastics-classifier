import cv2
import numpy as np
from math import sqrt
import os

features = ["area", "perimeter", "aspect_ratio",
            "extent", "pa_ratio", "number_of_hull_defects"]


def extract_features(image):
    contours, hierarchy = cv2.findContours(
        image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if (len(contours) < 1):
        return np.array((0, 0, 0, 0, 0, 0))

    contour = max(contours, key=cv2.contourArea)

    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    minAreaRect = cv2.minAreaRect(contour)
    (x, y), (width, height), angle = minAreaRect
    aspect_ratio = min(width, height) / max(width, height)
    # rect_area = width * height
    # extend = area / rect_area
    extend = area / cv2.contourArea(cv2.convexHull(contour))
    pa_ratio = perimeter / sqrt(area)

    approx_contour = cv2.approxPolyDP(contour, perimeter * 0.001, True)
    hull = cv2.convexHull(approx_contour, returnPoints=False)
    defects = cv2.convexityDefects(approx_contour, hull)

    number_of_hull_defects = len(defects)

    dst = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(dst, [contour], 0, (255, 0, 0), 3)
    cv2.drawContours(dst, [approx_contour], 0, (0, 255, 0), 2)

    box = cv2.boxPoints(minAreaRect)
    box = np.int0(box)
    cv2.drawContours(dst, [box], 0, (0, 255, 255), 2)

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(approx_contour[s][0])
        end = tuple(approx_contour[e][0])
        far = tuple(approx_contour[f][0])
        cv2.line(dst, start, end, [0, 0, 255], 2)
        cv2.circle(dst, far, 5, [0, 0, 255], -1)

    cv2.imshow("intermediate", dst)

    return np.array((area, perimeter, aspect_ratio, extend, pa_ratio, number_of_hull_defects))


if __name__ == "__main__":
    absolute_path = os.path.join(
        os.getcwd(), "evd_3", "original_dataset", "hangloose", "image1665496251.jpg")

    image = cv2.imread(absolute_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.blur(image, (3, 3))
    binary = cv2.inRange(image, (0, 24, 96), (15, 175, 255))

    kernel = np.ones((7, 7), np.uint8)

    binary = cv2.erode(binary, kernel)
    binary = cv2.dilate(binary, kernel)

    features = extract_features(binary)

    #cv2.imshow("binary", binary)
    cv2.waitKey(0)
    print(features)
