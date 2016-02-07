import picamera
from time import sleep

FRAME_WIDTH = 400
FRAME_HEIGHT = 300
FRAME_RATE = 60
FRAME_SIZE = ( FRAME_WIDTH, FRAME_HEIGHT )

camera = picamera.PiCamera()
camera.resolution = (FRAME_WIDTH, FRAME_HEIGHT)
camera.framerate = FRAME_RATE

camera.start_preview()
sleep(5)
camera.stop_preview()
camera.capture('image.jpg')

