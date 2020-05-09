import tkinter as tk
from database import *
from api import *
import requests
import json

HEIGHT = 450
WIDTH = 300


def show_profit_pressed():
    root = tk.Tk()
    root['bg'] = '#ffe0b3'
    root.title('Wallet')

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="#ffe0b3")
    canvas.pack()

    label_pair_name = tk.Label(root, text="Enter name of the currency pair to get data. \n Available pairs:",
                               bg="#ffe0b3")
    label_pair_name.place(relx=0.1, rely=0.02, relheight=0.13, relwidth=0.8)

    label_currencies = tk.Label(root, bg="#ffe0b3")
    label_currencies.place(relx=0.1, rely=0.13, relheight=0.11, relwidth=0.8)
    pairs = ['btcusd', 'btceur', 'eurusd', 'xrpusd', 'xrpeur', 'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc', 'ethusd',
             'etheur', 'ethbtc', 'bchusd', 'bcheur', 'bchbtc']
    element = ''
    x = 5
    for i in range(len(pairs)):
        element = element + pairs[i] + ','
        if i == x:
            element = element + '\n'
            x += 6
    label_currencies['text'] = element

    frame_entry_name = tk.Frame(root, bg='#ff9966')
    frame_entry_name.place(relx=0.09, rely=0.265, relheight=0.06, relwidth=0.42)

    entry_pair_name = tk.Entry(root, )
    entry_pair_name.place(relx=0.1, rely=0.27, relheight=0.05, relwidth=0.4)

    frame_return = tk.Frame(root, bg='#ff9966')
    frame_return.place(relx=0.09, rely=0.57, relheight=0.39, relwidth=0.82)

    label_return = tk.Label(root, bg='white', font=('Helvetica', 10), anchor='nw', justify='left', bd=10)
    label_return.place(relx=0.1, rely=0.58, relheight=0.37, relwidth=0.8)

    def get_currency_profit_data_pressed(entry_name):
        entry_name = entry_name.lower()
        x = Get_profit(entry_name)
        element = ''
        if float(x[2]) == 0:
            element += 'YOU DO NOT OWN THIS CURRENCY ' + '\n' 'Price change over 24 H: ' + ' ' + str(x[0]) + '%'
            label_return['text'] = element
        else:
            element += 'Price change over 24 H: ' + ' ' + str(x[0]) + '%' + '\n' + 'Money profit: ' + ' ' + str(x[1])
            label_return['text'] = element

    button = tk.Button(root, text="GET DATA", bg='gray',
                       command=lambda: get_currency_profit_data_pressed(entry_pair_name.get()))
    button.place(relx=0.6, rely=0.27, relheight=0.05, relwidth=0.3)

    label_name_market = tk.Label(root, text="Enter name of the market to get data\n about all owned currencies.",
                                 bg="#ffe0b3")
    label_name_market.place(relx=0.1, rely=0.33, relheight=0.10, relwidth=0.8)

    label_name_market = tk.Label(root, text="Available markets :  usd, eur, btc", bg="#ffe0b3")
    label_name_market.place(relx=0.1, rely=0.43, relheight=0.04, relwidth=0.8)

    frame_entry_market = tk.Frame(root, bg='#ff9966')
    frame_entry_market.place(relx=0.09, rely=0.485, relheight=0.06, relwidth=0.42)

    entry_market_name = tk.Entry(root, )
    entry_market_name.place(relx=0.1, rely=0.49, relheight=0.05, relwidth=0.4)

    def get_market_profit_data_pressed(entry_name):
        if str(entry_name) != 'usd' and str(entry_name) != 'eur':
            label_return['text'] = 'WRONG INPUT GIVEN \n PLEASE CHANGE YOUR INPUT'
        else:
            entry_name = entry_name.lower()
            x = Get_all_profit(entry_name)
            element = ''
            for i in range(len(x[0])):
                element += str(x[0][i]['currency name']) + ' ' + str(x[0][i]['percentage change']) + '%' + '\n'
            element += "Wallet percentage change " + ' ' + str(x[1]) + '%' + ' \n'
            element += 'Total earnings in' + ' ' + entry_name.upper() + ": " + str(x[2])
            label_return['text'] = element

    button = tk.Button(root, text="GET DATA", bg='gray',
                       command=lambda: get_market_profit_data_pressed(entry_market_name.get()))
    button.place(relx=0.6, rely=0.49, relheight=0.05, relwidth=0.3)

    root.mainloop()


