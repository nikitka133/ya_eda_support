import random
from datetime import datetime, timedelta

from person import Operator, User, Database


def generate_random_name():
    first_names = ["Иван", "Петр", "Сергей", "Анна", "Мария"]
    last_names = ["Иванов", "Петров", "Сидоров", "Смирнова", "Кузнецова"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def generate_random_city():
    cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург",
              "Казань"]
    return random.choice(cities)


def generate_random_date(start_year=1970, end_year=2005):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    return (start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days))).date()


def generate_operator():
    return Operator(
        full_name=generate_random_name(),
        city=generate_random_city(),
        birth_date=generate_random_date(),
        position="Support Specialist",
        experience_years=random.randint(1, 10)
    )


def generate_user():
    return User(
        full_name=generate_random_name(),
        city=generate_random_city(),
        birth_date=generate_random_date()
    )


def generate_random_message():
    messages = ["Привет, как дела?", "Мне нужна помощь!",
                "Какой у вас график работы?", "Спасибо за помощь!"]
    return random.choice(messages)


if __name__ == "__main__":
    db = Database()

    # Генерация операторов и пользователей
    operators = [generate_operator() for _ in range(10)]
    users = [generate_user() for _ in range(100)]

    for operator in operators:
        db.add_operator(operator)

    for user in users:
        db.add_user(user)

    # Генерация чатов
    for user in users:
        user_id = db.conn.execute("SELECT id FROM users WHERE full_name = ?",
                                  (user.full_name,)).fetchone()[0]
        available_operators = db.conn.execute('''SELECT id FROM operators 
                                                 WHERE id NOT IN (SELECT operator_id FROM chats WHERE is_closed = 0)''').fetchall()
        if available_operators:
            operator_id = random.choice(available_operators)[0]
            db.create_chat(user_id, operator_id)
            chat_id = db.conn.execute("SELECT last_insert_rowid()").fetchone()[
                0]
            for _ in range(random.randint(1, 5)):
                sender = random.choice([user.full_name, db.conn.execute(
                    "SELECT full_name FROM operators WHERE id = ?",
                    (operator_id,)).fetchone()[0]])
                db.add_message(chat_id, sender, generate_random_message())
            if random.choice([True, False]):
                csat = random.randint(1, 5)
                db.close_chat(chat_id, csat)

    # Выгрузка данных
    db.export_data()

    # Примеры выгрузок
    print("Все чаты:")
    print(db.get_chats())

    print("Чаты по оператору:")
    if operators:
        operator_id = \
        db.conn.execute("SELECT id FROM operators WHERE full_name = ?",
                        (operators[0].full_name,)).fetchone()[0]
        print(db.get_chats(by_operator_id=operator_id))

    print("Чаты по пользователю:")
    if users:
        user_id = db.conn.execute("SELECT id FROM users WHERE full_name = ?",
                                  (users[0].full_name,)).fetchone()[0]
        print(db.get_chats(by_user_id=user_id))
