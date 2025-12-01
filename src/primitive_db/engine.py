import prompt
import core
import utils
import shlex

METADATA_FILE = "db_meta.json"

def run():
    print("***Процесс работы с таблицей***")
    
    metadata = utils.load_metadata(METADATA_FILE)
    while True:
        user_input = prompt.string("Введите команду: ").strip()
        
        if user_input == 'exit' or user_input == 'quit':
            print("Выход из программы...")
            break

        elif user_input == 'help':
            print_help()

        elif user_input == 'list_tables':
            core.list_tables(metadata)

        elif user_input.startswith('create_table '):
            #args = user_input[len('create_table '):].strip().split()
            args = shlex.split(user_input)
            if len(args) < 3:
                print("ошибка")
            else:
                result = core.create_table(metadata, args[1], args[2:])
                if result is not None:
                    metadata = result
                    utils.save_metadata(METADATA_FILE, metadata)

        elif user_input.startswith('drop_table '):
            table_name = shlex.split(user_input)[1]
            if table_name:
                result = core.drop_table(metadata, table_name)
                if result is not None:
                    metadata = result
                    utils.save_metadata(METADATA_FILE, metadata)

        else:
            print(f"Неизвестная команда: {user_input}")

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit | quit - выход из программы")
    print("<command> help - справочная информация\n")