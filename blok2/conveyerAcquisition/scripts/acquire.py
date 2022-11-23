import cv2
import os
import time

cam = cv2.VideoCapture(0)

data_path = os.path.join("blok2", "conveyerAcquisition", "datasets")
mappings = {"i": "ignore",
            "k": "knife",
            "s": "spoon",
            "f": "fork",
            "b": "bottle",
            "a": "bag",
            "y": "syrofoam",
            "c": "bottlecap",
            "p": "pen"}


kMappings = {}
for key in mappings.keys():
    kMappings[ord(key)] = mappings[key]

print(mappings)

img = cv2.imread(os.path.join("blok2", "conveyerAcquisition",
                 "scripts", "keyboard_layout.png"))
cv2.imshow("keyboard layout", img)

time.sleep(1.0)

while True:
    # grab the frame from the threaded video file stream
    ret, frame = cam.read()

    if frame is None:
        continue

    # frame = np.rot90(frame,3)

    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1) & 0xFF

    # if the `q` key or ESC was pressed, break from the loop
    if k == ord("q") or k == 27:
        break
    # otherwise, check to see if a key was pressed that we are
    # interested in capturing
    elif k in kMappings.keys():
        # construct the path to the label subdirectory
        p = os.path.sep.join([data_path, kMappings[k]])
        if not os.path.exists(p):
            os.makedirs(p)
        # construct the path to the output image
        p = os.path.sep.join([p, "{}.png".format(int(time.time_ns()))])
        print("[INFO] saving frame: {}".format(p))
        cv2.imwrite(p, frame)
