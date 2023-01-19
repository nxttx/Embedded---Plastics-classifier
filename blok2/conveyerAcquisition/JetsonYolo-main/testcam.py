import cv2
import ueyeCustom as cam
hcam, mem_ptr, width, height, bitspixel, lineinc = cam.initialize_ueye_cam()

print("Cam is opend:")
while cv2.waitKey(1) != 27:

    print('reading frame')

    frame = cam.get_ueye_image(mem_ptr, width, height, bitspixel, lineinc)

    if frame is None:
        print('No frame')
        continue

    # frame = np.rot90(frame,3)

    cv2.imshow("Frame", frame)

cam.close_ueye_camera(hcam)