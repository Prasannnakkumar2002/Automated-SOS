import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.137.242", 12345))  # Replace with appropriate IP and port
    server_socket.listen(1)
    
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print("Connected to:", client_address)

    sos_pattern = "SOS"  # Replace with your SOS pattern
    client_socket.send(sos_pattern.encode())

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
