from djitellopy import tello
from time import sleep
drone=tello.Tello()
drone.connect()
# display drone battery
print("power level : ",drone.get_battery()," % ")
drone.takeoff()
#drone.send_rc_control()
drone.land()

