# import libraries
import cv2
import numpy as np
import os
import glob
import random
import matplotlib.pyplot as plt
import time  # for timing

# scale the images (this need to change to a function that keeps the same resolution as before)


def stretch_img_random(img):
    height, width = img.shape[:2]

    stretchCoefficient = 0.4

    stretchFactor = random.uniform(
        1 - stretchCoefficient, 1 + stretchCoefficient)

    horizontalStrech = bool(random.getrandbits(1))

    if horizontalStrech:
        v1 = [stretchFactor, 0, 0]
        v2 = [0, 1, 0]
    else:
        v1 = [1, 0, 0]
        v2 = [0, stretchFactor, 0]

    M = np.matmul(np.float32(
        [[1, 0, width / 2], [0, 1, height / 2], [0, 0, 1]]), np.float32([v1, v2, [0, 0, 1]]))
    M = np.matmul(M, np.float32(
        [[1, 0, -width / 2], [0, 1, -height / 2], [0, 0, 1]]))

    output = cv2.warpAffine(img, M[:2], (width, height))

    return output


def shear_img_random(img):
    '''
        function that shears the image randomly
        input: image (Mat object)
        output: sheared image (Mat object)
    '''
    height, width = img.shape[:2]

    shearCoefficient = 0.5

    v1 = [1, (random.random() - 0.5) * shearCoefficient, 0]
    v2 = [(random.random() - 0.5) * shearCoefficient, 1, 0]

    M = np.matmul(np.float32(
        [[1, 0, width / 2], [0, 1, height / 2], [0, 0, 1]]), np.float32([v1, v2, [0, 0, 1]]))
    M = np.matmul(M, np.float32(
        [[1, 0, -width / 2], [0, 1, -height / 2], [0, 0, 1]]))

    output = cv2.warpAffine(img, M[:2], (width, height))

    return output


def zoom_image_random(img):
    '''
        function that scales the image randomly
        input: image (Mat object)
        output: translated image (Mat object)
    '''
    height, width = img.shape[:2]

    zoomCoefficient = 0.2

    zoomFactor = random.uniform(1 - zoomCoefficient, 1 + zoomCoefficient)

    v1 = [zoomFactor, 0, 0]
    v2 = [0, zoomFactor, 0]

    M = np.matmul(np.float32(
        [[1, 0, width / 2], [0, 1, height / 2], [0, 0, 1]]), np.float32([v1, v2, [0, 0, 1]]))
    M = np.matmul(M, np.float32(
        [[1, 0, -width / 2], [0, 1, -height / 2], [0, 0, 1]]))

    output = cv2.warpAffine(img, M[:2], (width, height))

    return output


# flip the images horizontally
def flip_image_random(img):
    '''
        function that flips the image randomly
        input: image (Mat object)
        output: flipped image (Mat object)
    '''
    output = cv2.flip(img, random.randint(-2, 1))
    return output

# rotate the images
def rotate_image_random(img):
    '''
        function that rotates the image randomly
        input: image (Mat object)
        output: rotated image (Mat object)
    '''
    a = random.randint(0, 3)
    if a == 3:
        return img

    return cv2.rotate(img, a)

# translate the images
def translate_image_random(img):
    '''
        function that translates the image randomly
        input: image (Mat object)
        output: translated image (Mat object)
    '''
    # Store height and width of the image
    height, width = img.shape[:2]
    # for the new height, take a random number between -height and height
    new_height = random.randint(-height/4, height/4)
    # for the new width, take a random number between -width and width
    new_width = random.randint(-width/4, width/4)
    # Create translation matrix
    M = np.float32([[1, 0, new_width], [0, 1, new_height]])  # type: ignore
    # Apply translation
    output = cv2.warpAffine(img, M, (width, height))
    return output

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

# Change to canny edge detection
def canny_edge(img):
    '''
        function that changes the image to canny edge detection randomly
        input: image (Mat object)
        output: canny edge detection image (Mat object)
    '''
    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur the image
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    # apply canny edge detection
    # needs finetuning for fully edge detection
    canny = cv2.Canny(blur, 10, 160)
    # convert back to bgr
    canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    # add canny image to the original image
    output = cv2.addWeighted(img, 0.9, canny, 0.9, 0)
    return output

# Put random noise over the image
def add_noise_random(img):
    '''
        function that adds noise to the image randomly
        input: image (Mat object)
        output: image with added noise (Mat object)
    '''
    row,col,ch= img.shape
    mean = 0
    var = 0.1
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col,ch)) * 50
    gauss = gauss.reshape(row,col,ch).astype(np.float32)
    noisy = np.clip(cv2.add(img.astype(np.float32), gauss), 0, 255).astype(np.uint8)
    return noisy
    

# import image
img = cv2.imread(os.path.join("blok2", "v1", "data", "test_img.jpg"))
cv2.imshow("original", img)
# noise added to image
while (cv2.waitKey(500) != 27):
    img2 = add_noise_random(img)
# show image
    cv2.imshow("image", img2)

# path = 'C:/Users/nadin/Documents/GitHub/Embedded---Plastics-classifier/blok2/v1/augmented_dataset/rock'

# # path to the new folder where the images will be saved
# path_new = path + "_temp"

# # if folder does not exist, create it
# if not os.path.exists(path_new):
#     os.makedirs(path_new)

# # create a list with all the images
# images = glob.glob(path + "/*.jpg")

# # loop over all images
# for image in images:
#     # save the image
#     # cv.imwrite(path_new + "/" + os.path.basename(image), res)

#     # save image with timestamp
#     cv2.imwrite(path_new + "/" + os.path.basename(image) +
#                 str(time.time()) + ".jpg", img2)

cv2.waitKey(0)
cv2.destroyAllWindows()
