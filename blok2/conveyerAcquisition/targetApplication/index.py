import threading
import time
import sys
import os

from webserver import run_server
from dao.classifications import Classifications

# hacky way to import from parent directory
sys.path.insert(0, os.path.join(
    "blok2", "conveyerAcquisition", "transferlearn", "yolov5"))
from custom_detect import run_custom


dao = Classifications()

def callback(img, results):
    dao.insert(results)
    dao.save_image(img)


# create a new thread for the webserver
webserverThread = threading.Thread(target=run_server)
webserverThread.start()

# wait for the webserver to start
time.sleep(1)

# import the rest of the modules
run_custom(os.path.join("blok2", "conveyerAcquisition", "transferlearn",
           "weigths_of_training", "weights", "best00.15.pt"), 0, callback)
