import shlex

import prompt

from . import core, utils

METADATA_FILE = utils.get_metadata_path()

def run():
    print("***Процесс работы с таблицей***")
    
    metadata = utils.load_metadata(METADATA_FILE)
    
    while True:
        user_input = prompt.string("Введите команду: ").strip()
        
        if not user_input:
            continue
            
        if user_input == 'exit' or user_input == 'quit':
            print("Выход из программы...")
            break

        elif user_input == 'help':
            print_help()

        elif user_input == 'list_tables':
            core.list_tables(metadata)

        elif user_input.startswith('create_table '):
            args = shlex.split(user_input)
            if len(args) < 3:
                print("Ошибка: Формат: create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...")
            else:
                result = core.create_table(metadata, args[1], args[2:])
                if result is not None:
                    metadata = result
                    utils.save_metadata(METADATA_FILE, metadata)

        elif user_input.startswith('drop_table '):
            args = shlex.split(user_input)
            if len(args) < 2:
                print("Ошибка: Формат: drop_table <имя_таблицы>")
            else:
                table_name = args[1]
                
                try:
                    filepath = utils.get_table_filepath(table_name)
                    if filepath.exists():
                        filepath.unlink()
                        print(f"Файл данных удален: {filepath}")
                except OSError as e:
                    print(f"Предупреждение: Не удалось удалить файл данных: {e}")
                
                result = core.drop_table(metadata, table_name)
                if result is not None:
                    metadata = result
                    utils.save_metadata(METADATA_FILE, metadata)

        elif user_input.startswith('insert into '):
            args = shlex.split(user_input)
            if len(args) >= 4 and args[0] == 'insert' and args[1] == 'into':
                table_name = args[2]
                values = args[3:]
                table_data = utils.load_table_data(table_name)
                result = core.insert(metadata, table_name, values, table_data)
                if result is not None:
                    utils.save_table_data(table_name, result)
            else:
                print("Ошибка: Формат: insert into <таблица> <значение1> <значение2> ...")

        elif user_input.startswith('select from '):
            args = shlex.split(user_input)
            if len(args) >= 3 and args[0] == 'select' and args[1] == 'from':
                table_name = args[2]
                where_str = None
                
                # Проверяем, есть ли условие WHERE
                if len(args) >= 5 and args[3].upper() == 'WHERE':
                    where_str = ' '.join(args[4:])
                elif len(args) >= 4:
                    # Если аргументов 4 или больше, но нет WHERE, считаем все аргументы условием
                    where_str = ' '.join(args[3:])
                
                table_data = utils.load_table_data(table_name)
                core.execute_select(metadata, table_name, where_str, table_data)
            else:
                print("Ошибка: Формат: select from <таблица> [WHERE условие]")

        elif user_input.startswith('update '):
            args = shlex.split(user_input)
            if len(args) >= 4:
                table_name = args[1]
                
                set_index = -1
                where_index = -1
                for i, arg in enumerate(args):
                    if arg.upper() == 'SET':
                        set_index = i
                    elif arg.upper() == 'WHERE':
                        where_index = i
                
                if set_index == -1:
                    print("Ошибка: Не найден SET clause")
                    continue
                
                if where_index == -1:
                    print("Ошибка: Не найден WHERE clause")
                    continue
                
                set_str = ' '.join(args[set_index+1:where_index])
                where_str = ' '.join(args[where_index+1:])
                
                table_data = utils.load_table_data(table_name)
                result = core.execute_update(metadata, table_name, set_str, where_str, table_data)
                if result is not None:
                    utils.save_table_data(table_name, result)
            else:
                print("Ошибка: Формат: update <таблица> SET <колонка=значение> WHERE <условие>")

        elif user_input.startswith('delete from '):
            args = shlex.split(user_input)
            if len(args) >= 5 and args[0] == 'delete' and args[1] == 'from' and args[3].upper() == 'WHERE':
                table_name = args[2]
                where_str = ' '.join(args[4:])
                table_data = utils.load_table_data(table_name)
                result = core.execute_delete(metadata, table_name, where_str, table_data)
                if result is not None:
                    utils.save_table_data(table_name, result)
            else:
                print("Ошибка: Формат: delete from <таблица> WHERE <условие>")

        elif user_input.startswith('info '):
            args = shlex.split(user_input)
            if len(args) >= 2:
                table_name = args[1]
                table_data = utils.load_table_data(table_name)
                core.show_table_info(metadata, table_name, table_data)
            else:
                print("Ошибка: Формат: info <имя_таблицы>")
        else:
            print(f"Неизвестная команда: {user_input}")

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("list_tables - показать список всех таблиц")
    print("drop_table <имя_таблицы> - удалить таблицу")

    print("\nОперации c данными:")
    print("insert into <имя_таблицы> <значение1> <значение2> ... - создать запись.")
    print("select from <имя_таблицы> WHERE <условие> - прочитать записи по условию.")
    print("select from <имя_таблицы> - прочитать все записи.")
    print("update <имя_таблицы> SET <колонка=значение> WHERE <условие> - обновить запись.")
    print("delete from <имя_таблицы> WHERE <условие> - удалить запись.")
    print("info <имя_таблицы> - вывести информацию о таблице.")
    
    print("\nОбщие команды:")
    print("exit | quit - выход из программы")
    print("help - справочная информация\n")