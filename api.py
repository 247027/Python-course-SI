import requests
import json
from database import *


def Get_api(entry):
    URL = 'https://www.bitstamp.net/api/v2/transactions/'
    x = str(entry)
    currency_pairs = ['btcusd', 'btceur', 'eurusd', 'xrpusd', 'xrpeur', 'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc',
                      'ethusd', 'etheur', 'ethbtc', 'bchusd', 'bcheur', 'bchbtc']
    for i in range(len(currency_pairs)):
        if x == currency_pairs[i]:
            URL = URL + entry + '/'
    query = {'time': 'day'}
    response = requests.get(URL,params=query)
    data_offers = response.json()
    return (data_offers)


def Get_profit(entry):
    x = Show_owned_currencies()
    amount = 0
    for i in range(len(x)):
        if str(entry)[:3] == x[i][0] or str(entry)[:4] == x[i][0]:
            amount = float(x[i][1])
            break

    transactions = Get_api(entry)
    if len(transactions) > 0:
        transactions = sorted(transactions, key=lambda i: i['date'])
        profit = float(transactions[0]['price']) / float(transactions[-1]['price']) * 100 - 100
        money_profit = float(transactions[0]['price']) * amount - float(transactions[-1]['price']) * amount
        money_profit = round(money_profit, 3)
        profit = round(profit, 2)
        profits = [profit, money_profit, amount]
    else:
        profit = "Uncountable - there was not any transactions "
        money_profit = "Uncountable - there was not any transactions "
        profits = [profit, money_profit, amount]
    return (profits)


def Get_all_profit(market_name):
    x = Show_owned_currencies()
    whole_profit = []
    currencies_amount = []
    money_profit = []
    for i in range(len(x)):
        if str(market_name) == x[i][0]:
            c_money_profit = 0
            money_profit.append(c_money_profit)
            whole_profit.append({'currency name': str(x[i][0]), 'percentage change': 0})
            pass
        else:
            currencies_amount.append(x[i][1])
            entry = x[i][0] + str(market_name)
            transactions = Get_api(entry)
            if len(transactions) > 0:
                transactions = sorted(transactions, key=lambda i: i['date'])
                profit = float(transactions[0]['price']) / float(transactions[-1]['price']) * 100 - 100
                whole_profit.append({'currency name': str(x[i][0]), 'percentage change': round(profit, 2)})

                c_money_profit = float(transactions[0]['price']) * float(x[i][1]) - float(
                    transactions[-1]['price']) * float(x[i][1])
                money_profit.append(c_money_profit)

            else:
                profit = 0
                whole_profit.append({'currency name': str(x[i][0]), 'percentage change': 0})

    percentage_whole_profit = 0
    currencies_amount = sum(currencies_amount)
    for i in range(len(x)):
        weight = x[i][1] / currencies_amount
        percentage_whole_profit += whole_profit[i]['percentage change'] * weight

    money_profit = sum(money_profit)

    output = [whole_profit, round(percentage_whole_profit, 2), round(money_profit, 3)]
    return (output)
