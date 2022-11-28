import time

import cv2
import numpy as np
from djitellopy import tello

# import movment control to work good
import controlmodule as cm
import keyboardcontroler as kb
speed = 20
cm.init()
global img

drone = tello.Tello()
drone.connect()
drone.streamon()

drone.takeoff()
# if it was on ground so will match human height
# drone.send_rc_control(0,0,20,0)
# time.sleep(2.2)

w, h = 360, 240

fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]

perror = 0


def findface(img):
    print("find face detection on ... ")
    faceCascade = cv2.CascadeClassifier(
        "Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    # it could be many faces in camera so we wil choose the biggest one
    myfacelistcenter = []
    myfacelistarea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        centerx = x + w // 2
        centery = y + h // 2
        area = w * h
        # print("area", area, "\n")
        cv2.circle(img, (centerx, centery), 5, (0, 255, 0), cv2.FILLED)
        myfacelistcenter.append([centerx, centery])
        myfacelistarea.append(area)
    if len(myfacelistarea) != 0:
        i = myfacelistarea.index(max(myfacelistarea))
        return img, [myfacelistcenter[i], myfacelistarea[i]]
    else:
        return img, [[0, 0], 0]


def trackface(drone, info, w, pid, perror):  # previus err
    area = info[1]
    x, y = info[0]

    fb = 0

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - perror)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    # if nothinf detected  ( 0 )  it will not go forward
    elif area < fbRange[0] and area != 0:
        fb = 20
    # if nothinf detected  ( 0 )  it will not go forward   --for rotation
    if x == 0:
        speed = 0
        error = 0

    drone.send_rc_control(0, fb, 0, speed)
    return error


while True:
    # move
    values = kb.getKeyboardInput()
    drone.send_rc_control(values[0], values[1], values[2], values[3])
    # camera detection
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    # print("find me")
    faceimg, info = findface(img)
    perror = trackface(drone, info, w, pid, perror)
    # center used for rotate and area for backword and forward
    print("Area :", info[1], "  center :", info[0])
    cv2.imshow("output", faceimg)

    if cv2.waitKey(1) & 0xff == ord('q'):  # if q key is pressed
        drone.land()
        break  # end while loop
