from multiprocessing import Pool
import time
import sys
import os
from LEDcontroller import turnLedOnBasedOnItem 
from jetsonGPIO import setup, input

from webserver import run_server
from dao.classifications import Classifications

# hacky way to import from parent directory
sys.path.insert(0, os.path.join(
    'repositories', 'Embedded---Plastics-classifier',
    "blok2", "conveyerAcquisition", "JetsonYolo-main"))
# from JetsonYolo import yoloRun
from JetsonYoloUeye import yoloRun


dao = Classifications()

def callback(img, results):
    if (webserverOn):
        # get result with highest confidence
        result = max(results, key=lambda x: x['confidence'])
        # turn led on based on result
        turnLedOnBasedOnItem(result['class'])
        
    dao.insert(results)
    dao.save_image(img)


def startWebServer():
    time.sleep(10)
    run_server()

# check webserver switch
setup(37, 'in')
webserverOn = input(37)
if(webserverOn):
    # create a new multiprocess for the webserver
    webserverThread = Pool(1)
    webserverThread.apply_async(startWebServer)
    # webserverThread = threading.Thread(target= startWebServer)
    # webserverThread.start()


# import the rest of the modules
yoloRun(callback, weights=os.path.join(
    'repositories', 'Embedded---Plastics-classifier',
    "blok2", "conveyerAcquisition", "JetsonYolo-main", 'Transferlearn.pt'))
