from servo import *
from camera import Camera
from threading import Thread, Lock, Event
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import sys
import signal
import cv2
PAN_OFFSET = 0
TILT_OFFSET = 0

face_width = 0
face_height = 0
focal = 0

class Runner:
    def __init__(self):
        self.setup_servos()
        self.pan_servo = Servo(12, 50)
        self.tilt_servo = Servo(13, 50)
        self.camera = Camera()
        self.rawCapture = self.camera.rawCapture
        self.pan_event = Event()
        self.tilt_event = Event()
        self.lock = Lock()

    def detect(self):
        while True:
            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                grey = cv2.cvtColor(image, cv2.COLOR.BGR2GRAY)

                faces = self.camera.cascade.detectMultiScale(grey, 1.1, 5)
                global face_height, face_width
                for (x, y, z, w, h) in faces:
                    # cv2.rectangle(image(x, y), (x + y, y + h), (255, 0, 0), 2)
                    center_face_x = (w / 2) + x
                    center_face_y = (h / 2) + y

                    if center_face_x != self.pan_servo.current_position:
                        face_width = center_face_x
                        self.pan_event.set()
                    if center_face_y != self.tilt_servo.current_position:
                        face_height = center_face_y
                        self.pan_event.set()

                self.rawCapture.truncate(0)



    def pan_servo(self):
        while True:
            self.pan_event.wait()
            self.pan_event.clear()
            new_position = convert_for_pan(face_width)
            self.pan_servo.move_servo(new_position)

    def tilt_servo(self):
        while True:
            self.tilt_event.wait()
            self.tilt_event.clear()
            new_position = convert_for_pan(face_height)
            self.tilt_servo.move_servo(new_position)

    def run(self):
        t = Thread(target=self.pan_servo)
        t.daemon = True
        t.start()

        t = Thread(target=self.tilt_servo)
        t.daemon = True
        t.start()

        t = Thread(target=self.detect)
        t.daemon = True
        t.start()

        while True:
            pass


def convert_for_tilt(num):

def convert_for_pan(num):

