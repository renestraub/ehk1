# Add your Python code here. E.g.
from microbit import *
import time
import math


while True:
    # Get acceleration in x and y axis, then compute
    # angle micro:bit has (0 = level).
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    angle = math.atan2(x,y) / math.pi * 180    
    
    # Limits angle to -2 .. +2 degrees
    limit = 2.0
    if angle > limit:
        angle = limit
    elif angle < -limit:
        angle = -limit

    # Show a pixel depending on micro:bit level
    pos = round(2.0 + angle * 1.0)
    display.clear()
    display.set_pixel(int(pos), 1, 9)

    time.sleep_ms(50)
