import cv2
import random
import numpy as np

# higher contrast


def higher_contrast_random(img):
    '''
        function that highers the contrast of the image randomly
        input: image (Mat object)
        output: contrast highered image (Mat object)
    '''
    # convert to LAB
    LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # split the channels
    L, A, B = cv2.split(LAB)
    # create random float contrast
    contrast = random.uniform(0.0, 1.8)
    # apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=contrast, tileGridSize=(8, 8))
    cl = clahe.apply(L)
    # merge the channels
    Limg = cv2.merge((cl, A, B))
    # convert back to BGR
    output = cv2.cvtColor(Limg, cv2.COLOR_LAB2BGR)
    return output

# change brightness


def change_brightness_random(img):
    '''
        function that changes the brightness of the image randomly
        input: image (Mat object)
        output: image with changed brightness (Mat object)
    '''
    alpha = random.uniform(1.0, 1.35)  # Simple contrast control
    beta = random.uniform(0.0, 20.0)   # Simple brightness control

    # Do the operation new_image(i,j) = alpha*image(i,j) + beta
    # new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
    output = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    return output

# rotate on hsv values


def rotate_hsv_random(img):
    '''
        function that rotates the image randomly
        input: image (Mat object)
        output: rotated image (Mat object)
    '''
    # convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # rotate the hue channel
    rotation = random.randint(-10, 10)
    h, s, v = cv2.split(hsv)

    hnew = np.mod(h + rotation, 180).astype(np.uint8)

    hsv_new = cv2.merge([hnew, s, v])

    # convert back to bgr
    output = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
    return output

# Put random noise over the image


def add_noise_random(img):
    '''
        function that adds noise to the image randomly
        input: image (Mat object)
        output: image with added noise (Mat object)
    '''
    row, col, ch = img.shape
    mean = 0
    var = 0.1
    sigma = var**0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch)) * 50
    gauss = gauss.reshape(row, col, ch).astype(np.float32)
    noisy = np.clip(cv2.add(img.astype(np.float32), gauss),
                    0, 255).astype(np.uint8)
    return noisy
