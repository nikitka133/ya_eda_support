import json
import random

from chat import Chat


class SupportPlatform:
    def __init__(self):
        self.operators = []
        self.users = []
        self.chats = []

    def add_operator(self, operator):
        self.operators.append(operator)

    def add_user(self, user):
        self.users.append(user)

    def create_chat(self, user):
        available_operators = [op for op in self.operators if not any(chat.operator == op and not chat.is_closed for chat in self.chats)]
        operator = random.choice(available_operators) if available_operators else None
        chat = Chat(user, operator)
        self.chats.append(chat)
        return chat

    def get_chats(self, by_operator=None, by_user=None):
        if by_operator:
            return [chat for chat in self.chats if chat.operator == by_operator]
        if by_user:
            return [chat for chat in self.chats if chat.user == by_user]
        return self.chats

    def export_data(self):
        data = {
            "operators": [vars(op) for op in self.operators],
            "users": [vars(user) for user in self.users],
            "chats": [
                {
                    "user": chat.user.full_name,
                    "operator": chat.operator.full_name if chat.operator else None,
                    "messages": chat.messages,
                    "csat": chat.csat,
                    "is_closed": chat.is_closed
                }
                for chat in self.chats
            ]
        }
        with open('support_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(json.dumps(data, ensure_ascii=False, indent=4))
