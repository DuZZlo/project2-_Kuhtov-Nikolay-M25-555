# project2-_Kuhtov-Nikolay-M25-555

Демонстрация работы с таблицами:
https://asciinema.org/a/5oxu8J37q5VtLtdHiZXOLP9DU

Демонстрация CRUD операций:
https://asciinema.org/a/mcZGH9PxZOdnORBk7QKJXUWNj

Общие команды:
    exit | quit - выход из программы"
    help - справочная информация

Управление таблицами:
    create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу"
    list_tables - показать список всех таблиц"
    drop_table <имя_таблицы> - удалить таблицу"

Примеры:
    >>> database

    ***Процесс работы с таблицей***
    Функции:
    <command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
    <command> list_tables - показать список всех таблиц
    <command> drop_table <имя_таблицы> - удалить таблицу
    <command> exit - выход из программы
    <command> help - справочная информация 

    >>>Введите команду: create_table users name:str age:int is_active:bool
    Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

    >>>Введите команду: create_table users name:str
    Ошибка: Таблица "users" уже существует.

    >>>Введите команду: list_tables
    - users

    >>>Введите команду: drop_table users
    Таблица "users" успешно удалена.

    >>>Введите команду: drop_table products
    Ошибка: Таблица "products" не существует.

    >>>Введите команду: help
    ***Процесс работы с таблицей***
    Функции:
    <command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
    <command> list_tables - показать список всех таблиц
    <command> drop_table <имя_таблицы> - удалить таблицу
    <command> exit - выход из программы
    <command> help - справочная информация 

CURD операции:
    <command> insert into <имя_таблицы> (<значение1>, <значение2>, ...) - создать запись.
    <command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.
    <command> select from <имя_таблицы> - прочитать все записи.
    <command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.
    <command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.
    <command> info <имя_таблицы> - вывести информацию о таблице.