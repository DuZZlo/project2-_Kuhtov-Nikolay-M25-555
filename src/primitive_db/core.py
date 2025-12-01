def create_table(metadata, table_name, columns):
    """
    Создает новую таблицу в метаданных.
    
    Args:
        metadata: Текущие метаданные базы данных
        table_name: Имя таблицы для создания
        columns: Список столбцов в формате ['столбец1:тип', 'столбец2:тип', ...]
    
    Returns:
        Обновленные метаданные или None при ошибке
    """
    # Проверяем, не существует ли уже таблица с таким именем
    if table_name in metadata:
        print(f"Ошибка: Таблица '{table_name}' уже существует.")
        return None
    
    # Автоматически добавляем столбец ID:int в начало
    formatted_columns = ["ID:int"]
    
    # Обрабатываем остальные столбцы
    for column_def in columns:
        if ':' not in column_def:
            print(f"Ошибка: Неверный формат столбца '{column_def}'. Используйте 'имя:тип'")
            return None
        
        col_name, col_type = column_def.split(':', 1)
        col_type = col_type.strip().lower()
        
        # Проверяем корректность типа данных
        if col_type not in ('int', 'str', 'bool'):
            print(f"Ошибка: Неподдерживаемый тип данных '{col_type}' в столбце '{col_name}'. "
                  f"Допустимые типы: int, str, bool")
            return None
        
        formatted_columns.append(f"{col_name.strip()}:{col_type}")
    
    # Добавляем таблицу в метаданные
    metadata[table_name] = formatted_columns
    print(f"Таблица '{table_name}' успешно создана.")
    return metadata


def drop_table(metadata, table_name):
    """
    Удаляет таблицу из метаданных.
    
    Args:
        metadata: Текущие метаданные базы данных
        table_name: Имя таблицы для удаления
    
    Returns:
        Обновленные метаданные или None при ошибке
    """
    if table_name not in metadata:
        print(f"Ошибка: Таблица '{table_name}' не существует.")
        return None
    
    del metadata[table_name]
    print(f"Таблица '{table_name}' успешно удалена.")
    return metadata


def list_tables(metadata):
    """
    Выводит список всех таблиц и их структуру.
    
    Args:
        metadata: Текущие метаданные базы данных
    """
    if not metadata:
        print("В базе данных нет таблиц.")
        return
    
    print("\nСписок таблиц:")
    print("-" * 40)
    for table_name, columns in metadata.items():
        print(f"Таблица: {table_name}")
        print(f"  Столбцы: {', '.join(columns)}")
        print("-" * 40)