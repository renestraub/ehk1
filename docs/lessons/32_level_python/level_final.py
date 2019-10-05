# Add your Python code here. E.g.
from microbit import *
import time
import math


calibration = 0.0
angles = list()


def get_angle():
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    angle = math.atan2(x,y) / math.pi * 180
    return angle


def smooth(pos, angle):
    dx = abs(pos - angle)
    if dx > 1.0:
        dx = 1.0
    display.set_pixel(pos+2, 2, 9-int(9*dx))


def show_level(angle):
    """
    Display a water bubble like indicator
    One dot moves in the middle row, depending on angle
    Range is +/-2 degree
    """
    limit = 2.0
    if angle > limit:
        angle = limit
    elif angle < -limit:
        angle = -limit

    pos = round(2.0 + angle * 1.0)
    display.clear()
    #for x in range(0,5):
    #    display.set_pixel(x, 2, 0)
    display.set_pixel(int(pos), 1, 9)
    for level in range(-2, 3):
        smooth(level, angle)
#    smooth(-2, angle)
#    smooth(-1, angle)
#    smooth(-0, angle)
#    smooth( 1, angle)
#    smooth( 2, angle)


# Main Loop
while True:
    angle = get_angle()
    angles.append(angle)
    if len(angles) > 10:
        del angles[0]
    avg = sum(angles)/len(angles)

    if button_a.is_pressed():
        display.show(Image.ARROW_S)
        calibration = avg
    else:
        show_level(avg - calibration)
        # display.scroll(str(int(avg - calibration)))

    time.sleep_ms(50)

