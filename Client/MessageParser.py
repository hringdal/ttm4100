import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload) #load payload string as json object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return "Invalid server response received"

    def parse_error(self, payload):
        return payload.get('timestamp') + " - Error: " + payload.get('content')
    def parse_info(self, payload):
        return payload.get('timestamp') + " - Info: " + payload.get('content')
    def parse_message(self, payload):
        return payload.get('timestamp') + " - " + payload.get('sender') + ": " + payload.get('content')
    def parse_history(self, payload):
        all_history = payload.get('content')
        history = ""
        for line in all_history:
            history += self.parse_message(json.loads(line)) + "\n"
        return history