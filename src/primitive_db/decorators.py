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

def create_cacher():
    cache = {}
    
    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        else:
            result = value_func()
            cache[key] = result
            return result
    
    def clear_cache():
        cache.clear()
        print("Кэш очищен.")
    
    def get_cache_stats():
        return {
            'size': len(cache),
            'keys': list(cache.keys())
        }

    def invalidate_by_prefix(prefix):
        keys_to_remove = [k for k in list(cache.keys()) if k.startswith(prefix)]
        for key in keys_to_remove:
            del cache[key]
        return len(keys_to_remove)
    
    def invalidate_table(table_name):
        prefix = f"select:{table_name}:"
        removed = invalidate_by_prefix(prefix)
        if removed > 0:
            print(f"Очищено {removed} записей кэша для таблицы '{table_name}'")
    
    cache_result.clear = clear_cache
    cache_result.stats = get_cache_stats
    cache_result.invalidate_table = invalidate_table
    cache_result.invalidate_by_prefix = invalidate_by_prefix
    
    return cache_result