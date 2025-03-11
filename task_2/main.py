from pymongo import MongoClient
import random

# Підключення до MongoDB
client = MongoClient("mongodb+srv://kiti:CM6Z6Dd3cjz*RRs@cluster0.5vz2t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["cat_database"]
collection = db["cats"]

# Функція для додавання нового кота
def add_cat(name, age, features):
    new_cat = {"name": name, "age": age, "features": features}
    collection.insert_one(new_cat)
    print(f"Кіт {name} доданий.")

# Функція для автоматичного створення 5 котів, якщо база порожня
def initialize_cats():
    if collection.count_documents({}) == 0:  # Перевіряємо, чи порожня база
        names = ["Барсик", "Мурчик", "Сніжок", "Рижик", "Том"]
        features_list = [
            ["грається з м'ячем", "любить рибу", "білий"],
            ["спить на підвіконні", "чорний", "муркотить голосно"],
            ["ходить в капці", "дає себе гладити", "рудий"],
            ["стрибає на стіл", "полюбляє молоко", "сіро-білий"],
            ["грається з лазерною указкою", "чорний", "хвостатий"]
        ]
        for i in range(5):
            add_cat(names[i], random.randint(1, 10), features_list[i])
        print("База даних була порожня, тому додано 5 випадкових котів.")

# Функція для виведення всіх записів
def get_all_cats():
    cats = collection.find()
    found = False
    for cat in cats:
        print(cat)
        found = True
    if not found:
        print("База даних порожня.")

# Функція для пошуку кота за ім'ям
def get_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print("Кота з таким ім'ям не знайдено.")

# Функція для оновлення віку кота за ім'ям
def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count:
        print(f"Вік кота {name} оновлено до {new_age}.")
    else:
        print("Кота з таким ім'ям не знайдено.")

# Функція для додавання нової характеристики
def add_feature_to_cat(name, feature):
    result = collection.update_one({"name": name}, {"$push": {"features": feature}})
    if result.matched_count:
        print(f"До кота {name} додано характеристику: {feature}.")
    else:
        print("Кота з таким ім'ям не знайдено.")

# Функція для видалення кота за ім'ям
def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"Кіт {name} видалений.")
    else:
        print("Кота з таким ім'ям не знайдено.")

# Функція для видалення всіх записів
def delete_all_cats():
    result = collection.delete_many({})
    print(f"Видалено {result.deleted_count} записів.")

# Головне меню
if __name__ == "__main__":
    initialize_cats()  # Додаємо котів, якщо база порожня

    while True:
        print("\n1. Показати всіх котів")
        print("2. Знайти кота за ім'ям")
        print("3. Оновити вік кота")
        print("4. Додати характеристику коту")
        print("5. Видалити кота за ім'ям")
        print("6. Видалити всіх котів")
        print("7. Додати кота")
        print("8. Вийти")

        choice = input("Оберіть опцію: ").strip()

        if choice == "1":
            get_all_cats()
        elif choice == "2":
            name = input("Введіть ім'я кота: ").strip()
            get_cat_by_name(name)
        elif choice == "3":
            name = input("Введіть ім'я кота: ").strip()
            age = input("Введіть новий вік: ").strip()
            if age.isdigit():
                update_cat_age(name, int(age))
            else:
                print("Помилка: Вік має бути числом.")
        elif choice == "4":
            name = input("Введіть ім'я кота: ").strip()
            feature = input("Введіть нову характеристику: ").strip()
            add_feature_to_cat(name, feature)
        elif choice == "5":
            name = input("Введіть ім'я кота: ").strip()
            delete_cat_by_name(name)
        elif choice == "6":
            delete_all_cats()
        elif choice == "7":
            name = input("Введіть ім'я кота: ").strip()
            age = input("Введіть вік кота: ").strip()
            features = input("Введіть характеристики (через кому): ").strip().split(", ")
            if age.isdigit():
                add_cat(name, int(age), features)
            else:
                print("Помилка: Вік має бути числом.")
        elif choice == "8":
            print("Вихід...")
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")
