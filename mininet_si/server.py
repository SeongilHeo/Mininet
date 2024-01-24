import sys
import socket

# Create server socket(IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_IP = sys.argv[1]

# Set IP address, port
server_address = (server_IP, 12345)
server_socket.bind(server_address)

# Wait for connection
server_socket.listen(5)
round=0
while True:
    round+=1
    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Connected from {client_address}")
    
    # Send data to the client
    message = "Welcome your Admission"
    client_socket.sendall(message.encode())

    # Receive data from the clinet
    data = client_socket.recv(1024).decode()
    print(f"Received data: {data}")

    # End connection
    client_socket.close()
