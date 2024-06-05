import json
import sys
import requests
import supported_currencies
import datetime

def fetch_data(*, update=False, json_cache, url):
    if update:
        json_data = None
    else:
        try:
            with open(json_cache, 'r') as file:
                json_data = json.load(file)
                print('Fetched data from local cache')
        except(FileNotFoundError, json_data.JSONDecodeError) as e:
            print(f'No local cache found - {e}')
            json_data = None

    if not json_data:
        print('Fetching new json data.. (Creating local cache)')
        json_data = requests.get(url).json()
        with open(json_cache, 'w') as file:
            json.dump(json_data, file)

    return json_data
def calculate_currency(input_amount, ex_rate):
    converted_amount = input_amount * ex_rate
    return converted_amount

def get_api_key():
    with open("config.json", "r") as jsonfile:
        api_key = json.load(jsonfile)['api_key']

        return api_key

def find_exchange_rate(date, base_curr, target_curr):
    # TODO: check if data is cached in conversions.py
    # json_cache = 'conversions.json'
    # data: dict = fetch_data(update=False, json_cache=json_cache, url=url)
    # print('Data:', data)

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
    #TODO: check if 'END' is case-insensitive
    if input_word == 'end':
        sys.exit()
    return True


def request_data_for_conversion():
    date = None
    while date is None:
        #TODO: check if it is correct to add the labels (maybe del)
        #TODO: add validator - date before today
        #TODO: ensure correct type of data used
        date = input('python3 CurrencyConversion.py ')
        check_if_command_is_end(date)
        try:
            datetime.date.fromisoformat(date)
        except:
            date = None
            print('Please enter a valid data format: YYYY-MM-DD')

    amount = None
    while amount is None:
        amount = float(input('//Amount\n'))
        check_if_command_is_end(amount)
        print(len(str(amount).rsplit('.')[-1]))
        if len(str(amount).rsplit('.')[-1]) > 2:
            print('Please enter a valid amount')
            amount = None
    base_curr = None
    while base_curr is None:
        base_curr = str(input('//Base currency\n'))
        check_if_command_is_end(base_curr)
        if base_curr.upper() not in supported_currencies.supported_curr.keys():
            print('Please enter a valid currency code')
            base_curr = None
    target_curr = None
    while target_curr is None:
        target_curr = str(input('//Target currency\n'))
        check_if_command_is_end(target_curr)
        if target_curr.upper() not in supported_currencies.supported_curr.keys():
            print('Please enter a valid currency code')
            target_curr = None
    return date, amount, base_curr, target_curr


def save_to_conversions(date, amount, base_curr, target_curr, converted_amount):
    #TODO: save to conversions.json
    '''
    with open(r'conversions.json', 'a') as f:
        # The previous line will create the json file if doesn't exist
        Thing = {}
        Thing['stuff'] = []
        Thing['stuff'].append({
            "date": date,
            "amount": amount,
            "base_currency": base_curr,
            "target_currency": target_curr,
            "converted_amount": converted_amount
        })
        json.dump(Thing, f)
        '''
    '''
    conversions = {
        "date": date,
        "amount": amount,
        "base_currency": base_curr,
        "target_currency": target_curr,
        "converted_amount": converted_amount
    }
    # #TODO: dict to json

    with open("conversions.json", "a") as outfile:
        json.dump(conversions, outfile)
    '''
    '''
    Below not working:
    conversions = {
        "date": date,
        "amount": amount,
        "base_currency": base_curr,
        "target_currency": target_curr,
        "converted_amount": converted_amount
    }
    with open('conversions.json', 'r') as file:
        # read JSON data
        data = json.load(file)

        # add field
        data["demo"]["f'{datetime.datetime.now}'"] = conversions
'''



if __name__ == '__main__':
    date, amount, base_curr, target_curr = request_data_for_conversion()
    exchange_rate = find_exchange_rate(date, base_curr, target_curr)
    converted_amount = calculate_currency(amount, exchange_rate)
    save_to_conversions(date=date, amount=f'{amount:.2f}', base_curr=base_curr.upper(), target_curr=target_curr.upper(), converted_amount=f'{converted_amount:.2f}')
    print(f'{amount:.2f} {base_curr.upper()} is {converted_amount:.2f} {target_curr.upper()}')

    date, amount, base_curr, target_curr = request_data_for_conversion()
