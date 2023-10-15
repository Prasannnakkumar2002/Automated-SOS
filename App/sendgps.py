import socket
import time


# Define the server's IP address and port
server_ip = "192.168.137.28"  # Replace with the main laptop's IP address
server_port = 12345

# Connect to the GPS daemon
# gpsd.connect()

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

while True:
    # packet = gpsd.get_current()
    latitude = 12.9337
    longitude = 77.6921
    gps_data = f"{latitude},{longitude}"

    # Send GPS data to the server
    client_socket.send(gps_data.encode())

    time.sleep(5)  # Send data every 5 seconds

# Close the socket
client_socket.close()
