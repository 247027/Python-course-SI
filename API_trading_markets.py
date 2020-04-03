import requests
import json

URL_BIFINEX_ORDERBOOK = "https://api.bitfinex.com/v1/book/btcusd"
URL_BIBAY_ORDERBOOK = "https://bitbay.net/API/Public/BTCUSD/orderbook.json"
URL_BITABY_TICKER = "https://bitbay.net/API/Public/BTCUSD/ticker.json"
URL_BITFINEX_TICKER = "https://api.bitfinex.com/v1/pubticker/btcusd"

def sort(data):
    bigger = []
    equal = []
    smaller = []

    if len(data) > 1:
        choice = data[0]

        for element in data:
            if element < choice:
                smaller.append(element)
            elif element == choice:
                equal.append(element)
            elif element > choice:
                bigger.append(element)

        return sort(smaller) + equal + sort(bigger)
    else:

        return data

def bitbay_offers_show(URL):
    response = requests.get(URL)
    data_offers = response.json()
    print('FIRST TEN BUY AND SELL OFFERS FORM BITBAY', '\n')
    print('BUY OFFERS', '\n')
    for i in range(10):
        print(data_offers['bids'][i])

    print('\n', 'SELL OFFERS', '\n')
    for i in range(10):
        print(data_offers['asks'][i])
    print('\n')
    return

def compare_best_prices(URL_BIFINEX_ORDERBOOK, URL_BIBAY_ORDERBOOK):
    bitbay_response = requests.get(URL_BIBAY_ORDERBOOK)
    bitfinex_response = requests.get(URL_BIFINEX_ORDERBOOK)

    data_offers1 = bitbay_response.json()
    data_offers2 = bitfinex_response.json()

    bitbay_bids = []
    bitbay_asks = []
    bitforex_bids = []
    bitforex_asks = []

    for i in range(len(data_offers2['bids'])):
        x = data_offers2['bids'][i]
        bitforex_bids.append([float(x['price'])])

    bitforex_bids_sorted = sort(bitforex_bids)

    for i in range(len(data_offers2['asks'])):
        x = data_offers2['asks'][i]
        bitforex_asks.append([float(x['price'])])

    bitforex_asks_sorted = sort(bitforex_asks)

    for i in range(len(data_offers1['bids'])):
        bitbay_bids.append(data_offers1['bids'][i])

    bitbay_bids_sorted = sort(bitbay_bids)

    for i in range(len(data_offers1['asks'])):
        bitbay_asks.append(data_offers1['asks'][i])

    bitbay_asks_sorted = sort(bitbay_asks)

    if bitbay_asks_sorted[-1] > bitforex_asks_sorted[-1]:
        print("The best  price to buy was on bifinex", bitforex_asks_sorted[-1])
    elif bitbay_asks_sorted[-1] < bitforex_asks_sorted[-1]:
        print("The best  price tu buy was on bitbay", bitbay_asks_sorted[-1])
    elif bitbay_asks_sorted[-1] == bitforex_asks_sorted[-1]:
        print('The best price to buy was the same on both markets')
    if bitbay_bids_sorted[0] > bitforex_bids_sorted[0]:
        print("The best price to sell was on bifinex", bitbay_bids_sorted[0])
    elif bitbay_bids_sorted[0] < bitforex_bids_sorted[0]:
        print("The best price to sell was on bitbay", bitforex_bids_sorted[0])
    elif bitbay_bids_sorted[0] == bitforex_bids_sorted[0]:
        print('The best price to sell was the same on both markets', bitbay_bids_sorted[0])

    return


def compare_avarage(URL_BITABY_TICKER, URL_BITFINEX_TICKER):
    bitbay_response = requests.get(URL_BITABY_TICKER)
    bitfinex_response = requests.get(URL_BITFINEX_TICKER)
    bitbay_ticker = bitbay_response.json()
    bitfinex_ticker = bitfinex_response.json()

    if bitbay_ticker['bid'] > float(bitfinex_ticker['bid']):
        print('Better avarage selling price was on Bitbay market -', bitbay_ticker['bid'])

    elif bitbay_ticker['bid'] < float(bitfinex_ticker['bid']):
        print('Better avarage selling price was on Bitbay market -', float(bitfinex_ticker['bid']))

    elif bitbay_ticker['bid'] == float(bitfinex_ticker['bid']):
        print('On both markets same avarage prices' - bitbay_ticker['bid'])

    if bitbay_ticker['ask'] > float(bitfinex_ticker['ask']):
        print('Better avarage buying price  was on Bitbay market -', float(bitfinex_ticker['ask']))

    elif bitbay_ticker['ask'] < float(bitfinex_ticker['ask']):
        print('Better avarage buying price  was on Bitbay market -', bitbay_ticker['ask'])

    elif bitbay_ticker['ask'] == float(bitfinex_ticker['ask']):
        print('On both markets same avarage prices' - bitbay_ticker['ask'])

    return

def marekt_information():
    bitbay_offers_show(URL_BIBAY_ORDERBOOK)
    compare_avarage(URL_BITABY_TICKER, URL_BITFINEX_TICKER)
    compare_best_prices(URL_BIFINEX_ORDERBOOK, URL_BIBAY_ORDERBOOK)

    return
marekt_information()