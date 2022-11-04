'''
 Import model and predict with the camera
'''
import cv2
import joblib
model = joblib.load('model_joblib.pkl')

'''
 Import helpers
'''
import sys
# get current path and remove the last folder
path = sys.path[0]
path = path[:-10]

sys.path.append(path + '\pre_processing')

from feature_extraction import extract_features
from removing_background import remove_background


if __name__ == '__main__':
    # open video stream
    cap = cv2.VideoCapture(0)

    while True:
        # read frame
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (320, 240))
        # remove background
        binary_image = remove_background(frame)

        # show video and binary image
        cv2.imshow("frame", frame)
        cv2.imshow("binary", binary_image)

        try:
            # extract features
            features = extract_features(binary_image)
        except:
            # if no hand is detected
            continue

        # now we have the features, we can predict
        prediction = model.predict([features])
        print(prediction)

        # Check if the user wants to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close the video stream
    cap.release()
    # close all windows
    cv2.destroyAllWindows()