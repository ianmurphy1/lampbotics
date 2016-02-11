from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

CASCADES_PATH = '/home/pi/opencv-3.0.0/data/harrcascades'
FACE_CASCADE_FILE = '/haarcascade_frontalface_default.xml'
FRAME_WIDTH = 400
FRAME_HEIGHT = 300
FRAME_RATE = 60
FRAME_SIZE = ( FRAME_WIDTH, FRAME_HEIGHT )


class Camera:

    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (FRAME_WIDTH, FRAME_HEIGHT)
        self.camera.framerate = FRAME_RATE
        self.rawCapture = PiRGBArray(self.camera, size=FRAME_SIZE)
        self.cascade = cv2.CascadeClassifier(FACE_CASCADE_FILE)




