# import libraries
import sys
import cv2
import numpy as np
import os
import glob
import random
import matplotlib.pyplot as plt
import time  # for timing
import math

def get_new_boundingBox(boundingBox, M, width, height):
    # convert to corner cordinates
    boundingBoxTL = [boundingBox[0] - boundingBox[2] /
                     2, boundingBox[1] - boundingBox[3] / 2, 1]
    boundingBoxTR = [boundingBox[0] + boundingBox[2] /
                     2, boundingBox[1] - boundingBox[3] / 2, 1]
    boundingBoxBL = [boundingBox[0] - boundingBox[2] /
                     2, boundingBox[1] + boundingBox[3] / 2, 1]
    boundingBoxBR = [boundingBox[0] + boundingBox[2] /
                     2, boundingBox[1] + boundingBox[3] / 2, 1]

    # calculate new positions
    newBoundingBoxTL = M.dot(boundingBoxTL)
    newBoundingBoxTR = M.dot(boundingBoxTR)
    newBoundingBoxBL = M.dot(boundingBoxBL)
    newBoundingBoxBR = M.dot(boundingBoxBR)

    # make list for more readable code
    xValues = [newBoundingBoxTL[0], newBoundingBoxTR[0],
               newBoundingBoxBL[0], newBoundingBoxBR[0], ]

    yValues = [newBoundingBoxTL[1], newBoundingBoxTR[1],
               newBoundingBoxBL[1], newBoundingBoxBR[1], ]

    # calculate minimum and maximum values for new bounding box
    # NOTE this method of creating a new bounding box only works with resizing and translating
    # rotations and sheering can result in bounding boxes that are to big
    # fixing this would recuire having a label for every pixel, whether this is the object or background
    top = height
    bottom = 0
    left = width
    right = 0

    for x in xValues:
        if x < left:
            left = x
        if x > right:
            right = x

    for y in yValues:
        if y < top:
            top = y
        if y > bottom:
            bottom = y

    # reconstruct new bounding box

    return [(left + right) / 2, (top + bottom) / 2, right - left, bottom - top]


def stretch_img_random(img, boundingBox=None):
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

    if boundingBox != None:
        return output, get_new_boundingBox(boundingBox, M, width, height)

    return output


def shear_img_random(img, boundingBox=None):
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

    if boundingBox != None:
        return output, get_new_boundingBox(boundingBox, M, width, height)

    return output


def zoom_image_random(img, boundingBox=None):
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

    if boundingBox != None:
        return output, get_new_boundingBox(boundingBox, M, width, height)

    return output

def flip_image_random(img, boundingBox=None):
    '''
        function that flips the image randomly
        input: image (Mat object)
        output: flipped image (Mat object)
    '''
    randomNumber = random.randint(-2, 1)

    output = cv2.flip(img, randomNumber)

    if boundingBox != None:
        # flip the bounding box
        # get bouding box by creating a binary image
        # then setting the bounding box into the binary image
        # then flip the binary image
        # then get the bounding box from the binary image

        # create binary image
        binaryImage = np.zeros(img.shape[:2], np.uint8)

        # set bounding box

        x = int(boundingBox[0])
        y = int(boundingBox[1])
        w = int(boundingBox[2])
        h = int(boundingBox[3])

        # print(x, y, w, h)
        # print('-------------------------') 
        cv2.rectangle(binaryImage, (x, y), (x+w, y+h), 255, 0)

        # cv2.imshow('binaryImage', binaryImage)
        
        # flip the binary image
        binaryImage = cv2.flip(binaryImage, randomNumber)

        # cv2.imshow('binaryImageFlipped', binaryImage)

        # get the bounding box from the binary image
        [x, y, w, h] = cv2.boundingRect(binaryImage)

        # return the flipped image and the new bounding box
        return output, [x, y, w, h]



    return output



def rotate_image_random(img, boundingBox=None):
    '''
        function that rotates the image randomly
        input: image (Mat object)
        output: rotated image (Mat object)
    '''
    # height, width = img.shape[:2]

    # rotateAngle = random.randint(0, 3) * math.pi / 2

    # v1 = [math.cos(rotateAngle), math.sin(rotateAngle), 0]
    # v2 = [-math.sin(rotateAngle), math.cos(rotateAngle), 0]

    # M = np.matmul(np.float32(
    #     [[1, 0, width / 2], [0, 1, height / 2], [0, 0, 1]]), np.float32([v1, v2, [0, 0, 1]]))
    # M = np.matmul(M, np.float32(
    #     [[1, 0, -width / 2], [0, 1, -height / 2], [0, 0, 1]]))

    # output = cv2.warpAffine(img, M[:2], (width, height))

    # if boundingBox != None:
    #     return output, get_new_boundingBox(boundingBox, M, width, height)

    randomNumber = random.randint(0, 3)

    if(randomNumber == 3): # no rotation
        if boundingBox != None: # if there is a bounding box
            return img, boundingBox # return the image and the bounding box
        else: # if there is no bounding box
            return img # return the image
    
    output = cv2.rotate(img, randomNumber)

    if boundingBox != None:
        # rotate the bounding box
        # get bouding box by creating a binary image
        # then setting the bounding box into the binary image
        # then rotate the binary image
        # then get the bounding box from the binary image

        # create binary image
        binaryImage = np.zeros(img.shape[:2], np.uint8)

        # set bounding box

        x = int(boundingBox[0])
        y = int(boundingBox[1])
        w = int(boundingBox[2])
        h = int(boundingBox[3])

        # print(x, y, w, h)
        # print('-------------------------') 
        cv2.rectangle(binaryImage, (x, y), (x+w, y+h), 255, 0)

        # cv2.imshow('binaryImage', binaryImage)
        
        # flip the binary image
        binaryImage = cv2.rotate(binaryImage, randomNumber)

        # cv2.imshow('binaryImageFlipped', binaryImage)

        # get the bounding box from the binary image
        [x, y, w, h] = cv2.boundingRect(binaryImage)

        # return the flipped image and the new bounding box
        return output, [x, y, w, h]


    return output


