import socket

ROOT_PASSWORD = "yanggampang"

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    clients = {}
    usernames = set()  # Set to store unique usernames

    print(f"Server started on {ip}:{port}")

    try:
        while True:
            message, address = server_socket.recvfrom(1024)
            message = message.decode().strip()
            print(f"Received from {address}: {message}")

            if message.lower() == "shutdown":
                print("Shutdown command received. Shutting down the server.")
                break

            # Split message into password and username for authentication
            if address not in clients:
                # Expected message format: "password:username"
                if ":" in message:
                    password, username = message.split(":", 1)

                    # Validate password
                    if password == ROOT_PASSWORD:
                        # Check if username is unique
                        if username in usernames:
                            # Send a rejection message if username is already taken
                            server_socket.sendto("Username already taken. Please choose a different username.".encode(), address)
                            print(f"Rejected connection from {address} with duplicate username '{username}'")
                        else:
                            # Save the client and their username
                            clients[address] = username
                            usernames.add(username)
                            print(f"{username} ({address}) has joined the chatroom.")
                            server_socket.sendto(f"Password accepted. Welcome to the chatroom, {username}!".encode(), address)
                    else:
                        print(f"Connection attempt with wrong password from {address}")
                        server_socket.sendto("Incorrect password. Connection denied.".encode(), address)
                else:
                    # Invalid format if no ":" in message
                    server_socket.sendto("Invalid login format. Use 'password:username'.".encode(), address)
                    print(f"Invalid login format from {address}")
            else:
                # Handle incoming messages from authenticated clients
                username = clients[address]
                print(f"Received message from {username}: {message}")

                # Forward message to all other clients
                for client_address in clients:
                    if client_address != address:
                        server_socket.sendto(f"{username}: {message}".encode(), client_address)
    finally:
        server_socket.close()
        print("Server has been shut down.")

if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 12345
    start_server(ip, port)
