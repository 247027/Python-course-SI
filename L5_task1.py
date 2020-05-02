import requests
import json
import datetime
import time

def profits():
    while True:
        print(datetime.datetime.now())

        URL_BTC = 'https://www.bitstamp.net/api/v2/ticker/btcusd/'
        URL_ETH = 'https://www.bitstamp.net/api/v2/ticker/ethusd/'
        URL_LTC = 'https://www.bitstamp.net/api/v2/ticker/ltcusd/'
        URL_BCH = 'https://www.bitstamp.net/api/v2/ticker/bchusd/'
        URL_XRP = 'https://www.bitstamp.net/api/v2/ticker/xrpusd/'

        transactions_BTC, transacionts_ETH, transacionts_LTC, transactions_BCH, transaciotns_XRP = None, None, None, None, None
        api = [URL_BTC, URL_ETH, URL_LTC, URL_BCH, URL_XRP]
        transactions = [transactions_BTC, transacionts_ETH, transacionts_LTC, transactions_BCH, transaciotns_XRP]
        profit = [{'market': 'BTC', 'profit': 0}, {'market': 'ETH', 'profit': 0}, {'market': 'LTC', 'profit': 0},
                  {'market': 'BCH', 'profit': 0}, {'market': 'XRP', 'profit': 0}]

        for i in range(len(api)):
            response = requests.get(api[i])
            transactions[i] = response.json()

        for i in range(len(transactions)):
            profit[i]['profit'] = round(float(transactions[i]['high']) / float(transactions[i]['low']) * 100 - 100, 2)

        profit = sorted(profit, key = lambda i: i['profit'], reverse = True)
        for i in range(len(profit)):
            if profit[i]['profit'] > 0:
                print(profit[i]['market'], '+', profit[i]['profit'], '%')
            if profit[i]['profit'] < 0:
                print(profit[i]['market'], '-', profit[i]['profit'], '%')
        print('\n')
        time.sleep(300)


profits()



