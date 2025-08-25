import cv2
import configFile as config
import socket
import select
import base64
import paho.mqtt.client as mqtt

print(config.SERVER_IP)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_id=config.deviceName)
client.connect(config.SERVER_IP, 1883, 60)

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

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    if not ret:
        print("Failed to grab frame from camera")
        break

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        faceImg = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)


    if cv2.waitKey(1) == ord('q'):
        break

cap.release()






