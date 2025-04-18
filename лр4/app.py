from main import CurrencyRates
from controllers import CurrencyRatesCRUD
from controllers import ViewController

def main():

    c_r = CurrencyRates(['USD', 'EUR', 'GBP', 'AZN'])
    c_r.values = [("USD", "02-04-2025 11:10", "90"),
              ("EUR", "02-04-2025 11:11", "91"),
              ("GBP", '02-04-2025 11:37', '100')]

    c_r_controller = CurrencyRatesCRUD(c_r)
    c_r_controller.create()
    output = ViewController(c_r)

    print(output())

    print("\nАктуальные курсы валют:")
    current_rates = c_r.get_all_rates()
    for code, name, value, date in current_rates:
        print(f"{code} ({name}): {value} руб. (на {date})")

input("Проверка добавилось ли")


if __name__ == "__main__":
    main()