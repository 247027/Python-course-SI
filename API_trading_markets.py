import requests
import json

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