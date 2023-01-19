import cv2
import numpy as np
from elements.yolo import OBJ_DETECTION


def yoloRun(callback, weights='Transferlearn.pt' ):
    Object_classes = ['ignore','Bag', 'Bottle', 'Bottlecap', 'Fork', 'Knife', 'Pen', 'Spoon', 'Styrofoam']

    Object_colors = [(0,0,0), (0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,255), (255,255,0), (255,255,255), (128,128,128)]
    Object_detector = OBJ_DETECTION(weights, Object_classes)

    prevousFrame = None
    objs = None

    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)        

        # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret, frame = cap.read()

            # remove 25% of the left side of the image
            frame = frame[:, int(frame.shape[1]*0.25):]
            # remove 25% of the right side of the image
            frame = frame[:, :int(frame.shape[1]*0.75)]
            # remove 25% of the top side of the image
            frame = frame[int(frame.shape[0]*0.10):, :]
            # remove 25% of the bottom side of the image
            frame = frame[:int(frame.shape[0]*0.60), :]

            changePercentage= 100
            if prevousFrame is not None:
                changePercentage = cv2.absdiff(prevousFrame, frame)
                changePercentage = changePercentage.astype(np.uint8)
                changePercentage = (np.count_nonzero(changePercentage) * 100)/ changePercentage.size

            returnObjects = []

            if ret and changePercentage > 80: # turned off temporary 
                # detection process
                objs = Object_detector.detect(frame)
                prevousFrame = frame



            # plotting the results
            for obj in objs:
                # print(obj)
                label = obj['label']
                score = obj['score']
                [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                color = Object_colors[Object_classes.index(label)]
                frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2) 
                frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, color, 1, cv2.LINE_AA)
                # create new object with: class and confidence
                returnObjects.append({'class': label, 'confidence': str(score)})

            
            # call callback function
            if callback is not None:
                if len(returnObjects) == 0:
                    returnObjects.append({'class': 'ignore', 'confidence': str(changePercentage/100)})
                callback(frame, returnObjects)

            cv2.imshow("CSI Camera", frame)

            keyCode = cv2.waitKey(30)
            if keyCode == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    yoloRun(None)