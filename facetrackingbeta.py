import cv2
from time import sleep
import numpy as np
from djitellopy import Tello

import keyboardcontroler as kb

# static vars
TOLERANCE_X = 5
TOLERANCE_Y = 5
# SLOWDOWN_THRESHOLD = 20
SPEED = 15
SET_POINT_X = 360 / 2
SET_POINT_Y = 240 / 2

up_down = 0
right_left = 0
back_forward = 0

w, h = 360, 240
fbRange = [6600, 6800]
pid = [0.5, 0.5, 0]
perror = 0

drone = Tello()  # declaring drone object
drone.connect()
drone.streamon()
print(" battery :", drone.get_battery(), "%\n")

drone.takeoff()


# drone.move_up(20)



def findface(frame):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
    # it could be many faces in camera so we wil choose the biggest one
    myfacelistcenter = []
    myfacelistarea = []
    myfacelistdistance = []
    distanceX, distanceY = 0, 0

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)  # face
        centerx = x + w // 2
        centery = y + h // 2

        cv2.circle(frame, (centerx, centery), 5, (0, 255, 0), cv2.FILLED)  # face center

        cv2.circle(frame, (int(SET_POINT_X), int(SET_POINT_Y)), 12, (255, 255, 0), cv2.FILLED)  # center image point

        # left right , up and dawn
        distanceX = centerx - SET_POINT_X
        distanceY = centery - SET_POINT_Y
        # back and forward
        area = w * h
        # rotation

        myfacelistcenter.append([centerx, centery])
        myfacelistarea.append(area)
        myfacelistdistance.append([distanceX, distanceY])
    # if face found
    if len(myfacelistarea) != 0:
        # choose the big face
        i = myfacelistarea.index(max(myfacelistarea))
        return frame, [myfacelistcenter[i], myfacelistarea[i], myfacelistdistance[i]]
    else:
        return frame, [[0, 0], 0, [0, 0]]


def trackface(drone, info, w, pid, perror):
    global TOLERANCE_X, TOLERANCE_Y, SLOWDOWN_THRESHOLD, right_left, up_down

    distanceX = info[2][0]
    distanceY = info[2][1]

    area = info[1]

    x, y = info[0]

    fb = 0
    rotate = 0
    error = 0

    # left right track
    if distanceX < -TOLERANCE_X:
        right_left = - SPEED

    elif distanceX > TOLERANCE_X:
        right_left = SPEED
    else:
        right_left = 0
    # up dawn
    if distanceY < -TOLERANCE_Y:
        up_down = SPEED
    elif distanceY > TOLERANCE_Y:
        up_down = - SPEED
    else:
        up_down = 0
    # back and forward
    # if  in range or nothing detected  ( 0 )  it will not go forward
    if area > fbRange[0] and area < fbRange[1] or area == 0:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0]:
        fb = 20

    # rotation track
    if x != 0:
        error = x - w // 2  # width // 2 = is the real value where i anm cause it in center of width
        rotate = (pid[0] * error + pid[1] * (error - perror))
        rotate = int(np.clip(rotate, -100, 100))
    # if nothing detected  ( 0 )  it will not --for rotation
    if x == 0:
        rotate = 0
        error = 0

    # send command
    drone.send_rc_control(right_left, fb, up_down, rotate)
    return perror


def camreciver(drone):
    frame = drone.get_frame_read().frame
    frame = cv2.resize(frame, (360, 240))
    return frame


while True:
    # move
    values = kb.getKeyboardInput()
    # if values[0] == 0 & values[1] == 0 & values[2] == 0 & values[3] == 0:
    #    pass
    ## do nothing
    # else:
    # drone.send_rc_control(values[0], values[1], values[2], values[3])
    # camera detection
    frame = camreciver(drone)
    frame, info = findface(frame)
    perror = trackface(drone, info, w, pid, perror)
    cv2.imshow('Video', frame)
    # quit
    if cv2.waitKey(1) & 0xFF == ord('q'):  # quit from script
        break
drone.land()
cv2.destroyAllWindows()
