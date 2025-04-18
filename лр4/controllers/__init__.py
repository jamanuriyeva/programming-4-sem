import sqlite3


class CurrencyRatesCRUD:
    def __init__(self, currency_rates_obj):
        self.__connection = sqlite3.connect('data.sqlite3')
        self.cursor = self.__connection.cursor()
        self.currency_rates = currency_rates_obj
        self._create_table()

    def _create_table(self):
        self.__connection.execute(
            "CREATE TABLE IF NOT EXISTS currency("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "cur TEXT,"
            "date TEXT,"
            "value FLOAT);")
        self.__connection.commit()

    def create(self, data=None):
        try:
            if data is None:
                raw_data = self.currency_rates.get_all_rates()
                data = [
                    {
                        'char_code': item[0],
                        'name': item[1],
                        'value': item[2],
                        'date': item[3]
                    }
                    for item in raw_data
                ]

            if not data:
                print("Нет данных для записи")
                return False

            sql = """
                INSERT INTO currency_rates 
                (char_code, name, value, date)
                VALUES (:char_code, :name, :value, :date)
            """

            self.cursor.executemany(sql, data)
            self.__connection.commit()
            print(f"Успешно записано {len(data)} записей (именованный стиль)")
            return True

        except Exception as e:
            print(f"Ошибка при записи в БД (именованный стиль): {e}")
            self.__connection.rollback()
            return False

    def read(self, char_code=None):
        try:
            if char_code:
                self.cursor.execute("""
                    SELECT char_code, name, value, date 
                    FROM currency_rates 
                    WHERE char_code = ?
                    ORDER BY date DESC
                """, (char_code,))
            else:
                self.cursor.execute("""
                    SELECT char_code, name, value, date 
                    FROM currency_rates 
                    ORDER BY date DESC
                """)
            result = self.cursor.fetchall()
            return result if result else []
        except sqlite3.Error as e:
            print(f"Ошибка при чтении из БД: {e}")
            return []

    def update_rates(self):
        try:
            if not self.currency_rates.update_rates():
                return False
            return self.create()
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            return False

    def close(self):
        try:
            self.__connection.close()
            print("Соединение с БД закрыто")
        except sqlite3.Error as e:
            print(f"Ошибка при закрытии соединения: {e}")


class ViewController:
    def __init__(self, currency_rates):
        pass
        self.currency_name = currency_rates.values[0]
        self.currency_date = currency_rates.values[1]
        self.currency_value = currency_rates.values[2]

    def __call__(self):
        return f"{self.currency_name} - {self.currency_date} - {self.currency_value}"

