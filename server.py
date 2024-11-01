import socket

ROOT_PASSWORD = "apalahapalah"

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    clients = {}

    print(f"Server started on {ip}:{port}")

    try:
        while True:
            message, address = server_socket.recvfrom(1024)
            message = message.decode()
            print (message)
            print(address)

            if message.lower() == "shutdown":
                print("Shutdown command received. Shutting down the server.")
                break  # Exit the loop to shut down the server

            if address not in clients:
                # If the password is correct, save the client
                if message == ROOT_PASSWORD:
                    clients[address] = "User" + str(len(clients) + 1)
                    print(f"{clients[address]} ({address}) has joined the chatroom.")
                    server_socket.sendto("Password accepted. Welcome to the chatroom!".encode(), address)
                else:
                    print(f"Connection attempt with wrong password from {address}")
                    server_socket.sendto("Incorrect password. Connection denied.".encode(), address)
                    continue
            else:
                # Print the message from the sender
                print(f"Received message from {clients[address]}: {message}")

                # Forward the message to all other clients
                for client_address in clients:
                    if client_address != address:  # Do not send to the sender
                        server_socket.sendto(message.encode(), client_address)
    finally:
        server_socket.close()
        print("Server has been shut down.")

if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 12345
    start_server(ip, port)