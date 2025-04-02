import requests
from xml.etree import ElementTree


class Singleton(type):
    """(Одиночка)"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class CurrencyRates(metaclass=Singleton):
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"
    CODES = {"USD": "R01235", "EUR": "R01239", "GBP": "R01035"}

    def __init__(self, char_codes=None):
        if char_codes is None:
            char_codes = ['USD', 'EUR', 'GBP']

        self._rates = {}
        self._char_codes = []

        self.char_codes = char_codes
        self._fetch_rates()

    @property
    def rates(self):
        """Геттер для словаря с курсами валют"""
        return self._rates.copy()

    @property
    def char_codes(self):
        """Геттер для списка кодов валют"""
        return self._char_codes.copy()

    @char_codes.setter
    def char_codes(self, new_codes):
        """Сеттер для списка кодов валют с валидацией"""
        if not isinstance(new_codes, (list, tuple)):
            raise TypeError("Коды валют должны быть переданы в виде списка или кортежа")

        if not new_codes:
            raise ValueError("Должен быть указан хотя бы один код валюты")

        valid_codes = self._get_available_codes()
        invalid_codes = [code for code in new_codes if code not in valid_codes]

        if invalid_codes:
            raise ValueError(f"Недопустимые коды валют: {', '.join(invalid_codes)}")

        self._char_codes = list(new_codes)
        self._fetch_rates()

    @char_codes.deleter
    def char_codes(self):
        """Делитер для списка кодов валют"""
        raise AttributeError("Невозможно удалить атрибут char_codes")

    def _get_available_codes(self):
        """Вспомогательный метод для получения всех доступных кодов валют с сайта ЦБ"""
        response = requests.get(self.URL)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            return [elem.text for elem in tree.findall('.//CharCode')]
        raise ConnectionError("Не удалось получить доступные коды валют с сайта ЦБ")

    def _fetch_rates(self):
        """Получение текущих курсов валют с сайта ЦБ"""
        response = requests.get(self.URL)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            self._rates = {}

            for valute in tree.findall('.//Valute'):
                char_code = valute.find('CharCode').text
                if char_code in self._char_codes:
                    value = valute.find('Value').text.replace(",", ".")
                    nominal = int(valute.find('Nominal').text)
                    self._rates[char_code] = float(value) / nominal
        else:
            raise ConnectionError("Не удалось получить курсы валют с сайта ЦБ")


if __name__ == "__main__":
    rates1 = CurrencyRates(['USD', 'EUR'])
    print("Курсы из первого экземпляра:", rates1.rates)

    rates2 = CurrencyRates()
    print("Курсы из второго экземпляра:", rates2.rates)

    rates2.char_codes = ['USD', 'GBP']
    print("Обновленные курсы:", rates2.rates)

    print("Первый экземпляр после изменения:", rates1.rates)

    try:
        rates1.char_codes = ['USD', 'XYZ']
    except ValueError as e:
        print(f"Ошибка: {e}")