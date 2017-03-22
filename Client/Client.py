# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.host = (host, server_port)
        self.server_port = server_port

        self.run()

    def run(self):
        # TODO
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        receiver = MessageReceiver(self, self.connection)
        receiver.start()

        running = True
        while running:
            client_input = input()
            if client_input == "exit":
                running = False
                self.disconnect()
            else:
                self.send_payload(client_input)
    
    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        messageParser = MessageParser()
        response = MessageParser.parse(message)
        print(response)

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        request, content = data.split(" ")
        message = {
            'request': request,
            'content': content
        }
        self.connection.sendall(json.dumps(message))
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
