import json
import datetime

# Структура data.json
#data = {
#    "users" : [
#        {"admin" : 
#            [False, "admin", "123456", "0",
#                {
#                    "title1" : [1, "This is first title", date_created],
#                    "title2" : [2, "This is second title", date_created],
#                },
#               last_login
#            ]
#        },
#    ],
#}

# Данные хранятся в файле data.json в корне проекта.
# Если такого файла нет, 
# приложение создаст файл data.json и запишет туда тестово пользователя.

try:
    with open('data.json') as json_data:
        data = json.load(json_data)
except FileNotFoundError:
    data = {
        "users" : [
            {"admin" : 
                [False, "admin", "123456", "0",
                    {
                        "title1" : [1, "This is first title", str(datetime.datetime.now())],
                        "title2" : [2, "This is second title", str(datetime.datetime.now())],
                    },
                str(datetime.datetime.now())
                ]
            },
        ],
    }
    

def save_data():    
    with open('data.json', 'w') as database:
        json.dump(data, database)
    
user = None # сессия пользователя. Сюда будет записан авторизованный пользователь.

def registration():
    login = input("Придумай логин: ")
    if not check_login(login):
        password = input("Придумай пароль: ")
        new_user = [False, login, password, len(data["users"]), {}, None] #структура для ключа. Ключ словаря - логин пользователя
        data["users"][0][login] = new_user
        #print(data["users"])
        print("Вы успешно зарегистрировались!")
        save_data()
    else:
        print("Такой пользователь уже существует")

def create_note(user):
    title = input("Введи название записи: ")
    while title in user[4] or not title:
        if not title:
            title = input(print("Недопустимое название.Придумайте название записи: "))
        else: 
            title = input(print("Такое название уже есть, придумай другое: "))
    text = input("Введи текст записи: ")
    while not text:
        text = input("Запись не может быть пустой. Введите текст: ")
    user[4][title] = [0, text, datetime.datetime.now]
    user[4][title][0] = len(user[4][title]) + 1
    print("Запись создана")
    save_data()
    # print(user[4]) # отобразить данные по созданому пользователю

def show_notes(user):
    titles = user[4] # список статей пользователя [id, title, text]
    while True:
        for title in titles:
            print(titles[title][0], title)
        print("back")
        print("Чтобы вернуться в предыдущее меню, напишите back")
        id = input("Чтобы посмотреть запись, напиши ее номер: ")
        if id == "back":
            break
        title_exists = False
        for title in titles:
            if titles[title][0] == int(id):
                title_exists = True
                print("--------------")
                print(title, end="\n\n")
                print(titles[title][1], end="\n\n")
                print("--------------")
        if not title_exists:
            print("Такой записи нет")

def delete_note(user):
    titles = user[4] # список статей пользователя [id, title, text]
    while True:
        for title in titles:
            print(titles[title][0], title)
        print("back")
        print("Чтобы вернуться в предыдущее меню, напишите back")
        id = input("Чтобы посмотреть запись, напиши ее номер: ")
        if id == "back":
            break
        title_exists = False
        for title in titles:
            if titles[title][0] == int(id):
                title_exists = True
                to_delete = title
        sure = input("Вы уверены что хотите удалить запись? Y/n: ")
        if sure == "Y":
            del titles[title]
            print("Запись удалена")
            save_data()
        if not title_exists:
            print("Такой записи нет")

def main_menu(user):
    commands = {
    "1" : create_note,
    "2" : show_notes,
    "3" : delete_note,
    }
    print("Привет,", user[1])
    while True:
        print("Что ты хочешь сделать:")
        print("1. Создать запись")
        print("2. Посмотреть свои записи")
        print("3. Удалить запись")
        print("4. Выйти из учетной записи")
        command = input(": ")
        if command == "4":
            user[0] = False
            break
        if command in commands:
            commands[command](user)
        else:
            print("Такой команды нет")

def start():
    print("Для принудительного завершения нажмите комбинацию ctrl + c на Windows или control + c на MacOs")
    print("Несохраненные данные могут быть потеряны\n\n")
    print("Привет, это твой дневник")
    while True:
        print("Введи свои логин и пароль или напиши -reg для регистрации")
        username = input("Логин: ")
        while not check_login(username):
            if username == "-reg":
                registration()
            else:
                print("Неправильный логин. Напишите -reg для регистрации")
            username = input("Логин: ")
        user = data["users"][0][username]
        # запись пользователя в сессию 
        # user[session_status(True, False(default)), username, password, id, notes{note : [id, title, text]}]
        # дальше будет передаваться переменная user с данными авторизованного пользователя
        password = input("Пароль: ")
        while not check_password(password, user):
            print("Неправильный пароль")
            password = input("Пароль: ")
        user[0] = True # состояние сессии(False дефолтно)
        user[5] = str(datetime.datetime.now()) # запись времени входа
        # нужные выводы для проверки
        #print("session", user[0])
        #print("username", user[1])
        #print("authorized")
        save_data()
        main_menu(user)

def check_password(password, user):
    if password == user[2]:
        return True
    return False

def check_login(user):
    if user in data["users"][0]:
        return True
    return False

start()
