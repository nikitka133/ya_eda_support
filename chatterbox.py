import random
from person import Database

db = Database()

# Получаем открытые чаты
open_chats = db.get_open_chats()

# Запускаем цикл обработки чатов
while open_chats:
    # Выбираем случайный открытый чат
    chat = random.choice(open_chats)
    _, user_id, operator_id, csat, is_closed = chat
    chat_id = int(input("ID чата "))
    # Выводим информацию о чате и существующие сообщения
    print(f"Обработка чата #{chat_id} между пользователем #{user_id} и оператором #{operator_id}")
    messages = db.get_messages(chat_id)
    for message in messages:
        msg_id, chat_id, sender, text, timestamp = message
        print(f"{timestamp} - {sender}: {text}")

    # Ввод нового сообщения от пользователя
    user_message = input("Введите сообщение от пользователя: ")
    db.add_message(chat_id, f"User {user_id}", user_message)

    # Ввод нового сообщения от оператора
    operator_name = db.conn.execute("SELECT full_name FROM operators WHERE id = ?", (operator_id,)).fetchone()[0]
    operator_message = input(f"Введите сообщение от оператора ({operator_name}): ")
    db.add_message(chat_id, operator_name, operator_message)

    # Проверка, нужно ли закрыть чат
    close_chat = input("Закрыть чат? (да/нет): ").strip().lower()
    if close_chat == "да":
        csat = int(input("Введите оценку CSAT (1-5): "))
        db.close_chat(chat_id, csat)

    # Обновляем список открытых чатов
    open_chats = db.get_open_chats()
