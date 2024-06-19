import sqlite3
import random
from datetime import datetime, timedelta
import json


class Database:
    def __init__(self, db_name='support_platform.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS operators (
                                id INTEGER PRIMARY KEY,
                                full_name TEXT,
                                city TEXT,
                                birth_date TEXT,
                                position TEXT,
                                experience_years INTEGER)''')

            self.conn.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                full_name TEXT,
                                city TEXT,
                                birth_date TEXT)''')

            self.conn.execute('''CREATE TABLE IF NOT EXISTS chats (
                                id INTEGER PRIMARY KEY,
                                user_id INTEGER,
                                operator_id INTEGER,
                                csat INTEGER,
                                is_closed BOOLEAN)''')

            self.conn.execute('''CREATE TABLE IF NOT EXISTS messages (
                                id INTEGER PRIMARY KEY,
                                chat_id INTEGER,
                                sender TEXT,
                                text TEXT,
                                timestamp TEXT)''')

    def add_operator(self, operator):
        with self.conn:
            self.conn.execute('''INSERT INTO operators (full_name, city, birth_date, position, experience_years)
                                VALUES (?, ?, ?, ?, ?)''',
                              (operator.full_name, operator.city,
                               operator.birth_date, operator.position,
                               operator.experience_years))

    def add_user(self, user):
        with self.conn:
            self.conn.execute('''INSERT INTO users (full_name, city, birth_date)
                                VALUES (?, ?, ?)''',
                              (user.full_name, user.city, user.birth_date))

    def create_chat(self, user_id, operator_id):
        with self.conn:
            self.conn.execute('''INSERT INTO chats (user_id, operator_id, csat, is_closed)
                                VALUES (?, ?, ?, ?)''',
                              (user_id, operator_id, None, False))

    def add_message(self, chat_id, sender, text):
        with self.conn:
            self.conn.execute('''INSERT INTO messages (chat_id, sender, text, timestamp)
                                VALUES (?, ?, ?, ?)''',
                              (chat_id, sender, text,
                               datetime.now().isoformat()))

    def close_chat(self, chat_id, csat):
        with self.conn:
            self.conn.execute(
                '''UPDATE chats SET csat = ?, is_closed = ? WHERE id = ?''',
                (csat, True, chat_id))

    def get_open_chats(self):
        with self.conn:
            return self.conn.execute(
                '''SELECT * FROM chats WHERE is_closed = 0''').fetchall()

    def get_chats(self, by_operator_id=None, by_user_id=None):
        query = "SELECT * FROM chats"
        params = []
        if by_operator_id:
            query += " WHERE operator_id = ?"
            params.append(by_operator_id)
        elif by_user_id:
            query += " WHERE user_id = ?"
            params.append(by_user_id)

        with self.conn:
            return self.conn.execute(query, params).fetchall()

    def get_messages(self, chat_id):
        with self.conn:
            return self.conn.execute(
                '''SELECT * FROM messages WHERE chat_id = ?''',
                (chat_id,)).fetchall()

    def export_data(self):
        with self.conn:
            operators = self.conn.execute(
                '''SELECT * FROM operators''').fetchall()
            users = self.conn.execute('''SELECT * FROM users''').fetchall()
            chats = self.conn.execute('''SELECT * FROM chats''').fetchall()
            messages = self.conn.execute(
                '''SELECT * FROM messages''').fetchall()

        data = {
            "operators": [dict(
                zip(["id", "full_name", "city", "birth_date", "position",
                     "experience_years"], op)) for op in operators],
            "users": [dict(zip(["id", "full_name", "city", "birth_date"], usr))
                      for usr in users],
            "chats": [dict(
                zip(["id", "user_id", "operator_id", "csat", "is_closed"],
                    chat)) for chat in chats],
            "messages": [dict(
                zip(["id", "chat_id", "sender", "text", "timestamp"], msg)) for
                         msg in messages]
        }

        with open('support_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(json.dumps(data, ensure_ascii=False, indent=4))


class Person:
    def __init__(self, full_name, city, birth_date):
        self.full_name = full_name
        self.city = city
        self.birth_date = birth_date


class Operator(Person):
    def __init__(self, full_name, city, birth_date, position,
                 experience_years):
        super().__init__(full_name, city, birth_date)
        self.position = position
        self.experience_years = experience_years


class User(Person):
    def __init__(self, full_name, city, birth_date):
        super().__init__(full_name, city, birth_date)
