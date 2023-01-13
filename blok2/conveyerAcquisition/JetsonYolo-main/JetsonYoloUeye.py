import cv2
import numpy as np
from ueyeCustom import initialize_ueye_cam, get_ueye_image, close_ueye_camera
from elements.yolo import OBJ_DETECTION
import threading

def yoloRun(callback, weights='Transferlearn.pt' ):
    Object_classes = ['ignore','Bag', 'Bottle', 'Bottlecap', 'Fork', 'Knife', 'Pen', 'Spoon', 'Styrofoam']

    Object_colors = list(np.random.rand(80,3)*255)
    Object_detector = OBJ_DETECTION(weights, Object_classes)

    # get camera
    hcam, mem_ptr, width, height, bitspixel, lineinc = initialize_ueye_cam()
    

    window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
    # Window
    while cv2.getWindowProperty("CSI Camera", 0) >= 0:

        threading.Thread(target=classify, args=(Object_detector, callback, mem_ptr, width, height, bitspixel, lineinc)).start()

        # cv2.imshow("CSI Camera", frame)
        keyCode = cv2.waitKey(250)
        if keyCode == ord('q'):
            break

    close_ueye_camera(hcam)
    cv2.destroyAllWindows()

def classify(Object_detector, callback, mem_ptr, width, height, bitspixel, lineinc):
    frame = get_ueye_image(mem_ptr, width, height, bitspixel, lineinc)
    changePercentage= 100

    
    returnObjects = []


    # detection process
    objs = Object_detector.detect(frame)

    # plotting
    for obj in objs:
        # print(obj)
        label = obj['label']
        score = obj['score']
        # [(xmin,ymin),(xmax,ymax)] = obj['bbox']
        # color = Object_colors[Object_classes.index(label)]
        # frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2) 
        # frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, color, 1, cv2.LINE_AA)
        # create new object with: class and confidence
        returnObjects.append({'class': label, 'confidence': str(score)})

    # call callback function
    if callback is not None:
        if len(returnObjects) == 0:
            returnObjects.append({'class': 'ignore', 'confidence': str(changePercentage/100)})
        callback(frame, returnObjects)


if __name__ == "__main__":
    yoloRun(None)