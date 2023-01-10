import cv2
cam = cv2.VideoCapture(0)
print("Cam is opend:" + str(cam.isOpened()))
while cv2.waitKey(1) != 27:
    print("Cam is opend:" + str(cam.isOpened()))

    print('reading frame')

    ret, frame = cam.read()

    if frame is None:
        print('No frame')
        continue

    # frame = np.rot90(frame,3)

    cv2.imshow("Frame", frame)