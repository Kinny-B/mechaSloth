# using drivers from adafruit-circuitpython-motorkit for ease of use with 'Adafruit Pi motorHAT'.
import time
import busio
from adafruit_motorkit import MotorKit
import board
# setup
i2c = busio.I2C(board.SCL, board.SDA)
kit = MotorKit(i2c=board.I2C())
MOVE_DURATION = 5
# parse response for movement
def move(response):
    print("\nseeking path to move...\n")
    if any(cmd in response for cmd in ["forward", "ahead", "north"]):
        move_forward()
    elif any(cmd in response for cmd in ["backward", "behind", "reverse", "south"]):
        move_backward()
    elif any(cmd in response for cmd in ["left", "turn", "port", "west"]):
        turn_left()
    elif any(cmd in response for cmd in ["right", "starboard", "east"]):
        turn_right()
    else:
        stop_motors()
# move functions
def stop_motors():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0
def move_forward():
    kit.motor1.throttle = -1
    kit.motor2.throttle = -1
    kit.motor3.throttle = -1
    kit.motor4.throttle = -1
    time.sleep(MOVE_DURATION)
    stop_motors()
def move_backward():
    kit.motor1.throttle = 1
    kit.motor2.throttle = 1
    kit.motor3.throttle = 1
    kit.motor4.throttle = 1
    time.sleep(MOVE_DURATION)
    stop_motors()
def turn_left():
    kit.motor1.throttle = 0.5
    kit.motor2.throttle = 0.5
    kit.motor3.throttle = -0.5
    kit.motor4.throttle = -0.5
    time.sleep(MOVE_DURATION)
    stop_motors()
def turn_right():
    kit.motor1.throttle = -0.5
    kit.motor2.throttle = -0.5
    kit.motor3.throttle = 0.5
    kit.motor4.throttle = 0.5
    time.sleep(MOVE_DURATION)
    stop_motors()