import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, CurrencyRate


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class CurrencyRates(metaclass=Singleton):
    URL_JSON = "https://www.cbr-xml-daily.ru/daily_json.js"
    URL_XML = "https://www.cbr.ru/scripts/XML_daily.asp"

    def __init__(self, char_codes=None):
        self._char_codes = ['USD', 'EUR'] if char_codes is None else char_codes
        self._rates = {}
        self._last_update = None
        self.values = []
        self._fetch_rates()

    def _fetch_rates(self):
        try:
            response = requests.get(self.URL_JSON)
            data = response.json()

            self._rates = {}
            self.values = []

            for code in self._char_codes:
                if code in data['Valute']:
                    rate = data['Valute'][code]['Value']
                    self._rates[code] = rate
                    self.values.append((
                        code,
                        datetime.now().strftime('%d-%m-%Y %H:%M'),
                        str(rate)
                    ))

            self._last_update = datetime.now()
            return True
        except Exception as e:
            print(f"Ошибка получения курсов: {e}")
            return False

    @property
    def rates(self):
        return self._rates

    @property
    def char_codes(self):
        return self._char_codes

    @char_codes.setter
    def char_codes(self, new_codes):
        if isinstance(new_codes, str):
            new_codes = [code.strip().upper() for code in new_codes.split(',')]

        self._char_codes = new_codes
        self._fetch_rates()

    @property
    def last_update(self):
        return self._last_update