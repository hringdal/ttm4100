# -*- coding: utf-8 -*-
import socketserver
import json
import time
import re

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

clients = {}
messages = []

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.logged_in = False



        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)

            # TODO: Add handling of received payload from client

            received_dict = json.loads(received_string)
            request = received_dict['request']
            content = received_dict['content']


            # handle different requests with if/else

            if request == 'login':
                if content in clients.values():
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response':'error',
                        'content':'username already exist'
                        }
                    self.send_data(response)
                elif self.logged_in:
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response':'error',
                        'content':'already logged in'
                    }
                elif not re.match("^[A-Za-z0-9]+$", content):
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response':'error',
                        'content':'Username can only contain letters and numbers, and cannot be empty'
                    }
                else:
                    clients[self] = content
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response': 'info',
                        'content': 'login successful!'
                        }
                    self.send_data(response)
                    self.logged_in = True
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response': 'history',
                        'content': messages
                        }
                    self.send_data(response)
            elif request == 'logout':
                if self.logged_in:
                    self.logged_in = False
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response': 'info',
                        'content': None
                        }
                    self.send_data(response)
                else:
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response': 'error',
                        'content': 'Not logged in'
                    }
                    self.send_data(response)
            elif request == 'msg':
                if self.logged_in:
                    if type(content) is str:
                        messages.append(json.dumps(content))
                        response = {
                            'timestamp':time.strftime("%H:%M:%S"),
                            'sender':'server',
                            'response': 'message',
                            'content': content
                        }
                        for client in clients:
                            client.send_data(response)
                    else:
                        response = {
                            'timestamp':time.strftime("%H:%M:%S"),
                            'sender':'server',
                            'response': 'error',
                            'content': 'Not string in content'
                        }
                        self.send_data(response)
                else:
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response': 'error',
                        'content': 'Not logged in'
                    }
                    self.send_data(response)
            elif request == 'names':
                if self.logged_in:
                    names = []
                    for client in clients:
                        names.append(clients[client])
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response': 'info',
                        'content': names
                    }
                    self.send_data(response)
                else:
                    response = {
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response': 'error',
                        'content': 'Not logged in'
                    }
                    self.send_data(response)
            elif request == 'help':
                response = {
                    'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response': 'info',
                        'content': '''login <username> - log in with the given username \n
                                    logout - log out \n
                                    msg <message> - send message \n
                                    names - list users in chat'''
                       }
                self.send_data(response)
            else:
                response ={
                        'timestamp':time.strftime("%H:%M:%S"),
                        'sender':'server',
                        'response': 'error',
                        'content': 'not given command, use help'
                    }
                self.send_data(response)
                
    def send_data(self, response):
        self.request.sendall(json.dumps(response))
        self.request.sendall("\n")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
