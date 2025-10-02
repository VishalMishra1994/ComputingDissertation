import time
import configFile as config
import paho.mqtt.client as mqtt

client = mqtt.Client(client_id=config.deviceName)
client.connect(config.SERVER_IP, 1883, 60)  # Replace 'localhost' with broker IP if needed

# Publish a message
client.publish("CarMessages", "Hello from TestCar")

time.sleep(1)
# Disconnect cleanly
client.disconnect()
