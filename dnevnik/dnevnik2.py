import json
import datetime
import sys

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
        "auth" : [False, None]
    }

def save_data():    
    with open('data.json', 'w') as database:
        json.dump(data, database)

def info():
    print(
        """
        Перед началом работы залогиньтесь с помощью команды auth(login, password)
        Список команд:
        
        auth(login, password)                   Авторизация

        reg(login=None, password=None)          Регистрация.
                                                Возможен вызов без агрументов

        create_note(title=None, text=None)      Создать запись.
                                                Возможен вызов без аргументов

        show_notes()                            Посмотреть записи

        delete_note(id=None)                    Удалить запись.
                                                Возможен вызов без аргументов
        
        logout()                                Разлогиниться    

        ПО ОКОНЧАНИЮ РАБОТЫ НЕ ЗАБУДЬТЕ РАЗЛОГИНИТЬСЯ!                               
        """
    )

def reg(login=None, password=None):
    if data["auth"][0] == False:
        if not login:
            login = input("Придумай логин: ")
        if not login in data["users"][0]:
            if not password:
                password = input("Придумай пароль: ")
            new_user = [False, login, password, len(data["users"]), {}, None] #структура для ключа. Ключ словаря - логин пользователя
            data["users"][0][login] = new_user
            #print(data["users"])
            print("Вы успешно зарегистрировались!")
            save_data()
        else:
            print("Такой пользователь уже существует")
    else:
        print("Сейчас кто-то авторизован. Напишите команду logout()")

def auth(login, password):
    if data["auth"][0] == False:
        if login in data["users"][0]:
            user = data["users"][0][login]
            if password == user[2]:
                data["auth"][0] = True
                data["auth"][1] = login
                save_data()
                print("Вы авторизованы")
                print("--------------------------------------------")
                print("ПО ОКОНЧАНИЮ РАБОТЫ НЕ ЗАБУДЬТЕ РАЗЛОГИНИТЬСЯ!")
                print("--------------------------------------------")
            else:
                print("Неправильный пароль")
        else:
            print("Такого пользователя нет")
    else:
        print("Сейчас авторизован пользователь", data["auth"][1])
        print("Если это не вы, напишите команду logout()")


def logout():
    if data["auth"][0] == True:
        data["auth"][0] = False
        data["auth"][1] = None
        save_data()
    print("Вы успешно разлогинились")

def create_note(title=None, text=None):
    if not data["auth"][1]:
        print("Пользователь не авторизован. Вызовите info() для справки.")
        sys.exit()
    user = data["users"][0][data["auth"][1]]
    if not title:
        title = input("Введи название записи: ")
    while title in user[4] or not title:
        if not title:
            title = input(print("Недопустимое название. Придумайте название записи: "))
        else: 
            title = input(print("Такое название уже есть, придумай другое: "))
    if not text:
        text = input("Введи текст записи: ")
    while not text:
        text = input("Введите текст записи: ")
    user[4][title] = [0, text, str(datetime.datetime.now())]
    user[4][title][0] = len(user[4])
    print("Запись создана")
    save_data()

def show_notes():
    if not data["auth"][1]:
        print("Пользователь не авторизован. Вызовите info() для справки.")
        sys.exit()
    user = data["users"][0][data["auth"][1]]
    titles = user[4] # список статей пользователя [id, title, text]
    if len(titles) == 0:
        print("Записей нет")
        sys.exit()
    while True:
        for title in titles:
            print(titles[title][0], title)
        id = input("Чтобы посмотреть запись, напиши ее номер: ")
        while not id:
            id = input("Нужно ввести номер записи: ")
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

def delete_note(id=None):
    if not data["auth"][1]:
        print("Пользователь не авторизован. Вызовите info() для справки.")
        sys.exit()
    user = data["users"][0][data["auth"][1]]
    titles = user[4] # список статей пользователя [id, title, text]
    if len(titles) == 0:
        print("Записей нет")
        sys.exit()
    for title in titles:
        print(titles[title][0], title)
    if not id:
        id = input("Чтобы удалить запись, напиши ее номер: ")
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
