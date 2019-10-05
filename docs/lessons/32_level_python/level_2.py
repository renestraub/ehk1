from microbit import *
import time
import math

calibration = 0.0

while True:
    # Get acceleration in x and y axis, then compute
    # angle micro:bit has (0 = level).
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    angle = math.atan2(x,y) / math.pi * 180    
    
    if button_a.is_pressed():
        display.show(Image.ARROW_S)
        calibration = angle
    else:
        angle = angle - calibration

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
