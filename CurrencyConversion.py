import json
import os
import re
import sys
import requests
import supported_currencies
import datetime
from datetime import datetime, timedelta

DAYS_DATA_AVAILABLE_FROM = 14


def get_api_key():
    with open("config.json", "r") as jsonfile:
        api_key = json.load(jsonfile)['api_key']

        return api_key


def calculate_currency(input_amount, ex_rate):
    converted_amount = float(input_amount) * ex_rate

    return converted_amount


def find_exchange_rate(date, base_curr, target_curr):
    url_date = date
    base_currency = base_curr
    target_currency = target_curr
    api_key = get_api_key()
    url = f"https://api.fastforex.io/historical?date={url_date}&from={base_currency}&to={target_currency}&api_key={api_key}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    exchange_rate = response.json()['results'][f'{target_curr.upper()}']

    return exchange_rate


def check_if_command_is_end(input_word):
    if input_word.upper() == 'END':
        sys.exit()
    return True


def request_input_for_date():
    date = None
    while date is None:
        date = input('python3 CurrencyConversion.py ')
        check_if_command_is_end(date)
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        match = re.match(pattern, date)
        if not match:
            print('Date should be in format "YYYY-MM-DD"')
            request_input_for_date()
        date_string = str(date)
        input_datetime_format = datetime.strftime(datetime.strptime(date_string, '%Y-%m-%d'), '%Y-%m-%d')
        date_today = datetime.date(datetime.today())
        if str(date_today) <= input_datetime_format:
            print('Please enter date before today')
            request_input_for_date()
        elif input_datetime_format < str(datetime.date(datetime.today() - timedelta(days=DAYS_DATA_AVAILABLE_FROM))):
            print(f'Historical data limited to {DAYS_DATA_AVAILABLE_FROM} days during trial')
            request_input_for_date()
        else:
            continue

    return date


def request_input_for_amount():
    amount = None
    while amount is None:
        amount = input()
        check_if_command_is_end(amount)
        if amount == '':
            request_input_for_amount()
        if len(str(amount).rsplit('.')[-1]) > 2:
            print('Please enter a valid amount')
            request_input_for_amount()

    return amount


def request_input_for_base_curr():
    base_curr = None
    while base_curr is None:
        base_curr = str(input())
        check_if_command_is_end(base_curr)
        if base_curr.upper() not in supported_currencies.supported_curr.keys():
            print('Please enter a valid currency code')
            request_input_for_base_curr()

    return base_curr


def request_input_for_target_curr():
    target_curr = None
    while target_curr is None:
        target_curr = str(input())
        check_if_command_is_end(target_curr)
        if target_curr.upper() not in supported_currencies.supported_curr.keys():
            print('Please enter a valid currency code')
            request_input_for_target_curr()

    return target_curr


def save_to_conversions(date, amount, base_curr, target_curr, converted_amount):
    entry = {
        "date": date,
        "amount": amount,
        "base_currency": base_curr,
        "target_currency": target_curr,
        "converted_amount": f'{float(converted_amount):.2f}'
    }

    a = []
    if not os.path.isfile('conversions.json'):
        a.append(entry)
        with open('conversions.json', mode='w') as f:
            f.write(json.dumps(a, indent=2))
    else:
        with open('conversions.json') as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(entry)
        with open('conversions.json', mode='w') as f:
            f.write(json.dumps(feeds, indent=2))


def main():
    date = request_input_for_date()
    amount = request_input_for_amount()
    base_curr = request_input_for_base_curr()
    target_curr = request_input_for_target_curr()
    curr = {
        "date": date,
        "amount": float(amount),
        "base_currency": base_curr.upper(),
        "target_currency": target_curr.upper(),
    }
    with (open('conversions.json') as feedsjson):
        feeds = json.load(feedsjson)
        for item in feeds:
            if item['date'] == curr['date'] and \
                    item['amount'] == curr['amount'] and \
                    item['base_currency'] == curr['base_currency'] and \
                    item['target_currency'] == curr['target_currency']:
                print(item['converted_amount'])
                print(f"{float(amount):.2f} {base_curr.upper()} is {item['converted_amount']} {target_curr.upper()}")
                main()

        exchange_rate = find_exchange_rate(date, base_curr, target_curr)
        converted_amount = calculate_currency(amount, exchange_rate)
        save_to_conversions(date=date, amount=f'{float(amount):.2f}', base_curr=base_curr.upper(),
                            target_curr=target_curr.upper(), converted_amount=f'{converted_amount:.2f}')
        print(f'{float(amount):.2f} {base_curr.upper()} is {float(converted_amount):.2f} {target_curr.upper()}')
        main()


if __name__ == '__main__':
    main()
