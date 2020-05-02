import requests
import datetime
import time

def investment(start_budget):
    while True:
        print(datetime.datetime.now())
        URL_BTC = 'https://www.bitstamp.net/api/v2/transactions/btcusd/'
        URL_ETH = 'https://www.bitstamp.net/api/v2/transactions/ethusd/'
        URL_LTC = 'https://www.bitstamp.net/api/v2/transactions/ltcusd/'
        URL_BCH = 'https://www.bitstamp.net/api/v2/transactions/bchusd/'
        URL_XRP = 'https://www.bitstamp.net/api/v2/transactions/xrpusd/'
        start=start_budget
        transactions_BTC, transacionts_ETH, transacionts_LTC, transactions_BCH, transaciotns_XRP = None, None, None, None, None
        api = [URL_BTC, URL_ETH, URL_LTC, URL_BCH, URL_XRP]
        transactions = [transactions_BTC, transacionts_ETH, transacionts_LTC, transactions_BCH, transaciotns_XRP]
        profit = [{'market': 'BTC', 'profit': 0, 'finish_budget': 0}, {'market': 'ETH', 'profit': 0, 'finish_budget': 0}, {'market': 'LTC', 'profit': 0, 'finish_budget': 0},
                  {'market': 'BCH', 'profit': 0, 'finish_budget': 0}, {'market': 'XRP', 'profit': 0, 'finish_budget': 0}]

        for i in range(len(api)):
            query = {'time': 'day'}
            response = requests.get(api[i], params=query)
            transactions[i] = response.json()

        for i in range(len(transactions)):

            start_budget = start
            finish_budget = 0
            stock = 0
            buy = []
            sell = []

            for j in range(len(transactions[i])):
                if transactions[i][j]['type'] == '0':
                    buy.append({'price': float(transactions[i][j]['price']), 'amount': float(transactions[i][j]['amount'])})
                if transactions[i][j]['type'] == '1':
                    sell.append({'price': float(transactions[i][j]['price']), 'amount': float(transactions[i][j]['amount'])})

            buy = sorted(buy, key = lambda i: i['price'])
            sell = sorted(sell, key = lambda i: i['price'], reverse = True)

            while start_budget != 0:
                a = 0
                buy_power = start_budget / buy[a]['price']

                if buy_power == buy[a]['amount']:
                    stock += buy_power
                    start_budget -= buy_power * buy[a]['price']


                elif buy_power > buy[a]['amount']:
                    stock += buy[a]['amount']
                    start_budget -= buy[a]['price'] * buy[a]['amount']
                    a += 1


                elif buy_power < buy[a]['amount']:
                    stock += buy_power
                    start_budget -= buy[a]['price'] * buy_power

            while stock != 0:
                a = 0
                if stock == sell[a]['amount']:
                    finish_budget += sell[a]['price'] * sell[a]['amount']
                    stock -= sell[a]['amount']


                elif stock > sell[a]['amount']:
                    finish_budget += sell[a]['price'] * sell[a]['amount']
                    stock -= sell[a]['amount']
                    a += 1

                elif stock < sell[a]['amount']:
                    finish_budget += sell[a]['price'] * stock
                    stock = 0

            profit[i]['profit'] = round(finish_budget/start * 100 - 100, 2)
            profit[i]['finish_budget']= round(finish_budget,2)

        profit = sorted(profit, key = lambda i: i['profit'], reverse = True)
        print("start budget", start)
        for i in range(len(profit)):
            if profit[i]['profit'] > 0:
                earned=round(profit[i]['finish_budget'] - start, 2)
                print(profit[i]['market'], '+', profit[i]['profit'], '%','\n',
                      'Budget after investement', profit[i]['finish_budget'], 'earned', earned)
            if profit[i]['profit'] < 0:
                print(profit[i]['market'], '+-', profit[i]['profit'], '%', '\n',
                      'Budget after investement', profit[i]['finish_budget'], 'lost', (earned * -1))
        time.sleep(300)

investment(100000)


