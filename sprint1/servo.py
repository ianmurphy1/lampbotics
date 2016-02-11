import RPi.GPIO as GPIO
import time

START_POSITION = 90


class Servo:

    def __init__(self, channel, freq):
        self.channel = channel
        self.freq = freq
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.channel, GPIO.OUT)
        self.current_position = 0
        self.time_to_move = 3
        self.pwm = GPIO.PWM(self.channel, self.freq)

    def __call__(self, *args, **kwargs):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.channel, GPIO.OUT)
        self.current_position = 0
        self.time_to_move = 3
        self.pwm = GPIO.PWM(self.channel, self.freq)

    def setup_servo(self):
        self.pwm.start(6)
        self.move_servo(START_POSITION)

    def move_servo(self, degrees):
        print "Moving servo to " + str(degrees)
        for i in range(0, 180):
            desired_position1 = degrees
            for j in range(0, self.time_to_move):
                while self.current_position < desired_position1:
                    self.current_position = self.current_position + 1
                    time.sleep(0.016)
                    DutyCycle1 = 1. / 18. * (self.current_position) + 1
                    self.pwm.ChangeDutyCycle(DutyCycle1)

                while self.current_position > desired_position1:
                    self.current_position = self.current_position - 1
                    time.sleep(0.016)
                    DutyCycle1 = 1. / 18. * (self.current_position) + 1
                    self.pwm.ChangeDutyCycle(DutyCycle1)

                else:
                    self.current_position = desired_position1

