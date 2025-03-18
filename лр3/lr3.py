import sys
import functools
import sqlite3
import json
from datetime import datetime


# Функция-декоратор
def trace(func=None, *, handle=sys.stdout):
    print("func - > ", func)
    if func is None:
        return lambda func: trace(func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                'datetime': now,
                'func_name': func.__name__,
                'params': args,
                'result': result
            }

            if isinstance(handle, str) and handle.endswith('.json'):
                with open(handle, 'a+') as file:
                    json.dump(data, file, indent=4)
                    file.write('\n')
            elif isinstance(handle, sqlite3.Connection):
                cursor = handle.cursor()
                cursor.execute('''INSERT INTO logtable(datetime, func_name, params, result) 
                                  VALUES (?, ?, ?, ?)''',
                               (now, func.__name__, str(args), str(result)))
                handle.commit()
            else:
                handle.write(f'{data}\n')

            return result

        except Exception as e:
            raise e

    return inner


# Создание таблиц в базе данных SQLite
def create_log_table(con: sqlite3.Connection):
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logtable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            func_name TEXT,
            params TEXT,
            result TEXT
        )
    ''')
    con.commit()


# Отображаем логи из базы данных
def showlogs(con: sqlite3.Connection):
    cursor = con.cursor()
    cursor.execute('SELECT * FROM logtable')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# Функции для тестирования
@trace(handle=sys.stderr)  # Логирование в stderr
def increm(x):
    """Инкремент"""
    return x + 1


@trace(handle=sys.stdout)  # Логирование в stdout
def decrem(x):
    """Декремент"""
    return x - 1


@trace(handle='logger.json')  # Логирование в JSON-файл
def f3(x):
    return x ** 3


# Подключение к базе данных SQLite в памяти
con = sqlite3.connect(':memory:')
create_log_table(con)

cur = con.execute("INSERT INTO logtable (datetime, func_name, params, result) VALUES ('2023-01-01', 'foobar', '2', '4')")

@trace(handle=con)
def f4(x):
    return x ** 4


increm(10)
decrem(20)
f3(30)
f4(40)

showlogs(con)