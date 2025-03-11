import psycopg2
from faker import Faker
import random
from config import DB_CONFIG 

fake = Faker()

def connect_db():
    return psycopg2.connect(
        dbname=DB_CONFIG["dbname"], 
        user=DB_CONFIG["user"], 
        password=DB_CONFIG["password"], 
        host=DB_CONFIG["host"], 
        port=DB_CONFIG["port"]
    )

def seed_users(conn, num_users=10):
    cur = conn.cursor()
    user_ids = []

    for _ in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()
        
        # Вставка одного користувача та отримання його id
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;", (fullname, email))
        user_id = cur.fetchone()[0]  # Отримуємо id вставленого користувача
        user_ids.append(user_id)
        
    conn.commit()
    cur.close()
    
    print(f"Inserted {len(user_ids)} users.")
    return user_ids

def seed_tasks(conn, user_ids, num_tasks=20):
    cur = conn.cursor()
    status_ids = [1, 2, 3]  # ID статусів: new, in progress, completed
    tasks = [
        (fake.sentence(), fake.text(), random.choice(status_ids), random.choice(user_ids))
        for _ in range(num_tasks)
    ]
    cur.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);", tasks)
    conn.commit()
    cur.close()

def main():
    conn = connect_db()
    try:
        user_ids = seed_users(conn)  # Генерація користувачів та отримання їх id
        seed_tasks(conn, user_ids)   # Генерація завдань для кожного користувача
        print("Дані успішно вставлено в базу!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
