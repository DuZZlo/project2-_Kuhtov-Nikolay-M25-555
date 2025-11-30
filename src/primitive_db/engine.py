import prompt


def welcome():
    """Функция приветствия и игрового цикла"""
    print("Первая попытка запустить проект!")
    print("***")
    # Игровой цикл
    while True:
        user_input = prompt.string("Введите команду: ")
        
        if user_input == 'exit':
            print("Выход из программы...")
            break
        elif user_input == 'help':
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            print(f"Неизвестная команда: {user_input}")