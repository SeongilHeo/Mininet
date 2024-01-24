import sys
import socket

# Create clinet socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_IP = sys.argv[1]

# Set server IP & port
server_address = (server_IP, 12345)

# Connect to server
client_socket.connect(server_address)
print(f"Connected to server: {server_address}")

# Receive data from server
data = client_socket.recv(1024).decode()
print(f"Received data: {data}")

# Send data to server
message = "Hello, my name is Seongil Heo at Winet."
client_socket.sendall(message.encode())

# End connection
client_socket.close()
