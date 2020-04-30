import requests
import json

def show(URL):
    response = requests.get(URL)
    data_offers=response.json()
    return(print(data_offers))

def sort(data):
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i][0] < data[j][0]:
                temp = data[i]
                data[i] = data[j]
                data[j]= temp
def revsort(data):
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i][0] > data[j][0]:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp

def buy_sell():
    while True:
        URL_BIFINEX_ORDERBOOK = 'https://api.bitfinex.com/v1/book/btcusd'
        URL_BITBAY_ORDERBOOK = 'https://bitbay.net/API/Public/BTCUSD/orderbook.json'
        URL_BITTREX_ORDERBOOK = 'https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both'
        URL_BITSTAMP_ORDERBOOK = 'https://www.bitstamp.net/api/order_book/'

        response = requests.get(URL_BITBAY_ORDERBOOK)
        bitbay_offers=response.json()

        response1 = requests.get(URL_BIFINEX_ORDERBOOK)
        bitfinex_offer = response1.json()
        bitfinex_offers = {'bids':[],'asks':[]}

        response2 = requests.get(URL_BITTREX_ORDERBOOK)
        bittrex_offer = response2.json()
        bittrex_offers = {'bids':[], 'asks':[]}

        response3 = requests.get(URL_BITSTAMP_ORDERBOOK)
        bitstamp_offers = {'bids': response3.json()['bids'], 'asks': response3.json()['asks']}

        for i in range(len(bitstamp_offers['bids'])):
            bitstamp_offers['bids'][i][0] = float(bitstamp_offers['bids'][i][0])
            bitstamp_offers['bids'][i][1] = float(bitstamp_offers['bids'][i][1])
        for i in range(len(bitstamp_offers['asks'])):
            bitstamp_offers['asks'][i][0] = float(bitstamp_offers['asks'][i][0])
            bitstamp_offers['asks'][i][1] = float(bitstamp_offers['asks'][i][1])

        for i in range(len(bittrex_offer['result']['sell'])):
            pair = []
            pair.append(float(bittrex_offer['result']['sell'][i]['Rate']))
            pair.append((float(bittrex_offer['result']['sell'][i]['Quantity'])))
            bittrex_offers['asks'].append(pair)

        for i in range(len(bittrex_offer['result']['buy'])):
            pair = []
            pair.append(float(bittrex_offer['result']['buy'][i]['Rate']))
            pair.append((float(bittrex_offer['result']['buy'][i]['Quantity'])))
            bittrex_offers['bids'].append(pair)

        for i in range(len(bitfinex_offer['bids'])):
            pair = []
            pair.append(float(bitfinex_offer['bids'][i]['price']))
            pair.append((float(bitfinex_offer['bids'][i]['amount'])))
            bitfinex_offers['bids'].append(pair)
        for i in range(len(bitfinex_offer['asks'])):
            pair = []
            pair.append(float(bitfinex_offer['asks'][i]['price']))
            pair.append((float(bitfinex_offer['asks'][i]['amount'])))
            bitfinex_offers['asks'].append(pair)

        markets = [bitbay_offers,bitfinex_offers,bittrex_offers,bitstamp_offers]
        market_names = ['Bitbay','Bitfinex','Bittrex','Bitstamp']
        market_provisions = [1.0042, 1.002, 1.001, 1.0011]
        offers={'BUY':[],'SELL': []}
        budget={'Bitbay': 10000, 'Bitfinex': 10000, 'Bittrex':10000, 'Bitstamp': 10000}

        for i in range(len(markets)):
            for j in range(len(markets)):
                for k in range(len(markets[i]['asks'])):
                    for l in range(len(markets[j]['bids'])):

                        if i != j and  markets[i]['asks'][k][0]<markets[j]['bids'][l][0]:
                            offers['BUY'].append([markets[i]['asks'][k][0], markets[i]['asks'][k][1], market_names[i], market_provisions[i]])
                            offers['SELL'].append([markets[j]['bids'][l][0], markets[j]['bids'][l][1], market_names[j], market_provisions[j]])


        revsort(offers['SELL'])
        sort(offers['BUY'])
        print(offers['BUY'])
        print(offers['SELL'])


        if len(offers['SELL']) == 0:
            print('NO OFFERS')

        elif len(offers['SELL']) > 1:
            i = 0
            while len(offers['SELL']) - 1 >= i + 1:
                if offers['SELL'][i] == offers['SELL'][i + 1]:
                    offers['SELL'].pop(i + 1)
                else:
                    i += 1
            j=0
            while len(offers['BUY']) - 1 >= j + 1:
                    if offers['BUY'][j] == offers['BUY'][j + 1]:
                        offers['BUY'].pop(j + 1)
                    else:
                        j += 1

        earnings=[]
        if (int(len(offers['SELL'])) > 0) and (int(len(offers['BUY'])) > 0):

            i = 0
            while (int(len(offers['SELL'])) > 0) and (int(len(offers['BUY'])) > 0):



                if offers['SELL'][i][1] == offers['BUY'][i][1]:
                    if offers['SELL'][i][0] > offers['BUY'][i][0]:
                        profit = offers['SELL'][i][0] * offers['SELL'][i][1]  - offers['BUY'][i][0] * offers['BUY'][i][1] * offers['BUY'][i][3]
                        if profit > 0:
                            if budget[offers['BUY'][i][2]] > offers['BUY'][i][0] * offers['BUY'][i][1] * offers['BUY'][i][3]:
                                budget[offers['SELL'][i][2]] = budget[offers['SELL'][i][2]] + profit
                                earnings.append(profit)
                                print('BUY AT THE RATE', offers['BUY'][i][0], 'on', offers['BUY'][i][2],
                                      'SELL AT THE RATE ', offers['SELL'][i][0],'on', offers['SELL'][i][2],
                                      'amount', offers['SELL'][i][1], 'EARNED', round(profit, 3),'[USD]')
                                offers['BUY'].pop(i)
                                offers['SELL'].pop(i)
                            else:
                                profit = budget[offers['BUY'][i][2]] / offers['BUY'][i][0] / offers['BUY'][i][3] * offers['SELL'][i][0] - budget[offers['BUY'][i][2]]
                                if profit > 0:
                                    budget[offers['SELL'][i][2]] = budget[offers['SELL'][i][2]] + profit
                                    earnings.append(profit)
                                    print('BUY AT THE RATE', offers['BUY'][i][0], 'on', offers['BUY'][i][2],
                                          'SELL AT THE RATE ', offers['SELL'][i][0], 'on', offers['SELL'][i][2],
                                          'amount',budget[offers['BUY'][i][2]] / offers['BUY'][i][0] / offers['BUY'][i][3],
                                          'EARNED', round(profit, 3), '[USD]')
                                    offers['BUY'].pop(i)
                                    offers['SELL'].pop(i)
                                else:
                                    offers['BUY'].pop(i)

                        else:
                            offers['BUY'].pop(i)

                    else:
                        break

                elif offers['SELL'][i][1] > offers['BUY'][i][1]:
                    if offers['SELL'][i][0] > offers['BUY'][i][0]:
                        profit = offers['SELL'][i][0]*offers['BUY'][i][1] - offers['BUY'][i][0] * offers['BUY'][i][1] * offers['BUY'][i][3]
                        if profit > 0:
                            if budget[offers['BUY'][i][2]] > offers['BUY'][i][0] * offers['BUY'][i][1] * offers['BUY'][i][3]:
                                budget[offers['SELL'][i][2]] = budget[offers['SELL'][i][2]] + profit
                                earnings.append(profit)
                                print('BUY AT THE RATE', offers['BUY'][i][0], 'on', offers['BUY'][i][2],
                                      'SELL AT THE RATE', offers['SELL'][i][0],'on', offers['SELL'][i][2],
                                      'amount', offers['BUY'][i][1],
                                      'EARNED', round(profit, 3),'[USD]')
                                offers['SELL'][i][1] = offers['SELL'][i][1] - offers['BUY'][i][1]
                                offers['BUY'].pop(i)
                            else:
                                profit = budget[offers['BUY'][i][2]] / offers['BUY'][i][0] / offers['BUY'][i][3] * offers['SELL'][i][0] - budget[offers['BUY'][i][2]]
                                if profit > 0:
                                    budget[offers['SELL'][i][2]] = budget[offers['SELL'][i][2]] + profit
                                    earnings.append(profit)
                                    print('BUY AT THE RATE', offers['BUY'][i][0], 'on', offers['BUY'][i][2],
                                          'SELL AT THE RATE', offers['SELL'][i][0], 'on', offers['SELL'][i][2],
                                          'amount', (budget[offers['BUY'][i][2]] / offers['BUY'][i][0] / offers['BUY'][i][3]),
                                          'EARNED', round(profit, 3), '[USD]')
                                    offers['BUY'].pop(i)
                                else:
                                    offers['BUY'].pop(i)

                        else:
                            offers['BUY'].pop(i)
                    else:
                        break

                elif offers['SELL'][i][1] < offers['BUY'][i][1]:
                    if offers['SELL'][i][0] > offers['BUY'][i][0]:

                        profit = offers['SELL'][i][0] * offers['SELL'][i][1]  - offers['BUY'][i][0] * offers['SELL'][i][1] * offers['BUY'][i][3]
                        if profit > 0:
                            if budget[offers['BUY'][i][2]] > offers['BUY'][i][0] * offers['BUY'][i][1] * offers['BUY'][i][3]:
                                budget[offers['SELL'][i][2]] = budget[offers['SELL'][i][2]] + profit
                                earnings.append(profit)
                                print('BUY AT THE RATE', offers['BUY'][i][0],  'on', offers['BUY'][i][2],
                                      'SELL AT THE RATE', offers['SELL'][i][0], 'on', offers['SELL'][i][2],
                                      'amount', offers['SELL'][i][1],
                                      'EARNED', round(profit,3) ,'[USD]')
                                offers['BUY'][i][1] = offers['BUY'][i][1] - offers['SELL'][i][1]
                                offers['SELL'].pop(i)
                            else:
                                profit = budget[offers['BUY'][i][2]] / offers['BUY'][i][0] / offers['BUY'][i][3] * offers['SELL'][i][0] - budget[offers['BUY'][i][2]]
                                if profit > 0:
                                    print('BUY AT THE RATE', offers['BUY'][i][0], 'on', offers['BUY'][i][2],
                                          'SELL  AT THE RATAE', offers['SELL'][i][0], 'on', offers['SELL'][i][2],
                                          'amount', (budget[offers['BUY'][i][2]] / offers['BUY'][i][0]  / offers['BUY'][i][3]),
                                          'EARNED', round(profit, 3), '[USD]')
                                    budget[offers['SELL'][i][2]] = budget[offers['SELL'][i][2]] + profit
                                    earnings.append(profit)
                                    offers['SELL'].pop(i)
                                else:
                                    offers['BUY'].pop(i)
                        else:
                            offers['BUY'].pop(i)
                    else:
                        break
            profit = round(sum(earnings), 3)
            print('EARNED', profit, 'USD', )

            print('Bitbay budget:', round(budget['Bitbay'],3),'\n',
                  'Bifinex budget:', round(budget['Bitfinex'],3),'\n',
                  'Bittrex budget:', round(budget['Bittrex'],3),'\n',
                  'Bitstamp budget:', round(budget['Bitstamp'],3))
            time.sleep(5)
    return()

buy_sell()
#uwzględniłem tylko prowizję przy zakupie BTC, ponieważ po uwzględnieniu drugiej prowizji  przy sprzedaży nie było żadnych ofert przynoszacych zysk
#prowizja od sprzedaży = (offers['SELL'][i][3]*offers['SELL][i][0]*amount^-offers['SELL'][i][0]*amount^
#amount^- zależne od przypadku




