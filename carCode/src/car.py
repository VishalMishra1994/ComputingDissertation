import cv2
import os
import time, sys, signal
from picamera2 import Picamera2
from src import configFile as config
import json
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
from datetime import datetime
from FaceRecognitionModel.LBPH_Trainer import TrainModel, FaceRecognitionModel, FaceRecognitionLabelMap, trainerImageSize

# Callback when connected to broker
def on_connect(client, userdata, flags, reasonCode, properties=None):
    if reasonCode == 0:
        print("Connected")
        client.subscribe("CarMessages")
    else:
        print("Connection failed with result code " + str(reasonCode))

def stop(sig, frm):
    picam2.stop()
    client.disconnect()
    print("\nBye")
    sys.exit(0)

def sendText(topic, msg):
    client.publish(topic, msg)

def sendFace(topic, face, fileName, msg):
    props.UserProperty = [("filename", f"{fileName}.jpg"), ("content_type", "face"), ("message", msg)]
    client.publish(topic, face, qos=1, properties=props)

def checkIfModelFilesExist():
    if os.path.exists(FaceRecognitionModel) and os.path.exists(FaceRecognitionLabelMap):
        return True
    
    return False

face_cascade = cv2.CascadeClassifier(config.cascadePath)
if face_cascade.empty():
    print("Error: Haar cascade not loaded")
    sys.exit(1)

if not checkIfModelFilesExist():
    print("Model Files not found. Training Model")
    isTrained = TrainModel()

    if not isTrained:
        print("Model training failing. Exiting.")
        sys.exit(0)

faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
faceRecognizer.read(FaceRecognitionModel)

with open(FaceRecognitionLabelMap, "r") as f:
    labelMap = json.load(f)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (config.videoWidth, config.videoHeight), "format": "RGB888"}))
picam2.start()
time.sleep(0.5)

client = mqtt.Client(client_id=config.deviceName, protocol=mqtt.MQTTv5)
client.connect(config.SERVER_IP, 1883, 60)
props = Properties(PacketTypes.PUBLISH)
client.publish("CarMessages", "Hello from " + config.deviceName)

print("Haar detection running… Ctrl+C to stop")
signal.signal(signal.SIGINT, stop)

# Detect Face
t0, n = time.time(), 0
while True:
    frameOriginal = picam2.capture_array()
    if n % config.frameSkip == 0:
        frameResized = cv2.resize(frameOriginal, (0, 0), fx=(1/config.videoScaler), fy=(1/config.videoScaler)) #Resizing the frame to a lower resolution
        frameResizedGray  = cv2.cvtColor(frameResized, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(frameResizedGray, 1.2, 5, minSize=(20, 20))

        if len(faces) > 0:
            currentTime = datetime.now()
            timeStamp = currentTime.strftime("%Y%m%d%H%M%S%f")[:-3]
            for i, (x, y, w, h) in enumerate(faces):
                #crop face out of original frame
                x *= config.videoScaler
                y *= config.videoScaler
                w *= config.videoScaler
                h *= config.videoScaler

                faceRgb = frameOriginal[y:y+h, x:x+w]
                faceBgr = cv2.cvtColor(faceRgb, cv2.COLOR_RGB2BGR)

                # Recognition
                faceGray = cv2.cvtColor(faceBgr, cv2.COLOR_BGR2GRAY)
                faceResized = cv2.resize(faceGray, trainerImageSize)

                labelId, confidence = faceRecognizer.predict(faceResized)
                personName = labelMap.get(str(labelId), "Unknown")

                if confidence < 70:
                    recognitionResult = f"{personName} ({confidence:.1f})"
                else:
                    recognitionResult = "Unknown"

                print(f"Recognition: {recognitionResult}")

                #################################################
                
                ok, face = cv2.imencode(".jpg", faceBgr, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if ok:
                    if recognitionResult = "Unknown":
                        sendFace("ServerMessages", face.tobytes(), f"face_{timeStamp}_{i}", "Unknown Face")
                    else:
                        sendFace("ServerMessages", face.tobytes(), f"face_{timeStamp}_{i}", f"Recognised Face : {personName} ({confidence:.1f})")
                
    n += 1







