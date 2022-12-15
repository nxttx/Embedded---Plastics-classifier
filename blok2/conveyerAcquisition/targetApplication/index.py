# import webserver module and open it on a new thread
from webserver import WebServer
import threading
import time
import sys
import os
import cv2
# hacky way to import from parent directory
sys.path.insert(0, os.path.join("..", "transferlearn", "yolov5"))
from custom_detect import run_custom


def callback(img, results):
    cv2.imshow("img", img)
    print(results)


# create a new thread for the webserver
webserverThread = threading.Thread(target=WebServer)
webserverThread.start()

# wait for the webserver to start
time.sleep(1)

# import the rest of the modules
run_custom(os.path.join("blok2", "conveyerAcquisition", "transferlearn",
           "weigths_of_training", "weights", "best00.15.pt"), 0, callback)
