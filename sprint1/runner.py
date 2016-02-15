from servo import *
from camera import *
from camera import FRAME_HEIGHT, FRAME_WIDTH
from threading import Thread, Lock, Event
import cv2

PAN_CHANNEL = 11
TITLE_CHANNEL = 18
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
        self.tilt_servo = Servo(TITLE_CHANNEL, CHANNEL_FREQUENCY)
        self.pan_servo_move = getattr(self.pan_servo, 'move_servo')
        self.tilt_servo_move = getattr(self.tilt_servo, 'move_servo')
        self.camera = Camera()
        self.rawCapture = self.camera.rawCapture
        self.pan_event = Event()
        self.tilt_event = Event()
        self.lock = Lock()

    def detect(self):
        while True:
            global face_center
            for frame in self.camera.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                with self.lock:
                    image = frame.array
                    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    faces = self.camera.cascade.detectMultiScale(grey, 1.1, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(image, (x, y), (x + y, y + h), (255, 0, 0), 2)
                        center_face_x = (w / 2) + x
                        center_face_y = (h / 2) + y

                        print "Pic center x: " + str(center_face_x)
                        print "Pic center y: " + str(center_face_y)
                        print "Old center x: " + str(face_center[0])
                        print "Old center y: " + str(face_center[1])

                        if center_face_x != face_center[0]:
                            face_center[0] = center_face_x
                            self.pan_event.set()
                        if center_face_y != face_center[1]:
                            face_center[1] = center_face_y
                            self.tilt_event.set()

                    self.rawCapture.truncate(0)

    def pan_servo_thread(self):
        while True:
            global face_center
            with self.lock:
                print 'pan thread'
                self.pan_event.wait()
                self.pan_event.clear()
                new_position = convert_for_pan(face_center[0])
                self.pan_servo.move_servo(new_position)

    def tilt_servo_thread(self):
        while True:
            global face_center
            with self.lock:
                print 'pan thread'
                self.tilt_event.wait()
                self.tilt_event.clear()
                new_position = convert_for_tilt(face_center[1])
                print "new pos" + new_position
                self.tilt_servo.move_servo(new_position)

    def run(self):
        self.setup_servos()

        t = Thread(target=self.pan_servo_thread)
        t.daemon = True
        t.start()

        t = Thread(target=self.tilt_servo_thread)
        t.daemon = True
        t.start()

        t = Thread(target=self.detect)
        t.daemon = True
        t.start()

        while True:
            pass

    def setup_servos(self):
        getattr(self.pan_servo, 'setup_servo')()
        getattr(self.tilt_servo, 'setup_servo')()


def convert_for_tilt(num):
    return int(round((num / PAN_DEGREES_PER_PIXEL) + PAN_OFFSET, -1))


def convert_for_pan(num):
    return int(round((num / TILT_DEGREES_PER_PIXEL) + TILT_OFFSET, -1))

if __name__ == '__main__':
    Runner().run()