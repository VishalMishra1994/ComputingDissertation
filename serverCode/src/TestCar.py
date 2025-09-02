import time
import configFile as config
import paho.mqtt.client as mqtt

client = mqtt.Client(client_id=config.deviceName)
client.connect("localhost", 1883, 60)  # Replace 'localhost' with broker IP if needed

# Publish a message
client.publish("test/topic", "Hello from publisher!")

time.sleep(1)
# Disconnect cleanly
client.disconnect()
