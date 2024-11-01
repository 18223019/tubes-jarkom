import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatClient:
    def __init__(self, root, ip, port):
        self.root = root
        self.root.title("Chat Client")
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # GUI layout
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state="disabled")
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=5)

        # Connection setup
        self.connected = False
        self.username = ""
        self.password = ""

        # Start a thread to listen for messages
        self.listen_thread = threading.Thread(target=self.listen_for_messages)
        self.listen_thread.daemon = True

    def connect(self, username, password):
        self.username = username
        self.password = password

        try:
            # Send password to the server
            self.client_socket.sendto(password.encode(), (self.ip, self.port))

            # Receive server response
            response, _ = self.client_socket.recvfrom(1024)
            response_message = response.decode()
            self.show_message(response_message)

            if "Password accepted" in response_message:
                self.connected = True
                self.show_message(f"Connected as {username}. Type your messages below:")
                self.listen_thread.start()
            else:
                self.show_message("Connection failed: Incorrect password.")
        except OSError as e:
            self.show_message(f"Connection error: {e}")

    def listen_for_messages(self):
        """Function to listen for incoming messages from the server."""
        while self.connected:
            try:
                message, _ = self.client_socket.recvfrom(1024)
                self.show_message(message.decode())
            except:
                self.show_message("Connection closed.")
                self.connected = False
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            full_message = f"{self.username}: {message}"
            self.client_socket.sendto(full_message.encode(), (self.ip, self.port))
            self.message_entry.delete(0, tk.END)

    def show_message(self, message):
        """Display a message in the chat display."""
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state="disabled")
        self.chat_display.yview(tk.END)  # Scroll to the end

    def close(self):
        """Close the client connection and exit the program."""
        self.connected = False
        self.client_socket.close()
        self.root.destroy()

def main():
    # Set up GUI
    root = tk.Tk()
    ip = "10.5.107.181"  # Change IP if necessary
    port = 12345         # Change port if necessary

    client = ChatClient(root, ip, port)

    # Prompt for username and password
    username = input("Enter your username: ")
    password = input("Enter password: ")

    client.connect(username, password)

    # Handle closing the window
    root.protocol("WM_DELETE_WINDOW", client.close)
    root.mainloop()

if __name__ == "__main__":
    main()
