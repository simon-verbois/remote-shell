import socket
import sys
import os
import subprocess
from Crypto.Cipher import AES
import base64
import logging

def encrypt(message, key):
    # padding
    message = message + " " * ((16-len(message)) % 16)
    # encryption
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(message.encode())
    # encode to base64
    return base64.b64encode(encrypted_message).decode()

def decrypt(message, key):
    # decode from base64
    message = base64.b64decode(message.encode())
    # decryption
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_message = cipher.decrypt(message)
    # remove padding
    return decrypted_message.decode().rstrip()

def start_client():
    # get server information
    hostname = input("Enter server hostname: ")
    port = int(input("Enter server port: "))
    key = input("Enter encryption key: ")
    
    logging.basicConfig(filename=f"{socket.gethostname()}.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # create socket and connect to server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((hostname, port))
    except socket.error as e:
        print(str(e))
        sys.exit()

    while True:
        # get user command
        user_input = input("$ ")
        if not user_input:
            continue

        # encrypt command and send to server
        encrypted_command = encrypt(user_input, key)
        client_socket.send(encrypted_command.encode())

        # receive response from server and decrypt
        encrypted_response = client_socket.recv(4096).decode()
        response = decrypt(encrypted_response, key)

        # print response and log
        print(response)
        logging.info(response)

if __name__ == "__main__":
    start_client()
