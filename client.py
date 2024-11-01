import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

def listen_for_messages(client_socket, message_area, username):
    """Function to listen for incoming messages from the server and display them."""
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            message = message.decode()
            
            # Check if the message is from the user themselves
            if message.startswith(f"{username}:"):
                message = f"You: {message[len(username) + 2:]}"  # Replace "username:" with "You:"
            
            message_area.config(state=tk.NORMAL)
            message_area.insert(tk.END, message + '\n')
            message_area.yview(tk.END)
            message_area.config(state=tk.DISABLED)
        except:
            print("Connection closed.")
            break

def send_message(client_socket, message_entry, message_area, username, ip, port):
    """Function to send a message to the server and display it in the message area."""
    message = message_entry.get()
    if message.lower() == "exit":
        client_socket.close()
        root.quit()
    else:
        # Send the message to the server
        client_socket.sendto(message.encode(), (ip, port))

        # Display the message in the message area as "You: message"
        message_area.config(state=tk.NORMAL)
        message_area.insert(tk.END, f"You: {message}\n")
        message_area.yview(tk.END)
        message_area.config(state=tk.DISABLED)
        
        # Clear the input entry box
        message_entry.delete(0, tk.END)

def start_client(ip, port, username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Send login credentials to the server in the format "password:username"
        login_message = f"{password}:{username}"
        client_socket.sendto(login_message.encode(), (ip, port))

        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        response_message = response.decode()

        if "Password accepted" in response_message:
            # Create the main window
            global root
            root = tk.Tk()
            root.title("Chatroom")

            # Chat message display area
            message_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
            message_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            # Message entry box
            message_entry = tk.Entry(root, width=50)
            message_entry.pack(padx=10, pady=5, fill=tk.X)

            # Send button
            send_button = tk.Button(root, text="Send", command=lambda: send_message(client_socket, message_entry, message_area, username, ip, port))
            send_button.pack(pady=5)

            # Start a thread to listen for incoming messages
            listen_thread = threading.Thread(target=listen_for_messages, args=(client_socket, message_area, username))
            listen_thread.daemon = True
            listen_thread.start()

            # Start the GUI main loop
            root.protocol("WM_DELETE_WINDOW", lambda: client_socket.close())
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", response_message)
    except OSError as e:
        messagebox.showerror("Connection Error", f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Initial login screen
    login_root = tk.Tk()
    login_root.title("Login to Chatroom")

    tk.Label(login_root, text="IP Address:").pack(pady=5)
    ip_entry = tk.Entry(login_root)
    ip_entry.pack(pady=5)
    ip_entry.insert(0, "10.5.107.181")  # Default IP

    tk.Label(login_root, text="Port:").pack(pady=5)
    port_entry = tk.Entry(login_root)
    port_entry.pack(pady=5)
    port_entry.insert(0, "12345")  # Default Port

    tk.Label(login_root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_root)
    username_entry.pack(pady=5)

    tk.Label(login_root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_root, show="*")
    password_entry.pack(pady=5)

    def login():
        ip = ip_entry.get()
        port = int(port_entry.get())
        username = username_entry.get()
        password = password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password cannot be empty.")
        else:
            login_root.destroy()
            start_client(ip, port, username, password)

    login_button = tk.Button(login_root, text="Login", command=login)
    login_button.pack(pady=10)

    login_root.mainloop()