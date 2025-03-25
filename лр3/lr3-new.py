import sys
import functools
import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager


# Функция-декоратор
def trace(func=None, *, handle=sys.stdout):
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
                cursor.execute('''CREATE TABLE IF NOT EXISTS logtable (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    datetime TEXT,
                                    func_name TEXT,
                                    params TEXT,
                                    result TEXT
                                )''')
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


@contextmanager
def dbc():
    con = sqlite3.connect(':memory:')
    try:
        yield con
    finally:
        con.close()


@trace(handle=sys.stderr)
def increm(x):
    """Инкремент"""
    return x + 1


@trace(handle=sys.stdout)
def decrem(x):
    """Декремент"""
    return x - 1


@trace(handle='logger.json')
def f3(x):
    return x ** 3



with dbc() as con:
    @trace(handle=con)
    def f4(x):
        return x ** 4


    increm(10)
    decrem(20)
    f3(30)
    f4(40)

    cursor = con.cursor()
    cursor.execute('SELECT * FROM logtable')
    for row in cursor.fetchall():
        print(row)

    print(f4(10))