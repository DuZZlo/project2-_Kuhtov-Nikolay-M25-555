import time

from prompt import string


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Ошибка: Обращение к несуществующему ключу - {e}")
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except FileNotFoundError as e:
            print(f"Ошибка файла: Файл не найден - {e}")
            return None
        except Exception as e:
            print(f"Неизвестная ошибка в функции {func.__name__}: {e}")
            return None
    return wrapper

def confirm_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = string(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower()
            
            if response != 'y' and response != 'yes' and response != 'да':
                print("Операция отменена.")
                return None
            
            # Если пользователь подтвердил, выполняем функцию
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        
        print(f"Функция {func.__name__} выполнилась за {execution_time:.3f} секунд.")
        return result
    return wrapper