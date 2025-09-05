SERVER_IP = "100.94.90.37"
PORT = 6000
deviceName = "Car1"

#Camera constants
videoWidth, videoHeight, FPS = 320, 240, 15
vidFormat = "RGB888"
frameSkip = 1

#Cascade path
import os
cascadePath = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")