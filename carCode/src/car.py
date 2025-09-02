import cv2
import time, sys, signal
from picamera2 import Picamera2
import configFile as config
import socket
import select
import base64
import paho.mqtt.client as mqtt

# print(config.SERVER_IP)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (W, H), "format": "RGB888"}))
picam2.start()
time.sleep(0.5)

print("Haar detection running… Ctrl+C to stop") 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_id=config.deviceName)
client.connect(config.SERVER_IP, 1883, 60)

def stop(sig, frm):
    picam2.stop()
    print("\nBye")
    sys.exit(0)

signal.signal(signal.SIGINT, stop)

def sendText(topic, msg):
    client.publish(topic, msg)

def sendFace(topic, face):
    _, buffer = cv2.imencode('.jpg', face)
    faceAsText = base64.b64encode(buffer).decode('utf-8')
    sendText(topic, faceAsText)


client.publish("test/topic", "Hello from " + config.deviceName)

client.disconnect()

#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Detect Face
t0, n = time.time(), 0
while True:
    frame = picam2.capture_array()
    if n % configFile.frameSkip == 0:
        gray  = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(40, 40))
        if n % (FPS) == 0:
            fps = (n+1)/(time.time()-t0)
            print(f"FPS≈{fps:0.1f} | faces={len(faces)} | boxes={faces.tolist() if len(faces) else []}")
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






