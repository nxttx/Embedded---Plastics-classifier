import ctypes
from pyueye import ueye
import numpy as np

def initialize_ueye_cam():
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

    return hcam, mem_ptr, width, height, bitspixel, lineinc

def get_ueye_image(mem_ptr, width, height, bitspixel, lineinc):
    img = ueye.get_data(mem_ptr, width, height,
                        bitspixel, lineinc, copy=True)
    img = np.reshape(img, (height, width, 3))
    return img

def close_ueye_camera(hcam):
    ret = ueye.is_StopLiveVideo(hcam, ueye.IS_FORCE_VIDEO_STOP)
    print(f"StopLiveVideo returns {ret}")
    ret = ueye.is_ExitCamera(hcam)
    print(f"ExitCamera returns {ret}")