def show_resources_pressed():
    root = tk.Tk()
    root['bg'] = '#ffe0b3'
    root.title('Wallet')

    canvas = tk.Canvas(root, height=300, width=WIDTH, bg="#ffe0b3")
    canvas.pack()

    label_name = tk.Label(root, bg="#ffe0b3")
    label_name['text'] = "Enter name of the currency \n or enter 'all' to get all data \n \n Available currencies"
    label_name.place(relx=0.1, rely=0.07, relheight=0.18, relwidth=0.8)

    label_currencies = tk.Label(root, bg="#ffe0b3")
    label_currencies.place(relx=0.1, rely=0.26, relheight=0.05, relwidth=0.8)
    z = Update_available_currencies()
    label_currencies['text'] = z

    frame_entry_name = tk.Frame(root, bg='#ff9966')
    frame_entry_name.place(relx=0.09, rely=0.32, relheight=0.1, relwidth=0.42)

    entry_name = tk.Entry(root, )
    entry_name.place(relx=0.1, rely=0.33, relheight=0.08, relwidth=0.4)

    frame_return = tk.Frame(root, bg='#ff9966')
    frame_return.place(relx=0.09, rely=0.44, relheight=0.5, relwidth=0.82)

    label_return = tk.Label(root, bg='white', font=('Helvetica', 10), anchor='nw', justify='left', bd=10)
    label_return.place(relx=0.1, rely=0.45, relheight=0.48, relwidth=0.8)

    def get_data_pressed(entry_name):
        entry_name = entry_name.lower()
        if entry_name == 'all':
            x = Show_data_base()
            element = ''
            for i in range(len(x)):
                element = element + str(x[i][0]) + ' ' + str(x[i][1]) + '\n'
            label_return['text'] = element
        else:
            x = Show_element(entry_name)
            label_return['text'] = x[0]


    button = tk.Button(root, text="GET DATA", bg='gray', command=lambda: get_data_pressed(entry_name.get()))
    button.place(relx=0.6, rely=0.33, relheight=0.08, relwidth=0.3)

    root.mainloop()


