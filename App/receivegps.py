import socket
import webbrowser
import folium

# Define the server's IP address and port
server_ip = "192.168.137.242"  # Replace with your main laptop's IP address
server_port = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen()

print("Waiting for client to connect...")
client_socket, client_address = server_socket.accept()
print("Client connected!")

m = folium.Map(location=[0, 0], zoom_start=15)

while True:
    # Receive GPS data from the client
    gps_data = client_socket.recv(1024).decode()
    latitude, longitude = map(float, gps_data.split(','))

    # Update the map
    m = folium.Map(location=[latitude, longitude], zoom_start=40)
    folium.Marker(location=[latitude, longitude], popup="GPS Location").add_to(m)

    # Save the map as an HTML file and open it in a web browser
    map_filename = "gps_map.html"
    m.save(map_filename)
    webbrowser.open(map_filename)

# Close the sockets
client_socket.close()
server_socket.close()
