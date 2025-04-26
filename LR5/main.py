import requests
from xml.etree import ElementTree as ET
from datetime import datetime


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
        self._char_codes = ['USD', 'EUR', 'GBP'] if char_codes is None else char_codes
        self._rates = {}
        self._last_update = None
        self.values = []
        self._fetch_rates()  # Убрал дублирующий вызов

    def _check_char_codes(self, char_codes):
        """Проверяет, существуют ли указанные коды валют в API ЦБ РФ"""
        if not all(isinstance(code, str) and len(code) == 3 for code in char_codes):
            return False

        try:
            response = requests.get(self.URL_XML)
            if response.status_code == 200:
                tree = ET.fromstring(response.content)
                available_codes = [el.find('CharCode').text for el in tree.findall('Valute')]
                return all(code.upper() in available_codes for code in char_codes)
            return False
        except Exception:
            return False

    def _fetch_rates(self):
        """Получает актуальные курсы валют с API ЦБ РФ"""
        try:
            # Пробуем получить данные в JSON формате
            response = requests.get(self.URL_JSON)
            response.raise_for_status()
            data = response.json()

            new_rates = {}
            for code in self._char_codes:
                if code.upper() in data['Valute']:
                    new_rates[code.upper()] = data['Valute'][code.upper()]['Value']

            self._rates = new_rates
            self._last_update = datetime.now()
            return True

        except requests.RequestException as json_error:
            # Если JSON API не работает, пробуем XML
            try:
                response = requests.get(self.URL_XML)
                response.raise_for_status()
                tree = ET.fromstring(response.content)

                new_rates = {}
                for valute in tree.findall('Valute'):
                    char_code = valute.find('CharCode').text
                    if char_code in self._char_codes:
                        value = valute.find('Value').text.replace(',', '.')
                        new_rates[char_code] = float(value)

                self._rates = new_rates
                self._last_update = datetime.now()
                return True

            except requests.RequestException as xml_error:
                print(f"Ошибка при получении курсов валют (JSON: {json_error}, XML: {xml_error})")
                return False
            except ET.ParseError:
                print("Ошибка парсинга XML ответа от ЦБ РФ")
                return False

        except ValueError as e:
            print(f"Ошибка обработки данных: {e}")
            return False

    @property
    def rates(self):
        """Возвращает текущие курсы валют"""
        return self._rates

    @property
    def char_codes(self):
        """Возвращает список отслеживаемых кодов валют"""
        return self._char_codes

    @char_codes.setter
    def char_codes(self, new_codes):
        """Устанавливает новые коды валют и обновляет курсы"""
        if not isinstance(new_codes, list):
            new_codes = [new_codes] if isinstance(new_codes, str) else list(new_codes)

        cleaned_codes = [code.upper().strip() for code in new_codes if isinstance(code, str) and len(code.strip()) == 3]

        if not cleaned_codes:
            raise ValueError("Не указаны корректные коды валют")

        if self._check_char_codes(cleaned_codes):
            self._char_codes = cleaned_codes
            self._fetch_rates()
        else:
            raise ValueError(f"Некоторые коды валют не найдены в API ЦБ РФ: {cleaned_codes}")

    @property
    def last_update(self):
        """Возвращает время последнего обновления"""
        return self._last_update

    @last_update.setter
    def last_update(self, value):
        """Устанавливает время последнего обновления"""
        if isinstance(value, datetime):
            self._last_update = value
        else:
            raise ValueError("last_update должен быть объектом datetime")