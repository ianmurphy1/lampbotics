from servo import *
from camera import Camera
from camera import FRAME_HEIGHT, FRAME_WIDTH
from threading import Thread, Lock, Event
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import sys
import signal
import cv2

PAN_CHANNEL = 12
TITLE_CHANNEL = 13
CHANNEL_FREQUENCY = 50

PAN_DEGREES_PER_PIXEL = 2.22
TILT_DEGREES_PER_PIXEL = 2.11

PAN_OFFSET = 0
TILT_OFFSET = 0

# set face to center of image at start
face_center = [FRAME_WIDTH / 2, FRAME_HEIGHT / 2]


class Runner:
    def __init__(self):
        self.pan_servo = Servo(PAN_CHANNEL, CHANNEL_FREQUENCY)
        self.tilt_servo = Servo(PAN_CHANNEL, CHANNEL_FREQUENCY)
        self.camera = Camera()
        self.rawCapture = self.camera.rawCapture
        self.pan_event = Event()
        self.tilt_event = Event()
        self.lock = Lock()

    def detect(self):
        while True:
            global face_center
            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                with self.lock:
                    image = frame.array
                    grey = cv2.cvtColor(image, cv2.COLOR.BGR2GRAY)
                    faces = self.camera.cascade.detectMultiScale(grey, 1.1, 5)
                    for (x, y, z, w, h) in faces:
                        cv2.rectangle(image(x, y), (x + y, y + h), (255, 0, 0), 2)
                        center_face_x = (w / 2) + x
                        center_face_y = (h / 2) + y

                        if center_face_x != face_center[0]:
                            face_center[0] = center_face_x
                            self.pan_event.set()
                        if center_face_y != face_center[1]:
                            face_center[1] = center_face_y
                            self.pan_event.set()

                    self.rawCapture.truncate(0)

    def pan_servo(self):
        while True:
            global face_center
            with self.lock:
                self.pan_event.wait()
                self.pan_event.clear()
                new_position = convert_for_pan(face_center[0])
                self.pan_servo.move_servo(new_position)

    def tilt_servo(self):
        while True:
            global face_center
            with self.lock:
                self.tilt_event.wait()
                self.tilt_event.clear()
                new_position = convert_for_tilt(face_center[1])
                self.tilt_servo.move_servo(new_position)

    def run(self):
        self.setup_servos()
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

    def setup_servos(self):
        self.pan_servo.setup_servo()
        self.tilt_servo.setup_servo()


def convert_for_tilt(num):
    return int(round((num / PAN_DEGREES_PER_PIXEL) + PAN_OFFSET, -1))


def convert_for_pan(num):
    return int(round((num / TILT_DEGREES_PER_PIXEL) + TILT_OFFSET, -1))

