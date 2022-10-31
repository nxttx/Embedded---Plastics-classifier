# import model and predict with the camera
import cv2
import joblib
model = joblib.load('model.pkl')


# now import helpers
import sys
# get current path and remove the last folder
path = sys.path[0]
path = path[:-10]

sys.path.append(path + '\pre_processing')

from feature_extraction import extract_features
from removing_background import remove_background


cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (320, 240))
    binary_image = remove_background(frame)
    try:
        features = extract_features(binary_image)
    except:
        continue
    cv2.imshow("frame", frame)
    cv2.imshow("binary", binary_image)

    # now we have the features, we can predict
    prediction = model.predict([features])
    print(prediction)

    if cv2.waitKey(500) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()