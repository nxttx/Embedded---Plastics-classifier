# import webserver module and open it on a new thread
from webserver import WebServer
import threading
import time

# create a new thread for the webserver
webserverThread = threading.Thread(target=WebServer)
webserverThread.start()

# wait for the webserver to start
time.sleep(1)

# import the rest of the modules
