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
        self.host = host
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
            print("What to do: ")
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
        response = messageParser.parse(message)
        print(response)

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        msg = data.split(" ")
        request = msg[0]
        content = ""
        if len(msg) > 1:
            if request == 'msg' and len(msg)>2:
                for word in msg[1:]:
                    content += word + ' '
            else:
                content = msg[1]
        if request in ['logout', 'names', 'help']:
            content = None
        message = {
            'request': request,
            'content': content
        }
        self.connection.sendall(json.dumps(message).encode())
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
