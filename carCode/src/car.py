import cv2
import time, sys, signal
from picamera2 import Picamera2
import configFile as config
import socket
import select
import base64
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
from datetime import datetime
from FaceRecognitionModel.LBPH_Trainer import TrainModel

# print(config.SERVER_IP)
def stop(sig, frm):
    picam2.stop()
    client.disconnect()
    print("\nBye")
    sys.exit(0)

#Remove lines below
TrainModel()
print("\nBye")
sys.exit(0)

def sendText(topic, msg):
    client.publish(topic, msg)

def sendFace(topic, face, fileName, msg):
    props.UserProperty = [("filename", f"{fileName}.jpg"), ("content_type", "face"), ("message", msg)]
    client.publish(topic, face, qos=1, properties=props)
    # _, buffer = cv2.imencode('.jpg', face)
    # faceAsText = base64.b64encode(buffer).decode('utf-8')
    # sendText(topic, faceAsText)

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(config.cascadePath)
if face_cascade.empty():
    print("Error: Haar cascade not loaded")
    sys.exit(1)

print("Haar detection running… Ctrl+C to stop")
signal.signal(signal.SIGINT, stop)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (config.videoWidth, config.videoHeight), "format": "RGB888"}))
picam2.start()
time.sleep(0.5)

client = mqtt.Client(client_id=config.deviceName, protocol=mqtt.MQTTv5)
client.connect(config.SERVER_IP, 1883, 60)
props = Properties(PacketTypes.PUBLISH)
client.publish("test/topic", "Hello from " + config.deviceName)

# Detect Face
t0, n = time.time(), 0
while True:
    frame_original = picam2.capture_array()
    if n % config.frameSkip == 0:
        frame_resized = cv2.resize(frame_original, (0, 0), fx=(1/config.videoScaler), fy=(1/config.videoScaler)) #Resizing the frame to a lower resolution
        gray  = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))

        if len(faces) > 0:
            currentTime = datetime.now()
            timeStamp = currentTime.strftime("%Y%m%d%H%M%S%f")[:-3]
            for i, (x, y, w, h) in enumerate(faces):
                #crop face out of original frame
                x *= config.videoScaler
                y *= config.videoScaler
                w *= config.videoScaler
                h *= config.videoScaler

                face_rgb = frame_original[y:y+h, x:x+w]
                face_bgr = cv2.cvtColor(face_rgb, cv2.COLOR_RGB2BGR)
                ok, face = cv2.imencode(".jpg", face_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if not ok:
                    continue
                
                sendFace("test/topic", face.tobytes(), f"face_{timeStamp}_{i}", "Face") #change msg here
                # print(f"boxes={face.tolist()}")
                # cv2.imwrite(f"Face{i}.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            print(f"faces={len(faces)} | boxes={faces.tolist()}")

        
        # elif n % (config.FPS) == 0:
        #     fps = (n+1)/(time.time()-t0)
        #     print(f"FPS≈{fps:0.1f} | faces=0")
        #     cv2.imwrite("debug_frame.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        #     print("Saved debug_frame.jpg — check lighting/distance/pose")
            # cv2.imwrite(f"frame_{n}.jpg", frame)
            # print("saved", f"frame_{n}.jpg", frame.shape)
    n += 1







