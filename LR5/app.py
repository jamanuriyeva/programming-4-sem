import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from main import CurrencyRates
from model import CurrencyRatesCRUD

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Инициализация
currency_rates = CurrencyRates()
db_controller = CurrencyRatesCRUD(currency_rates)

@app.route('/')
def index():
    try:
        currency_rates._fetch_rates()
        db_controller.create()
        rates_data = db_controller.read()
        return render_template('index.html',
                           rates=rates_data,
                           last_update=currency_rates.last_update)
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