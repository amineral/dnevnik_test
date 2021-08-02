### Установка:

**python3 .../dnevnik_test/setup.py install** 

Не забудьте создать виртуальное окружение


### Команда для импорта:

* **from dnevnik.dnevnik2 import info, auth, reg, logout, create_note, show_note, delete_note**

    * Для подробной информации о командах вызвать команду **info()**



* При первом запуске создается файл data.json
    * В нем создается тестовая учетная запись: 

    * **login == "admin", password == "123456"**

    * Если файл data.json есть, то информация будет взята оттуда.

* Структура dict из data.json описана в начале файла dnevnik2.py

* После авторизации, файл data.json хранит информацию о сессии(активна или нет) и пользователе(логин пользователя)

* Обязательно после завершения работы с программой вызвать команду logout(), чтобы закрыть сессию
