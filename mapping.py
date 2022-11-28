import time

import controlmodule as cm
from djitellopy import tello
from time import sleep
import cv2
import numpy as np
import math


cm.init()
drone = tello.Tello()
drone.connect()
global img
#  --- parameters ---
fSpeed = 15  # forward speed in cm/s (117/10 cm/s)
aSpeed = 36  # angular speed in degree/s (360/10)
interval = 0.25  # 1/4 second

dInterval = fSpeed * interval
aInterval = aSpeed * interval
# --------------------
x, y = 500, 500
a = 0  # angle
yaw = 0

# line of movement
points = []
print("power level : ", drone.get_battery(), " % ")

drone.takeoff()


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    forwardSpeed = 15
    angularSpeed =50   # 22.5 so when it double will be 45 degree rotation
    d = 0  # distance
    global x, y, yaw, a
    #   if cm.getkey("8") : speed = +10
    #   elif cm.getkey("2"): speed =  -10

    #   if cm.getkey("6") : angularSpeed = +10
    #   elif cm.getkey("4"): angularSpeed =  -10

    # moving controls
    if cm.getkey("LEFT"):
        # move
        lr = -forwardSpeed
        # map
        d = dInterval
        a = -180

    elif cm.getkey("RIGHT"):
        lr = forwardSpeed
        d = -dInterval
        a = 180

    if cm.getkey("UP"):
        fb = forwardSpeed
        d = dInterval
        a = 270

    elif cm.getkey("DOWN"):
        fb = -forwardSpeed
        d = -dInterval
        a = -90

    if cm.getkey("w"):
        ud = forwardSpeed
    elif cm.getkey("s"):
        ud = -forwardSpeed

    if cm.getkey("a"):
        yv = angularSpeed
        yaw -= aInterval
    elif cm.getkey("d"):
        yv = -angularSpeed
        yaw += aInterval

    if cm.getkey("l"): drone.land()
    if cm.getkey("t"): drone.takeoff()

    if cm.getkey("b"): drone.flip_forward()
    sleep(interval)  # to
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))
    return [lr, fb, ud, yv]


def drawPoints():
    for point in points:
        cv2.circle(blackImage, point, 5, (0, 0, 255), cv2.FILLED)  # img , center, radius , color , thickness

    cv2.circle(blackImage, (x,y),8, (0, 255, 0), cv2.FILLED)
    cv2.putText(blackImage, f'({(x - 500)/ 100},{(y - 500)/ 100})m', (x + 10, y + 30),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),1)


while True:
    # moves
    values = getKeyboardInput()
    print(values[0], values[1], values[2], values[3])
    drone.send_rc_control(values[0], values[1], values[2], values[3])
    # image maping
    blackImage = np.zeros((1000, 1000, 3))
    points.append((x, y))
    drawPoints()
    cv2.imshow("map", blackImage)
    cv2.waitKey(1)
