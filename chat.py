from datetime import datetime


class Chat:
    def __init__(self, user, operator=None):
        self.user = user
        self.operator = operator
        self.messages = []
        self.csat = None
        self.is_closed = False

    def add_message(self, sender, text):
        message = {
            "sender": sender,
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)

    def close_chat(self, csat):
        self.is_closed = True
        self.csat = csat

