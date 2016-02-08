import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
servoPin1=11
servoPin2=18
GPIO.setup(servoPin1, servoPin2, GPIO.OUT)
pwm1=GPIO.PWM(servoPin1,50)
pwm2=GPIO.PWM(servoPin2,50)
pwm1.start(6)
pwm2.start(6)
currentPosition1 = 90
currentPosition2 = 90
time_to_move = 3
for i in range (0,180):
    desiredPosition1=input("Pan servo position in degrees? 0-180 ")
    for i in range (0, time_to_move):
        while currentPosition1 < desiredPosition1:
            currentPosition1 = currentPosition1 + 1
            time.sleep(0.016)
            DutyCycle1 = 1./18.*(currentPosition1)+1
            pwm1.ChangeDutyCycle(DutyCycle1)
            
        while currentPosition1 > desiredPosition1:
            currentPosition1 = currentPosition1 - 1
            time.sleep(0.016)
            DutyCycle1 = 1./18.*(currentPosition1)+1
            pwm1.ChangeDutyCycle(DutyCycle1)
            
        else:
            currentPosition1 = currentPosition1

for i in range (0,180):
    desiredPosition2=input("Tilt servo position in degrees? 0-180 ")
    for i in range (0, time_to_move):
        while currentPosition2 < desiredPosition2:
            currentPosition2 = currentPosition2 + 1
            time.sleep(0.016)
            DutyCycle2 = 1./18.*(currentPosition2)+1
            pwm2.ChangeDutyCycle(DutyCycle2)
            
        while currentPosition2 > desiredPosition2:
            currentPosition2 = currentPosition2 - 1
            time.sleep(0.016)
            DutyCycle2 = 1./18.*(currentPosition2)+1
            pwm2.ChangeDutyCycle(DutyCycle2)
            
        else:
            currentPosition2 = currentPosition2

pwm.stop()
GPIO.cleanup()









