import socket
import sys
import logging


def encrypt(message, key):
    encrypted_message = ""
    for char in message:
        encrypted_char = chr(ord(char) + key)
        encrypted_message += encrypted_char
    return encrypted_message


def decrypt(encrypted_message, key):
    decrypted_message = ""
    for char in encrypted_message:
        decrypted_char = chr(ord(char) - key)
        decrypted_message += decrypted_char
    return decrypted_message


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen(1)
    logging.info("Server started")

    while True:
        client_socket, address = server_socket.accept()
        logging.info(f"Connection from {address} established")

        key = 42
        client_socket.send(str(key).encode())

        while True:
            encrypted_command = client_socket.recv(1024)
            command = decrypt(encrypted_command.decode(), key)
            logging.info(f"Received command: {command}")
            if command == "":
                break

            try:
                output = subprocess.check_output(
                    command.split(), stderr=subprocess.STDOUT)
                encrypted_output = encrypt(output.decode(), key)
                client_socket.send(encrypted_output.encode())
            except Exception as e:
                encrypted_error = encrypt(str(e).encode(), key)
                client_socket.send(encrypted_error)

        client_socket.close()


if __name__ == "__main__":
    logging.basicConfig(filename="server.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    start_server()
