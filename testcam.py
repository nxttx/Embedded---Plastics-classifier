import cv2
cam = cv2.VideoCapture(0)

while cv2.waitKey(1) != 27:
    ret, frame = cam.read()

    if frame is None:
        continue

    # frame = np.rot90(frame,3)

    cv2.imshow("Frame", frame)