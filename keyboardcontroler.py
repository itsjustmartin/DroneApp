import time

import controlmodule as cm
from djitellopy import tello
from time import sleep
import cv2
import numpy as np

drone = tello.Tello()
drone.connect()
drone.streamon()

cm.init()

speed = 20


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    global speed  # to change the global var
    angularspeed = 22  # 22.5 so when it doubles will be 45-degree  but i cant use float

    if cm.getkey("8"):
        speed = +10
    elif cm.getkey("2"):
        speed = -10

    if cm.getkey("6"):
        angularspeed = +10
    elif cm.getkey("4"):
        angularspeed = -10

    # moving controls
    if cm.getkey("LEFT"):
        lr = -speed
    elif cm.getkey("RIGHT"):
        lr = speed

    if cm.getkey("UP"):
        fb = speed
    elif cm.getkey("DOWN"):
        fb = -speed

    if cm.getkey("w"):
        ud = speed
    elif cm.getkey("s"):
        ud = -speed

    if cm.getkey("a"):
        yv = angularspeed
    elif cm.getkey("d"):
        yv = -angularspeed

    if cm.getkey("l"):
        drone.land()
    if cm.getkey("t"):
        drone.takeoff()

    if cm.getkey("b"):
        drone.flip_forward()

    # capture image
    if cm.getkey("c"):
        cv2.imwrite(f"Resources/Images/{time.time()}.jpg", img)
        time.sleep(0.3)  # so il will not take alot of pics

    return [lr, fb, ud, yv]


if __name__ == '__main__':

    print("power level : ", drone.get_battery(), " % 'controler' ")
    # drone.takeoff()

    while True:
        # moves
        values = getKeyboardInput()
        print(values[0], values[1], values[2], values[3])

        # if values[0] == 0 & values[1] == 0 & values[2] == 0 & values[3] == 0:
        # print("------")
        # else:  #its causing errors idk
        drone.send_rc_control(values[0], values[1], values[2], values[3])
        # camera
        img = drone.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imshow("image", img)
        sleep(0.05)
