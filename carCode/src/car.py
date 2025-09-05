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

# print(config.SERVER_IP)
def stop(sig, frm):
    picam2.stop()
    client.disconnect()
    print("\nBye")
    sys.exit(0)

def sendText(topic, msg):
    client.publish(topic, msg)

def sendFace(topic, face, fileName, msg):
    props.UserProperty = [("filename", fileName), ("content_type", "face"), ("message", msg)]
    client.publish(topic, face, qos=1, properties=props)
    # _, buffer = cv2.imencode('.jpg', face)
    # faceAsText = base64.b64encode(buffer).decode('utf-8')
    # sendText(topic, faceAsText)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (config.Width, config.Height), "format": "RGB888"}))
picam2.start()
time.sleep(0.5)

client = mqtt.Client(client_id=config.deviceName, protocol=mqtt.MQTTv5)
client.connect(config.SERVER_IP, 1883, 60)
props = Properties(PacketTypes.PUBLISH)
client.publish("test/topic", "Hello from " + config.deviceName)

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(config.cascadePath)
if face_cascade.empty():
    print("Error: Haar cascade not loaded")
    sys.exit(1)

print("Haar detection running… Ctrl+C to stop")
signal.signal(signal.SIGINT, stop)

# Detect Face
t0, n = time.time(), 0
while True:
    frame = picam2.capture_array()
    if n % config.frameSkip == 0:
        gray  = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(40, 40))

        if len(faces) > 0:
            for i, face in enumerate(faces):
                #crop face out of frame
                #here
                sendFace("test/topic", face, "face" + {i}, i)
                # print(f"boxes={face.tolist()}")
                # cv2.imwrite(f"Face{i}.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            print(f"faces={len(faces)} | boxes={faces.tolist()}")

        
        elif n % (config.FPS) == 0:
            fps = (n+1)/(time.time()-t0)
            print(f"FPS≈{fps:0.1f} | faces=0")
            cv2.imwrite("debug_frame.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            print("Saved debug_frame.jpg — check lighting/distance/pose")
            # cv2.imwrite(f"frame_{n}.jpg", frame)
            # print("saved", f"frame_{n}.jpg", frame.shape)
    n += 1

# cap = cv2.VideoCapture(0)

# while True:
#     ret,frame = cap.read()
#     if not ret:
#         print("Failed to grab frame from camera")
#         break

    
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#     for (x,y,w,h) in faces:
#         faceImg = frame[y:y+h, x:x+w]
#         cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)


#     if cv2.waitKey(1) == ord('q'):
#         break

# cap.release()






