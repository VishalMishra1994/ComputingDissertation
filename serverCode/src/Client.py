import socket
import select

SERVER_IP = "100.94.90.37"  #Tailscale IP of server
PORT = 6000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
client_socket.setblocking(False)

print(f"🔗 Connected to server at {SERVER_IP}:{PORT}")

while True:
    readable, _, _ = select.select([client_socket], [], [], 0.5)
    for s in readable:
        data = s.recv(1024)
        if not data:
            print("❌ Server closed connection.")
            client_socket.close()
            exit()
        message = data.decode()
        print(f"📩 Server says: {message}")

    # Client can also send messages
    user_input = input("💬 Enter message to server (or 'exit'): ")
    if user_input.lower() == 'exit':
        client_socket.sendall(b'Goodbye!')
        client_socket.close()
        print("👋 Client exiting.")
        break
    else:
        client_socket.sendall(user_input.encode())


###################################################################

# import socket
# import os
# from protocol import HEADER_SIZE, TEXT, IMAGE

# def send_text(ip, port, message):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((ip, port))
#         header = f"{TEXT}:{len(message):<{HEADER_SIZE - len(TEXT) - 1}}"
#         s.sendall(header.encode())
#         s.sendall(message.encode())

# def send_image(ip, port, filepath):
#     if not os.path.exists(filepath):
#         print("❌ File does not exist.")
#         return

#     filesize = os.path.getsize(filepath)
#     filename = os.path.basename(filepath)

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((ip, port))
#         header = f"{IMAGE}:{filesize:<{HEADER_SIZE - len(IMAGE) - 1}}"
#         s.sendall(header.encode())
#         s.sendall(f"{filename:<100}".encode())  # Fixed-length filename

#         with open(filepath, 'rb') as f:
#             while True:
#                 bytes_read = f.read(4096)
#                 if not bytes_read:
#                     break
#                 s.sendall(bytes_read)

#         print(f"📤 Image {filename} sent.")

# # Simple command-line interface
# if __name__ == '__main__':
#     print("Send message/image to another peer")
#     ip = input("Enter peer Tailscale IP: ")
#     port = int(input("Enter peer port (e.g., 6000): "))
#     mode = input("Send (text/image): ").strip().lower()

#     if mode == 'text':
#         message = input("Enter message: ")
#         send_text(ip, port, message)
#     elif mode == 'image':
#         filepath = input("Enter image file path: ")
#         send_image(ip, port, filepath)
#     else:
#         print("❌ Invalid mode.")
