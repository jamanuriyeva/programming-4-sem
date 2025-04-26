# from flask import Flask, render_template, request, redirect, url_for
# from main import CurrencyRates
# from model import CurrencyRatesCRUD
# from controllers import ViewController
#
# app = Flask(__name__)
#
# # Инициализация объектов
# c_r = CurrencyRates(['USD', 'EUR'])
# c_r.values = [("USD", "02-04-2025 11:10", "90"),
#               ("EUR", "02-04-2025 11:11", "91"),
#               ("GBP", '02-04-2025 11:37', '100')]
#
# c_r_controller = CurrencyRatesCRUD(c_r)
# c_r_controller.create()  # Создаем таблицу в базе данных
#
#
# @app.route('/')
# def index():
#     # Получаем данные из базы
#     output = ViewController(c_r)
#     rates_data = output()
#     return render_template('index.html', rates=rates_data)
#
#
# @app.route('/add', methods=['GET', 'POST'])
# def add_rate():
#     if request.method == 'POST':
#         # Получаем данные из формы
#         currency = request.form['currency']
#         date = request.form['date']
#         value = request.form['value']
#
#         # Добавляем новую запись
#         c_r.values.append((currency, date, value))
#         c_r_controller.create()  # Обновляем базу данных
#
#         return redirect(url_for('index'))
#
#     return render_template('update.html')
#
#
# @app.route('/delete/<int:index>')
# def delete_rate(index):
#     if 0 <= index < len(c_r.values):
#         del c_r.values[index]
#         c_r_controller.create()  # Обновляем базу данных
#     return redirect(url_for('index'))
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from main import CurrencyRates
from model import CurrencyRatesCRUD

app = Flask(__name__)
app.secret_key = 'realeyesrealisereallies'

# Инициализируем объекты
currency_rates = CurrencyRates()
db_controller = CurrencyRatesCRUD(currency_rates)

# Сначала создаем таблицу в базе данных
db_controller.create()

@app.route('/')
def index():
    try:
        # Загружаем актуальные курсы валют
        currency_rates._fetch_rates()

        # Преобразовываем данные для передачи в шаблон
        rates_data = [(code, currency_rates.last_update.strftime('%d-%m-%Y %H:%M'), value)
                      for code, value in currency_rates.rates.items()]

        # Возвращаем шаблон с данными
        return render_template('index.html', rates=rates_data, last_update=currency_rates.last_update)

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/update', methods=['GET', 'POST'])
def update_currencies():
    if request.method == 'POST':
        try:
            new_codes = request.form.get('currencies', '').upper().replace(' ', '').split(',')
            new_codes = [code.strip() for code in new_codes if code.strip()]

            # Проверяем, что введены корректные коды
            test_response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
            if test_response.status_code == 200:
                available_codes = test_response.json()['Valute'].keys()
                invalid_codes = [code for code in new_codes if code not in available_codes]

                if invalid_codes:
                    flash(f'Неверные коды валют: {", ".join(invalid_codes)}', 'error')
                else:
                    # Обновляем список валют и сразу получаем новые курсы
                    currency_rates.char_codes = new_codes
                    currency_rates._fetch_rates()
                    db_controller.create()
                    flash('Список валют успешно обновлён!', 'success')
            else:
                flash('Не удалось проверить коды валют', 'error')

            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')
            return redirect(url_for('index'))

    # GET-запрос: показываем текущий список валют
    current_currencies = ','.join(currency_rates.char_codes)
    return render_template('update.html', current_currencies=current_currencies)

@app.route('/refresh')
def refresh_rates():
    try:
        # Обновляем курсы валют
        if currency_rates._fetch_rates():
            flash('Курсы валют успешно обновлены!', 'success')
        else:
            flash('Не удалось обновить курсы валют.', 'error')
    except Exception as e:
        flash(f'Ошибка при обновлении: {str(e)}', 'error')

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)