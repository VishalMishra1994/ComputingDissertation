import os

SERVER_IP = "100.94.90.37"
PORT = 6000
deviceName = "Car2"

#Camera constants
videoWidth, videoHeight = 1920, 1080
FPS = 15
vidFormat = "RGB888"
videoScaler = 6
frameSkip = 1

#Cascade path
cascadePath = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")

#Face Recognition Model path
FaceRecognitionModelParentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FaceRecognitionModel = os.path.join(FaceRecognitionModelParentDir, "FaceRecognitionModel", "LBPH_Trainer.py")
FaceRecognitionDatasetPath = os.path.join(FaceRecognitionModelParentDir, "FaceRecognitionModel", "FaceTrainingDataset")