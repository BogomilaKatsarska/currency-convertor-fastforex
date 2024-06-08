import json
import os
import sys
import requests
import supported_currencies
import datetime
from datetime import datetime, timedelta

DAYS_DATA_AVAILABLE_FROM = 14

def calculate_currency(input_amount, ex_rate):
    converted_amount = float(input_amount) * ex_rate
    return converted_amount

def get_api_key():
    with open("config.json", "r") as jsonfile:
        api_key = json.load(jsonfile)['api_key']

        return api_key

def find_exchange_rate(date, base_curr, target_curr):
    date = date
    base_curr = base_curr
    target_curr = target_curr
    api_key = get_api_key()
    url = f"https://api.fastforex.io/historical?date={date}&from={base_curr}&to={target_curr}&api_key={api_key}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    exchange_rate = response.json()['results'][f'{target_curr.upper()}']
    return exchange_rate

def check_if_command_is_end(input_word):
    if input_word == 'END':
        sys.exit()
    return True


def request_data_for_conversion():
    date = None
    while date is None:
        date = input('python3 CurrencyConversion.py ')
        check_if_command_is_end(date)
        #TODO: chech if correct format
        # date_str = str(date)
        # if datetime.strptime(date_str, '%Y-%m-%d'):
        #     continue
        # else:
        #     date = None
        #     print("date format alalaba")
        date_string = str(date)
        input_datetime_format = datetime.strftime(datetime.strptime(date_string, '%Y-%m-%d'), '%Y-%m-%d')
        date_today = datetime.date(datetime.today())
        if str(date_today) <= input_datetime_format:
            date = None
            print('Please enter date before today')
        elif input_datetime_format < str(datetime.date(datetime.today() - timedelta(days=DAYS_DATA_AVAILABLE_FROM))):
            date = None
            print(f'Historical data limited to {DAYS_DATA_AVAILABLE_FROM} days during trial')
        else:
            continue

    amount = None
    while amount is None:
        amount = (input())
        # if type(amount) not in (int, float):
        #     print('Amount should be a value')
        #     amount = None
        # if not type(amount) == int or type(amount) == float:
        #     print('Amount should be a value')
        #     amount = None
        check_if_command_is_end(amount)
        if len(str(amount).rsplit('.')[-1]) > 2:
            print('Please enter a valid amount')
            amount = None
    base_curr = None
    while base_curr is None:
        base_curr = str(input())
        check_if_command_is_end(base_curr)
        if base_curr.upper() not in supported_currencies.supported_curr.keys():
            print('Please enter a valid currency code')
            base_curr = None
    target_curr = None
    while target_curr is None:
        target_curr = str(input())
        check_if_command_is_end(target_curr)
        if target_curr.upper() not in supported_currencies.supported_curr.keys():
            print('Please enter a valid currency code')
            target_curr = None
    return date, amount, base_curr, target_curr


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


# if __name__ == '__main__':
#     date, amount, base_curr, target_curr = request_data_for_conversion()
#     curr = {
#     "date": date,
#     "amount": f'{float(amount):.2f}',
#     "base_currency": base_curr.upper(),
#     "target_currency": target_curr.upper(),
#     }
#     with (open('conversions.json') as feedsjson):
#         feeds = json.load(feedsjson)
#         for item in feeds:
#             if item['date'] == curr['date'] and item['amount'] == curr['amount'] and item['base_currency'] == curr['base_currency'] and item['target_currency'] == curr['target_currency']:
#                 print(item['converted_amount'])
#                 print(f"{float(amount):.2f} {base_curr.upper()} is {item['converted_amount']} {target_curr.upper()}")
#                 #TODO: restart program
#
#                 date, amount, base_curr, target_curr = request_data_for_conversion()
#
#         exchange_rate = find_exchange_rate(date, base_curr, target_curr)
#         converted_amount = calculate_currency(amount, exchange_rate)
#         save_to_conversions(date=date, amount=f'{float(amount):.2f}', base_curr=base_curr.upper(), target_curr=target_curr.upper(), converted_amount=f'{converted_amount:.2f}')
#         print(f'{float(amount):.2f} {base_curr.upper()} is {float(converted_amount):.2f} {target_curr.upper()}')
#
#         date, amount, base_curr, target_curr = request_data_for_conversion()
def main():
    date, amount, base_curr, target_curr = request_data_for_conversion()
    curr = {
        "date": date,
        "amount": f'{float(amount):.2f}',
        "base_currency": base_curr.upper(),
        "target_currency": target_curr.upper(),
    }
    with (open('conversions.json') as feedsjson):
        feeds = json.load(feedsjson)
        for item in feeds:
            if item['date'] == curr['date'] and item['amount'] == curr['amount'] and item['base_currency'] == curr[
                'base_currency'] and item['target_currency'] == curr['target_currency']:
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
