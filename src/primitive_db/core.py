from prettytable import PrettyTable

from . import parser
from .decorators import confirm_action, handle_db_errors, log_time, create_cacher

query_cache = create_cacher()

@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает новую таблицу в метаданных."""
    
    if table_name in metadata:
        print(f"Ошибка: Таблица '{table_name}' уже существует.")
        return None
    
    formatted_columns = ["ID:int"]

    for column_def in columns:
        if ':' not in column_def:
            print(f"Ошибка: Неверный формат столбца '{column_def}'. Используйте 'имя:тип'")
            return None
        
        col_name, col_type = column_def.split(':', 1)
        col_type = col_type.strip().lower()
        
        if col_type not in ('int', 'str', 'bool'):
            print(f"Ошибка: Неподдерживаемый тип данных '{col_type}' в столбце '{col_name}'. "
                  f"Допустимые типы: int, str, bool")
            return None
        
        formatted_columns.append(f"{col_name.strip()}:{col_type}")
    
    metadata[table_name] = formatted_columns
    print(f"Таблица '{table_name}' успешно создана.")
    return metadata

@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""

    del metadata[table_name]
    print(f"Таблица '{table_name}' успешно удалена из метаданных.")
    return metadata

@handle_db_errors
@log_time
def list_tables(metadata):
    """Выводит список всех таблиц в базе данных."""
    
    if not metadata:
        print("В базе данных нет таблиц.")
        return
    
    table = PrettyTable()
    table.field_names = ["Имя таблицы", "Колонки", "Файл данных"]
    table.align = "l"

    for table_name, columns in metadata.items():
        columns_str = ", ".join(columns)
        data_file = f"data/{table_name}.json"
        table.add_row([table_name, columns_str, data_file])
    
    print("\nСписок таблиц:")
    print(table)

@handle_db_errors
@log_time
def insert(metadata, table_name, values, table_data):
    """Добавляет новую запись в таблицу."""

    columns = metadata[table_name]

    expected_count = len(columns) - 1  # минус ID
    if len(values) != expected_count:
        print(f"Ошибка: Ожидается {expected_count} значений, получено {len(values)}")
        print(f"Структура таблицы: {', '.join(columns)}")
        return None

    if table_data:
        max_id = 0
        for row in table_data:
            row_id = row.get('ID', 0)
            if isinstance(row_id, (int, float)):
                max_id = max(max_id, int(row_id))
        new_id = max_id + 1
    else:
        new_id = 1

    new_row = {'ID': new_id}

    for i, col_def in enumerate(columns[1:]):  
        col_name, expected_type = parser._parse_column_def(col_def)
        value = values[i]
        
        is_valid, validated_value = _validate_value_type(value, expected_type)
        if not is_valid:
            print(f"Ошибка валидации для колонки '{col_name}': {validated_value}")
            return None
        
        new_row[col_name] = validated_value

    table_data.append(new_row)
    
    query_cache.invalidate_table(table_name)

    print(f"Запись с ID={new_id} успешно добавлена в таблицу '{table_name}'")
    return table_data

def _validate_value_type(value, expected_type):
    """Проверяет и преобразует значение к указанному типу."""
    
    if expected_type == 'int':
        try:
            int_value = int(value)
            return True, int_value
        except (ValueError, TypeError):
            return False, f"Ожидается int, получено: {value}"
    
    elif expected_type == 'bool':
        value_lower = value.lower()
        if value_lower in ('true', '1', 'yes', 'да'):
            return True, True
        elif value_lower in ('false', '0', 'no', 'нет'):
            return True, False
        return False, f"Ожидается bool, получено: {value}"
    
    elif expected_type == 'str':
        return True, str(value)
    
    return False, f"Неизвестный тип: {expected_type}"

@handle_db_errors
@log_time
def execute_select(metadata, table_name, where_str=None, table_data=None):
    """Выполняет SELECT запрос и выводит результаты."""

    where_clause = parser._parse_where_clause(where_str) if where_str else {}
    
    cache_key = f"select:{table_name}:{str(sorted(where_clause.items()))}"
    
    results = query_cache(cache_key, lambda: select(table_data, where_clause))
    
    table = PrettyTable()
    columns = metadata[table_name]
    column_names = [parser._parse_column_def(col)[0] for col in columns]
    table.field_names = column_names
    
    for row in results:
        row_data = [str(row.get(col, "")) for col in column_names]
        table.add_row(row_data)
    
    if results:
        print(f"\nРезультаты SELECT из таблицы '{table_name}' ({len(results)} записей):")
        print(table)
    else:
        print(f"\nВ таблице '{table_name}' не найдено записей, соответствующих условию.")
    
    return True

@handle_db_errors
def select(table_data, where_clause=None):
    """Выбирает записи из таблицы по условию WHERE."""
    
    if where_clause is None:
        where_clause = {}
    
    return _apply_where_clause(table_data, where_clause)

def _apply_where_clause(table_data, where_clause):
    """Применяет условие WHERE к данным таблицы."""
    
    if not where_clause:
        return table_data
    
    filtered_data = []
    for row in table_data:
        match = True
        for key, expected_value in where_clause.items():
            if key not in row or str(row[key]) != str(expected_value):
                match = False
                break
        if match:
            filtered_data.append(row)
    
    return filtered_data

@handle_db_errors
@log_time
def execute_update(metadata, table_name, set_str, where_str, table_data):
    """Выполняет UPDATE запрос."""

    set_clause = parser._parse_set_clause(set_str)
    where_clause = parser._parse_where_clause(where_str)
    
    columns = metadata[table_name]
    column_names = [parser._parse_column_def(col)[0] for col in columns]
    
    for col in set_clause.keys():
        if col not in column_names and col != 'ID':
            print(f"Ошибка: Колонка '{col}' не существует в таблице '{table_name}'")
            print(f"Доступные колонки: {', '.join(column_names)}")
            return None
    
    updated_data = update(table_data, set_clause, where_clause, table_name)
    
    query_cache.invalidate_table(table_name)

    return updated_data

@handle_db_errors
def update(table_data, set_clause, where_clause, table_name):
    """Обновляет записи в таблице по условию WHERE."""
    
    if not set_clause:
        print("Ошибка: Не указано что обновлять (SET clause)")
        return table_data
    
    if not where_clause:
        print("Предупреждение: WHERE clause не указан, будут обновлены ВСЕ записи")
        confirm = input("Вы уверены? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Обновление отменено")
            return table_data
    
    updated_ids = []
    for row in table_data:
        match = True
        for key, expected_value in where_clause.items():
            if key not in row or str(row[key]) != str(expected_value):
                match = False
                break
        
        if match:
            for key, new_value in set_clause.items():
                if key in row:
                    row[key] = new_value
            updated_ids.append(row.get('ID', ''))
    
    if updated_ids:
        if len(updated_ids) == 1:
            print(f'Запись с ID={updated_ids[0]} в таблице "{table_name}" успешно обновлена.')
        else:
            ids_str = ', '.join(str(id) for id in updated_ids)
            print(f'Записи с ID={ids_str} в таблице "{table_name}" успешно обновлены.')
    else:
        print("Не найдено записей для обновления.")
    
    return table_data

@handle_db_errors
@confirm_action("удаление строк(и)")
@log_time
def execute_delete(metadata, table_name, where_str, table_data):
    """Выполняет DELETE запрос."""

    if table_name not in metadata:
        # Это вызовет KeyError, который перехватит декоратор
        raise KeyError(f"Таблица '{table_name}' не существует.")

    where_clause = parser._parse_where_clause(where_str)
    if not where_clause:
        print("Ошибка: WHERE clause обязателен для DELETE")
        return None
    
    new_data = delete(table_data, where_clause, table_name)
    
    query_cache.invalidate_table(table_name)

    return new_data

@handle_db_errors
def delete(table_data, where_clause, table_name):
    """Удаляет записи из таблицы по условию WHERE."""
    
    if not where_clause:
        print("Ошибка: WHERE clause обязателен для операции DELETE")
        return table_data

    records_to_delete = _apply_where_clause(table_data, where_clause)
    
    if not records_to_delete:
        print("Не найдено записей для удаления")
        return table_data

    deleted_ids = [record.get('ID', '') for record in records_to_delete]

    new_data = [row for row in table_data if row not in records_to_delete]
    
    if deleted_ids:
        if len(deleted_ids) == 1:
            print(f'Запись с ID={deleted_ids[0]} в таблице "{table_name}" успешно удалена.')
        else:
            ids_str = ', '.join(str(id) for id in deleted_ids)
            print(f'Записи с ID={ids_str} в таблице "{table_name}" успешно удалены.')

    return new_data

@handle_db_errors
@log_time
def show_table_info(metadata, table_name, table_data=None):
    """Показывает информацию о таблице."""

    columns = metadata[table_name]
    record_count = len(table_data) if table_data else 0
    
    print(f"\nТаблица: {table_name}")
    print(f"Столбцы: {', '.join(columns)}")
    print(f"Количество записей: {record_count}")
    
    return True