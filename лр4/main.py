import requests
from xml.etree import ElementTree
from datetime import datetime


class CurrencyRates:
    _instance = None
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"

    def __new__(cls, char_codes=None):
        if cls._instance is None:
            cls._instance = super(CurrencyRates, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, char_codes=None):
        if not self._initialized:
            self._char_codes = char_codes or ['USD', 'EUR', 'GBP']
            self._rates = {}
            self.update_rates()
            self._initialized = True

    def update_rates(self):
        try:
            response = requests.get(self.URL, timeout=10)
            response.raise_for_status()

            tree = ElementTree.fromstring(response.content)
            self._rates = {}
            update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for valute in tree.findall('.//Valute'):
                char_code = valute.find('CharCode').text
                if char_code in self._char_codes:
                    value = float(valute.find('Value').text.replace(',', '.'))
                    nominal = int(valute.find('Nominal').text)
                    self._rates[char_code] = {
                        'value': round(value / nominal, 4),
                        'name': valute.find('Name').text,
                        'date': update_time
                    }
            return True
        except Exception as e:
            print(f"Ошибка при загрузке курсов: {e}")
            return False

    def get_all_rates(self):
        if not self._rates:
            print("Нет данных о курсах")  # Добавим лог
            return []
        return [
            (code, info['name'], info['value'], info['date'])
            for code, info in self._rates.items()
        ]

    @property
    def char_codes(self):
        return self._char_codes

    @char_codes.setter
    def char_codes(self, new_codes):
        self._char_codes = new_codes
        self.update_rates()