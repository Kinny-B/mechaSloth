import time
import RPi.GPIO as GPIO
# Motor Control
distance = 0
direction = ""

# motors
MOTOR_PINS = {'IN1': 17, 'IN2': 18, 'IN3': 22, 'IN4': 23}
MOVE_DURATION = 2  # Seconds for movement actions
# parse response for movement
def move(response):
    print("\nseeking path to move...\n")
    if any(cmd in response for cmd in ["forward", "ahead", "move", "drive", "north"]):
        move_forward()
    elif any(cmd in response for cmd in ["backward", "behind", "reverse", "south"]):
        move_backward()
    elif any(cmd in response for cmd in ["left", "turn", "port", "west"]):
        turn_left()
    elif any(cmd in response for cmd in ["right", "starboard", "east"]):
        turn_right()
    else:
        stop_motors()
# move
def move_forward():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.LOW)
    time.sleep(MOVE_DURATION)
    stop_motors()
def move_backward():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.HIGH)
    time.sleep(MOVE_DURATION)
    stop_motors()
def turn_left():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.LOW)
    time.sleep(1)  # Shorter duration for turning
    stop_motors()
def turn_right():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.HIGH)
    time.sleep(1)
    stop_motors()
def stop_motors():
    for pin in MOTOR_PINS.values():
        GPIO.output(pin, GPIO.LOW)
#def test_motors():
#    setup_motors()
#    move_forward()
#    time.sleep(2)
#    turn_left()
#    time.sleep(1)
#    stop_motors()
