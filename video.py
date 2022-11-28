import time

import controlmodule as cm
from djitellopy import tello
from time import sleep
import cv2
import numpy as np

#cm.init()

drone = tello.Tello()
drone.connect()
drone.streamon()

global img
print("power level : ", drone.get_battery(), " % ")


while True:
    # camera
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("image", img)
    sleep(1)
