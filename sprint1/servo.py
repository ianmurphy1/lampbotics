import RPi.GPIO as GPIO

START_POSITION = 90


class Servo():
    def __init__(self, channel, freq):
        self.channel = channel
        self.freq = freq
        self.current_position = 0

    def setup_servo(self):
        GPIO.setup(self.channel, GPIO.OUT)
        GPIO.PWM(self.channel, self.freq)
        self.move_servo(START_POSITION)

    def move_servo(self, degrees):
        self.current_position = degrees

