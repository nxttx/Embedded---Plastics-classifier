import ctypes
from pyueye import ueye
import numpy as np
import cv2
import os
import time


def main():
    # init camera
    hcam = ueye.HIDS(0)
    ret = ueye.is_InitCamera(hcam, None)
    print(f"initCamera returns {ret}")

    # set color mode
    ret = ueye.is_SetColorMode(hcam, ueye.IS_CM_BGR8_PACKED)
    print(f"SetColorMode IS_CM_BGR8_PACKED returns {ret}")

    # set region of interest
    width = 640
    height = 480
    rect_aoi = ueye.IS_RECT()
    rect_aoi.s32X = ueye.int(0)
    rect_aoi.s32Y = ueye.int(0)
    rect_aoi.s32Width = ueye.int(width)
    rect_aoi.s32Height = ueye.int(height)
    ueye.is_AOI(hcam, ueye.IS_SET_AUTO_WB_AOI, rect_aoi, ueye.sizeof(rect_aoi))
    print(f"AOI IS_AOI_IMAGE_SET_AOI returns {ret}")

    # allocate memory
    mem_ptr = ueye.c_mem_p()
    mem_id = ueye.int()
    bitspixel = 24  # for colormode = IS_CM_BGR8_PACKED
    ret = ueye.is_AllocImageMem(hcam, width, height, bitspixel,
                                mem_ptr, mem_id)
    print(f"AllocImageMem returns {ret}")

    # set active memory region
    ret = ueye.is_SetImageMem(hcam, mem_ptr, mem_id)
    print(f"SetImageMem returns {ret}")

    # continuous capture to memory
    ret = ueye.is_CaptureVideo(hcam, ueye.IS_DONT_WAIT)
    print(f"CaptureVideo returns {ret}")

    # try white balance
    ret = ueye.is_SetAutoParameter(
        hcam, ueye.IS_SET_ENABLE_AUTO_WHITEBALANCE, ctypes.c_double(1), ctypes.c_double(0))
    print(f"White balance {ret}")

    # get data from camera and display
    lineinc = width * int((bitspixel + 7) / 8)

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

    delayTime = 1.0 / 5  # 5 FPS

    lastTime = time.time()

    while True:
        img = ueye.get_data(mem_ptr, width, height,
                            bitspixel, lineinc, copy=True)
        img = np.reshape(img, (height, width, 3))
        cv2.imshow('uEye Python Example (q to exit)', img)

        k = cv2.waitKey(1) & 0xFF
        if k == ord("q") or k == 27:
            break
        elif k in kMappings.keys():
            # construct the path to the label subdirectory
            p = os.path.sep.join([data_path, kMappings[k]])
            if not os.path.exists(p):
                os.makedirs(p)
            # construct the path to the output image
            currentTime = time.time()
            p = os.path.sep.join([p, "{}.png".format(int(currentTime))])
            frameTime = currentTime - lastTime
            print("[INFO] saving frame: {}, with frame time of {}ms, {} FPS".format(
                p, frameTime, 1e9/frameTime))
            cv2.imwrite(p, img)

            lastTime = currentTime

            time.sleep(delayTime - frameTime / 1e6)

    cv2.destroyAllWindows()

    # cleanup
    ret = ueye.is_StopLiveVideo(hcam, ueye.IS_FORCE_VIDEO_STOP)
    print(f"StopLiveVideo returns {ret}")
    ret = ueye.is_ExitCamera(hcam)
    print(f"ExitCamera returns {ret}")


if __name__ == '__main__':
    main()
