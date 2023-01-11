import threading
import time
import sys
import os

from webserver import run_server
from dao.classifications import Classifications

# hacky way to import from parent directory
sys.path.insert(0, os.path.join(
    "blok2", "conveyerAcquisition", "JetsonYolo-main"))
# from JetsonYolo import yoloRun
from JetsonYoloUeye import yoloRun


dao = Classifications()

def callback(img, results):
    dao.insert(results)
    dao.save_image(img)

def startWebServer():
    time.sleep(10)
    run_server()

# create a new thread for the webserver
webserverThread = threading.Thread(target= startWebServer)
webserverThread.start()


# import the rest of the modules
yoloRun(callback, weights=os.path.join(
    "blok2", "conveyerAcquisition", "JetsonYolo-main", 'Transferlearn.pt'))
