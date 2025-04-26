import sqlite3
from datetime import datetime


class CurrencyRatesCRUD:
    def __init__(self, currency_rates_obj):
        self.__con = sqlite3.connect('data.sqlite3', check_same_thread=False)
        self.__create_table()
        self.__cursor = self.__con.cursor()
        self.__currency_rates_obj = currency_rates_obj

    def __create_table(self):
        self.__con.execute(
            "CREATE TABLE IF NOT EXISTS currency("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "cur TEXT,"
            "date TEXT,"
            "value FLOAT);")
        self.__con.commit()

    def __prepare_data(self):
        """Преобразует данные из self.__currency_rates_obj в формат для БД"""
        if not hasattr(self.__currency_rates_obj, 'rates') or not self.__currency_rates_obj.rates:
            return None

        return [
            (code, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), value)
            for code, value in self.__currency_rates_obj.rates.items()
        ]

    def create(self, data=None):
        try:
            if data is None:
                # Автоматически генерируем данные из текущих курсов
                data = self.__prepare_data()
                if not data:
                    print("Нет данных для записи: курсы валют не загружены")
                    return False

            if not data:
                print("Нет данных для записи: передан пустой список")
                return False

            # Удаляем старые данные перед записью новых
            self.__cursor.execute("DELETE FROM currency")

            # Используем параметризованный запрос
            self.__cursor.executemany(
                "INSERT INTO currency (cur, date, value) VALUES (?, ?, ?)",
                data
            )
            self.__con.commit()
            print(f"Успешно записано {len(data)} записей")
            return True

        except Exception as e:
            print(f"Ошибка при записи в БД: {str(e)}")
            self.__con.rollback()
            return False

    def read(self, char_code=None):
        try:
            if char_code:
                self.__cursor.execute(
                    "SELECT cur, date, value FROM currency WHERE cur = ? ORDER BY date DESC",
                    (char_code,))
            else:
                self.__cursor.execute(
                    "SELECT cur, date, value FROM currency ORDER BY date DESC")

            return self.__cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Ошибка при чтении из БД: {str(e)}")
            return []

    def update(self, new_data):
        """Алиас для create() с очисткой старых данных"""
        return self.create(new_data)

    def delete(self, currency_code=None):
        try:
            if currency_code:
                self.__cursor.execute(
                    "DELETE FROM currency WHERE cur = ?", (currency_code,))
            else:
                self.__cursor.execute("DELETE FROM currency")

            deleted_rows = self.__cursor.rowcount
            self.__con.commit()
            print(f"Удалено {deleted_rows} записей")
            return deleted_rows

        except Exception as e:
            print(f"Ошибка при удалении: {str(e)}")
            self.__con.rollback()
            return 0

    def close(self):
        self.__con.close()