def translate_image_random(img, boundingBox=None):
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

    if boundingBox != None:
        return output, get_new_boundingBox(boundingBox, M, width, height)

    return output

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
    canny = cv2.Canny(blur, 0, 175)
    # convert back to bgr
    canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    # add canny image to the original image
    output = cv2.addWeighted(img, 0.9, canny, 0.9, 0)
    return output


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


def augment_images(directory):
    '''
        function that augments the images in the directory
        input:  directory (string)
        output: augmented images (list of images)
    '''
    # get all images in the directory
    images = os.listdir(directory)

    # get the amount of images in the directory without counting the .txt files
    amount = 0
    for image in images:
        if image.endswith(".png") and not '_ignore' in image:
            amount += 1

    target = 1000

    while amount < target:
        # loop over all images in the directory
        for image in images:
            # if image includes '_ignore' or .txt skip it
            if '_ignore' in image or '.txt' in image:
                continue
            # read the image
            img = cv2.imread(os.path.join(directory, image))
            # read the label file
            labelOrg = open(os.path.join(directory, image[:-4] + '.txt'), 'r')
            # read the label
            labelOrg = labelOrg.read()
            # split the label
            labelOrg = labelOrg.split(' ')
            # convert item 1234 to float but keep the first item a string
            labelOrg = [labelOrg[0]] + [float(i) for i in labelOrg[1:]]


            xc = float(labelOrg[1])
            yc = float(labelOrg[2])
            w = float(labelOrg[3])
            h = float(labelOrg[4])

            # print(xc, yc, w, h)

            # decenter the bounding box
            '''The last thing we do in the labelfile generation is to de-center the bounding box.'''
            x = xc - (w/2)
            y = yc - (h/2)

            # print(x, y, w, h)

            # de normalize the bounding box
            '''The last thing we do in get_bounding_box (labelfilegenerator) is dnormalize the bounding box.'''	
            x = int(x * img.shape[1])
            y = int(y * img.shape[0])
            w = int(w * img.shape[1])
            h = int(h * img.shape[0])

            # print(x, y, w, h)
            # print('-------------------------') 
            # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 20)

            # execute the functions
            # [img, label] = stretch_img_random(
            #     img, [x, y, w, h]) # turned off because it is gives to much transformation
            [img, label] = shear_img_random(img,  [x, y, w, h])
            [img, label] = zoom_image_random(img, label)
            [img, label] = flip_image_random(img, label)  
            # [img, label] = rotate_image_random(img, label)   # turned off because it rotates the image witch could change the aspect ratio
            [img, label] = translate_image_random(img, label)  
            img = higher_contrast_random(img)
            img = change_brightness_random(img)
            img = rotate_hsv_random(img)
            img = canny_edge(img)
            img = add_noise_random(img)

            # draw bounding box from label on image
            x = int(label[0])
            y = int(label[1])
            w = int(label[2])
            h = int(label[3])


            # #### SHOW IMAGE ####
            # img2 = img.copy()	
            # cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 8)
            # cv2.imshow('image', img2)
            # cv2.waitKey(1)

            # if cv2.waitKey(0) & 0xFF == ord('q'):
            #     sys.exit()
            # continue


            # normalize the label
            x = x/ img.shape[1]  
            y = y/ img.shape[0]
            w = w/ img.shape[1]
            h = h/ img.shape[0]


            # save the image
            currentEpochTime = int(round(time.time() * 1000))
            safeDir = os.path.join(
                directory, image[:-4] + '_aug_' + str(currentEpochTime))
            cv2.imwrite(safeDir + '.png', img)
            # save the label
            labelFile = open(safeDir + '.txt', 'w')
            labelFile.write(str(labelOrg[0]) + ' ' + str(x) + ' ' +
                            str(y) + ' ' + str(w) + ' ' +
                            str(h))
            labelFile.close()

            amount += 1

            # print percentage
            print(directory + ' - percentage: ' + str(amount/target*100) + '%')

            if amount >= target:
                # break forloop and while loop
                break


if __name__ == '__main__':

    root_dir = os.path.join("blok2", "conveyerAcquisition", "datasets")
    bag_dir = os.path.join(root_dir, "bag")
    bottle_dir = os.path.join(root_dir, "bottle")
    bottlecap_dir = os.path.join(root_dir, "bottlecap")
    fork_dir = os.path.join(root_dir, "fork")
    knife_dir = os.path.join(root_dir, "knife")
    pen_dir = os.path.join(root_dir, "pen")
    spoon_dir = os.path.join(root_dir, "spoon")
    styrofoam_dir = os.path.join(root_dir, "styrofoam")

    augment_images(bag_dir)
    augment_images(bottle_dir)
    augment_images(bottlecap_dir)
    augment_images(fork_dir)
    augment_images(knife_dir)
    augment_images(pen_dir)
    augment_images(spoon_dir)
    augment_images(styrofoam_dir)