def update_pressed():
    root = tk.Tk()
    root['bg'] = '#ffe0b3'
    root.title('Wallet')

    canvas = tk.Canvas(root, height=250, width=300, bg="#ffe0b3")
    canvas.pack()

    label_currencies = tk.Label(root, text="List of available currencies:", bg="#ffe0b3")
    label_currencies.place(relx=0.1, rely=0.03, relheight=0.10, relwidth=0.8)

    label_list = tk.Label(root, bg="#ffe0b3")
    label_list.place(relx=0.1, rely=0.14, relheight=0.07, relwidth=0.8)
    z = Update_available_currencies()
    label_list['text'] = z

    label_name = tk.Label(root, text="Enter name of \n the resource", bg="#ffe0b3")
    label_name.place(relx=0.1, rely=0.25, relheight=0.1, relwidth=0.3)

    frame_entry_name = tk.Frame(root, bg='#ff9966')
    frame_entry_name.place(relx=0.09, rely=0.38, relheight=0.12, relwidth=0.32)

    entry_name = tk.Entry(root, )
    entry_name.place(relx=0.1, rely=0.39, relheight=0.1, relwidth=0.3)

    label_amount = tk.Label(root, text="Enter amount of \n  resource", bg="#ffe0b3")
    label_amount.place(relx=0.6, rely=0.25, relheight=0.1, relwidth=0.3)

    frame_entry_amount = tk.Frame(root, bg='#ff9966')
    frame_entry_amount.place(relx=0.59, rely=0.38, relheight=0.12, relwidth=0.32)

    entry_amount = tk.Entry(root, )
    entry_amount.place(relx=0.6, rely=0.39, relheight=0.1, relwidth=0.3)

    frame_return = tk.Frame(root, bg='#ff9966')
    frame_return.place(relx=0.09, rely=0.69, relheight=0.22, relwidth=0.82)

    label_return = tk.Label(root, bg='white', font=('Helvetica', 10), anchor='nw', justify='left', bd=10)
    label_return.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.8)

    def add_data_pressed(entry_name, entry_amount):
        entry_name = entry_name.lower()
        x = Amount_upadate_add(entry_name, entry_amount)
        element = 'Amount changed:' + ' ' + str(x[0][0]) + ' ' + str(x[0][1])
        label_return['text'] = element

    button = tk.Button(root, text="ADD DATA", bg='#99e699', command=lambda: add_data_pressed(entry_name.get(), entry_amount.get()))
    button.place(relx=0.2, rely=0.55, relheight=0.1, relwidth=0.3)


    def remove_data_pressed(entry_name, entry_amount):
        entry_name = entry_name.lower()
        x = Amount_update_rm(entry_name, entry_amount)
        element = 'Amount changed:' + ' ' + str(x[0][0]) + ' ' + str(x[0][1])
        label_return['text'] = element

    button = tk.Button(root, text="REMOVE DATA", bg='#ff8080',
                       command=lambda: remove_data_pressed(entry_name.get(), entry_amount.get()))
    button.place(relx=0.5, rely=0.55, relheight=0.1, relwidth=0.3)

    root.mainloop()


def delete_pressed():
    root = tk.Tk()
    root['bg'] = '#ffe0b3'
    root.title('Wallet')

    canvas = tk.Canvas(root, height=250, width=300, bg="#ffe0b3")
    canvas.pack()

    label_name = tk.Label(root, text="Enter name of the currency \n or enter 'all' to delete all data", bg="#ffe0b3")
    label_name.place(relx=0.1, rely=0.07, relheight=0.15, relwidth=0.8)

    frame_entry_name = tk.Frame(root, bg='#ff9966')
    frame_entry_name.place(relx=0.09, rely=0.275, relheight=0.11, relwidth=0.42)

    entry_name = tk.Entry(root, )
    entry_name.place(relx=0.1, rely=0.28, relheight=0.1, relwidth=0.4)

    frame_return = tk.Frame(root, bg='#ff9966')
    frame_return.place(relx=0.09, rely=0.44, relheight=0.47, relwidth=0.82)

    label_return = tk.Label(root, bg='white', font=('Helvetica', 10), anchor='nw', justify='left', bd=2)
    label_return.place(relx=0.1, rely=0.45, relheight=0.45, relwidth=0.8)

    def delete_data_pressed(entry_name):
        entry_name = str(entry_name).lower()
        x = Delete_one(entry_name)
        if str(entry_name) == 'all':
            x = Delete_all()
            element = 'Success delete:' + '\n'
            for i in range(len(x)):
                element = element + str(x[i][0]) + ' ' + str(x[i][1]) + '\n'
            label_return['text'] = element
        else:
            x = Delete_one(entry_name)
            element = 'Success delete:' + ' ' + str(x[0][0]) + ' ' + str(x[0][1])
            label_return['text'] = element

    button = tk.Button(root, text="DELETE DATA", bg='gray', command=lambda: delete_data_pressed(entry_name.get()))
    button.place(relx=0.6, rely=0.28, relheight=0.1, relwidth=0.3)

    root.mainloop()
