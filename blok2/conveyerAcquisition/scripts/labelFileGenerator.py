'''
  Label file generator for the conveyer acquisition system.
  This script generates label files for every image in the dataset.
  The label files are generated in the same directory as the images.
  The label files are named the same as the image files, but with the extension .txt.
  The label files contain the class label and the bounding box coordinates.
  The bounding box coordinates are normalized to the range [0, 1].
  The class labels are:
    # 0: Ignore
    1: Bag
    2: Bottle
    3: Bottlecap
    4: Fork
    5: Knife  
    6: Pen
    7: Spoon 
    8: Styrofoam
'''
# imports
import os
import cv2
import numpy as np


def remove_background(src):
    '''
    Remove the background from the image.

    Arguments: 
        {Mat} src: The source image. 
    Returns:
        {Mat} The image with the background removed.
    '''

    src = src.copy()




    # # remove background from the image
    # src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # dst = src.copy()
    # kernel = np.ones((3,3), np.uint8)
    # dst = cv2.erode(dst, kernel, iterations=1)
    # dst = cv2.dilate(dst, kernel, iterations=1)

    # # subtract dst from src
    # src = cv2.subtract(src, dst)

    # # src = cv2.absdiff(src, background)

    # # # normalize histogram
    # src = cv2.equalizeHist(src)

    # # threshold the image
    # # ret, src = cv2.threshold(src,5 , 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # return src
    #######################################################    
    

    # find first whiteish line
    for i in range(src.shape[0]):	
        if np.sum(src[i, :, :]) > 255 * 3 * 100:
            break

    # remove line and everything above it
    src[:i+30, :, :] = 0

    # find last whiteish line
    for i in range(src.shape[0] - 1, 0, -1):
        if np.sum(src[i, :, :]) > 255 * 3 * 100:
            break 

    # remove line and everything below
    src[i-30:, :, :] = 0

    # small gaussian blur
    # src = cv2.GaussianBlur(src, (3,3), 0)

    # simplefy image to 8bit colors
    src = cv2.convertScaleAbs(src, alpha=0.03)
    

    # add laplacian filter
    src = cv2.Laplacian(src, cv2.CV_8U)

    # histogram equalization
    src = cv2.cvtColor(src, cv2.COLOR_BGR2YUV)
    src[:, :, 0] = cv2.equalizeHist(src[:, :, 0])
    src = cv2.cvtColor(src, cv2.COLOR_YUV2BGR)


    # add gaussian blur
    src = cv2.GaussianBlur(src, (3,3), 0)
    

    return src



def get_bounding_box(org):
    '''
    Get the bounding box of the object in the image.

    Arguments:
        {Mat} src: The source image.
    Returns:
        Output: {int[]} - The bounding box coordinates.   
    '''

    # #  erode src 
    # kernel = np.ones((3,3), np.uint8)
    # src = cv2.dilate(src, kernel, iterations=1)
    # src = cv2.dilate(src, kernel, iterations=1)

    # cv2.imshow('src', src)




    # # connect all the white pixels together
    # kernel = np.ones((3,3), np.uint8)
    # src = cv2.dilate(src, kernel, iterations=5)
    # src = cv2.erode(src, kernel, iterations=5)


    # #  equalize black and white image histogram
    # src = cv2.equalizeHist(src)

    # cv2.imshow('src', src)


    # # find contours
    # contours, hierarchy = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # # find the biggest contour
    # max_area = 0
    # max_contour = None
    # for contour in contours:
    #     area = cv2.contourArea(contour)
    #     if area > max_area:
    #         max_area = area
    #         max_contour = contour

    # # get bounding box
    # x, y, w, h = cv2.boundingRect(max_contour)

    # # return bounding box
    # return [x, y, w, h]

    src = org.copy()
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)



    # find the contours in the image
    contours, hierarchy = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find the biggest contour
    max_area = 0
    max_cnt = None
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_cnt = cnt

    # get the bounding box of the biggest contour + some padding
    x, y, w, h = cv2.boundingRect(max_cnt)
    # add 50px padding
    x -= 50
    y -= 50
    w += 50
    h += 50


    # draw the bounding box on org without changing org
    org2 = org.copy()
    cv2.rectangle(org2, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('CALCULATED BOUNDING BOX', org2)

    # ask user to confirm the bounding box 
    while True:
        print('Is the bounding box correct? (y/n/q)')
        key = cv2.waitKey(0)
        if key == ord('y'):
            break
        elif key == ord('q'):
            exit()
        elif key == ord('n'):
            # get new bounding box
            x, y, w, h = cv2.selectROI(org)
            cv2.rectangle(org, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow('COMFIRM', org)
            break



    cv2.destroyAllWindows()
    # return the bounding box
    return [x, y, w, h]

def generateLabelFile(images, dir):
    '''
    Generate the labelfile with the images in the given directory.

    Arguments:
        {string[]} images: The images.
        {string} dir: The directory.
    Returns:
        Output: void
    '''

    for image in images:
        # clear previous frames and console
        os.system('cls' if os.name == 'nt' else 'clear')
        cv2.destroyAllWindows()

        # if image includes '_ignore' skip it
        if '_ignore' in image:
            continue

        img = cv2.imread(os.path.join(dir, image))
        cv2.imshow("org", img)
        WB = remove_background(img)
        x, y, w, h = get_bounding_box(WB)


        x = cv2.waitKey(0)
        if x == ord("q"):
            break

        # now write label file
        with open(os.path.join(bag_dir, image.replace('.jpg', '.txt')), 'w') as f:
            f.write('1 {} {} {} {}'.format(x+w/2, y+h/2, w, h))




if __name__ == "__main__":
    # dataset image directories
    root_dir = os.path.join("blok2", "conveyerAcquisition", "datasets")
    bag_dir = os.path.join(root_dir, "bag")
    bottle_dir = os.path.join(root_dir, "bottle")
    bottlecap_dir = os.path.join(root_dir, "bottlecap")
    fork_dir = os.path.join(root_dir, "fork")
    knife_dir = os.path.join(root_dir, "knife")
    pen_dir = os.path.join(root_dir, "pen")
    spoon_dir = os.path.join(root_dir, "spoon")
    styrofoam_dir = os.path.join(root_dir, "styrofoam")


    # get all images in the dataset
    bag_images = os.listdir(bag_dir)
    bottle_images = os.listdir(bottle_dir)
    bottlecap_images = os.listdir(bottlecap_dir)
    fork_images = os.listdir(fork_dir)
    knife_images = os.listdir(knife_dir)    
    pen_images = os.listdir(pen_dir)
    spoon_images = os.listdir(spoon_dir)
    styrofoam_images = os.listdir(styrofoam_dir)

    # generate label files
    generateLabelFile(bag_images, bag_dir)
    generateLabelFile(bottle_images, bottle_dir)
    generateLabelFile(bottlecap_images, bottlecap_dir)
    generateLabelFile(fork_images, fork_dir)
    generateLabelFile(knife_images, knife_dir)
    generateLabelFile(pen_images, pen_dir)
    generateLabelFile(spoon_images, spoon_dir)
    generateLabelFile(styrofoam_images, styrofoam_dir)
    
    
