import paho.mqtt.client as mqtt
import configFile as config

# Callback when connected to broker
def on_connect(client, userdata, flags, reasonCode, properties=None):
    if reasonCode == 0:
        print("Connected")
        client.subscribe("CarMessages")
        client.subscribe("ServerMessages")
    else:
        print("Connection failed with result code " + str(reasonCode))

# Callback when a message is received
def on_message(client, userdata, msg):
    if getattr(msg, "properties", None) and getattr(msg.properties, "UserProperty", None):
        props = dict(msg.properties.UserProperty)
        if props.get("content_type") == "face":
            with open(config.FacesFolder/props.get("filename"), "wb") as f:
                f.write(msg.payload)
            print(f"Saved {props.get("filename")} , {len(msg.payload)} bytes")
    
    else:
        print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}'")

client = mqtt.Client(client_id="Server", protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)  # Replace 'localhost' with broker IP if needed
client.loop_forever()