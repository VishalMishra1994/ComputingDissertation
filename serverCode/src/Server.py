import paho.mqtt.client as mqtt

# Callback when connected to broker
def on_connect(client, userdata, flags, reasonCode, properties=None):
    # print("Connected with result code " + str(reasonCode))
    # Subscribe to a topic
    if reasonCode == 0:
        print("Connected")
        client.subscribe("test/topic")
        # client.subscribe("CarMessages")
        # client.subscribe("ServerMessages")
    else:
        print("Connection failed with result code " + str(reasonCode))

# Callback when a message is received
def on_message(client, userdata, msg):
    # print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}'")
    if getattr(msg, "properties", None) and getattr(msg.properties, "UserProperty", None):
        props = dict(msg.properties.UserProperty)
        if props.get("content_type") == "face":
            with open(filename, "wb") as f:
                f.write(msg.payload)
            print(f"Saved {filename} , {len(m.payload)} bytes")
    
    else:
        print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}'")

client = mqtt.Client(client_id="Server", protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)  # Replace 'localhost' with broker IP if needed
client.loop_forever()


##############
# client = mqtt.Client()
# client.connect("localhost", 1883)
# client.publish("alerts/status", "Server is online")
# client.disconnect()

# import socket
# import select

# HOST = '0.0.0.0'  # Accept connections from anywhere (Tailscale will secure it)
# PORT = 6000

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST, PORT))
# server_socket.listen(1)
# print(f"🔌 Server listening on port {PORT}...")

# conn, addr = server_socket.accept()
# print(f"✅ Connection established with {addr}")

# conn.setblocking(False)

# while True:
#     readable, _, _ = select.select([conn], [], [], 0.5)
#     for s in readable:
#         data = s.recv(1024)
#         if not data:
#             print("❌ Connection closed by client.")
#             conn.close()
#             server_socket.close()
#             exit()
#         message = data.decode()
#         print(f"📩 Client says: {message}")

#     # Server can also send messages
#     user_input = input("💬 Enter message to client (or 'exit'): ")
#     if user_input.lower() == 'exit':
#         conn.sendall(b'Goodbye!')
#         conn.close()
#         server_socket.close()
#         print("👋 Server shutting down.")
#         break
#     else:
#         conn.sendall(user_input.encode())

###################################################################
# tskey-auth-krRABAAdfH11CNTRL-8cKfkvzbbu2EM1L6m5AYu26LKqLGZJUc
# import socket
# import threading
# import os
# from protocol import HEADER_SIZE, TEXT, IMAGE

# HOST = '0.0.0.0'
# PORT = 6000

# def handle_client(conn, addr):
#     print(f"📶 Connected by {addr}")
#     while True:
#         try:
#             header = conn.recv(HEADER_SIZE).decode()
#             if not header:
#                 break

#             msg_type, length = header.strip().split(':')
#             length = int(length)

#             if msg_type == TEXT:
#                 data = conn.recv(length).decode()
#                 print(f"💬 Message from {addr[0]}: {data}")
#             elif msg_type == IMAGE:
#                 filename = conn.recv(100).decode().strip()
#                 image_data = b''
#                 while len(image_data) < length:
#                     packet = conn.recv(min(4096, length - len(image_data)))
#                     if not packet:
#                         break
#                     image_data += packet

#                 with open(f"received_{filename}", 'wb') as f:
#                     f.write(image_data)
#                 print(f"📷 Image received and saved as received_{filename}")

#         except Exception as e:
#             print(f"❌ Error: {e}")
#             break

#     conn.close()

# def start_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((HOST, PORT))
#     server.listen()
#     print(f"🖥️ Listening on port {PORT}...")

#     while True:
#         conn, addr = server.accept()
#         threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# start_server()
