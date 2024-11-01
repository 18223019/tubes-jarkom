import socket
import threading

def listen_for_messages(client_socket):
    """Function to listen for incoming messages from the server."""
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print(message.decode())  # Print the received message
        except:
            print("Connection closed.")
            break

def start_client(ip, port, username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Send login credentials to the server in the format "password:username"
        login_message = f"{password}:{username}"
        client_socket.sendto(login_message.encode(), (ip, port))

        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        response_message = response.decode()
        print(response_message)

        # If the password is accepted, continue
        if "Password accepted" in response_message:
            print(f"Connected as {username}. Type your messages below:")

            # Start a thread to listen for incoming messages
            listen_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
            listen_thread.daemon = True
            listen_thread.start()
            
            while True:
                # Input message from the user
                message = input()

                # Check if the user wants to exit
                if message.lower() == "exit":
                    print("Exiting chatroom...")
                    break

                # Send the message directly to the server (without username prefix)
                client_socket.sendto(message.encode(), (ip, port))

    except OSError as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    ip = "10.5.107.181"  # Change IP if necessary
    port = 12345         # Change port if necessary
    username = input("Enter your username: ")
    password = input("Enter password: ")

    start_client(ip, port, username, password)