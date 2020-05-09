import sqlite3
import os


def Create_data_base():
    connection = sqlite3.connect('wallet.db')
    cursor = connection.cursor()

    cursor.execute(""" CREATE TABLE wallet(
                        currency_name text,
                        currency_amount real)""")

    currencies = ['btc', 'eur', 'xrp', 'ltc', 'eth', 'bch']
    for i in range(len(currencies)):
        cursor.execute("INSERT INTO wallet VALUES('{}',0)".format(currencies[i]))

    connection.commit()
    connection.close()
    return (print("DATA BASE CREATED"))


def Show_data_base():
    connection = sqlite3.connect('wallet.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM wallet")
    x = cursor.fetchall()
    connection.commit()
    connection.close()
    return (x)


def Show_element(currency_n):
    connection = sqlite3.connect('wallet.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM wallet WHERE currency_name = '{}'".format(currency_n))
    x = cursor.fetchall()
    connection.commit()
    connection.close()
    return (x)


def Update_available_currencies():
    connection = sqlite3.connect('wallet.db')
    cursor = connection.cursor()
    cursor.execute(""" SELECT currency_name 
                        FROM wallet """)
    x = cursor.fetchall()
    connection.commit()
    connection.close()
    return (x)


def Amount_upadate_add(currency_n, currency_a):
    connection = sqlite3.connect('wallet.db')
    cursor = connection.cursor()
    cursor.execute("""UPDATE wallet  
                    SET currency_amount = currency_amount + {} 
                    WHERE currency_name = '{}' """.format(currency_a, currency_n))
    cursor.execute("SELECT * FROM wallet WHERE currency_name ='{}'".format(currency_n))
    x = cursor.fetchall()
    connection.commit()
    connection.close()
    return (x)


def Amount_update_rm(currency_n, currency_a):
    connection = sqlite3.connect('wallet.db')
    cursor = connection.cursor()
    cursor.execute("""UPDATE wallet  
                    SET currency_amount = currency_amount - {} 
                    WHERE currency_name = '{}' AND currency_amount >= {}""".format(currency_a, currency_n, currency_a))
    cursor.execute("SELECT * FROM wallet WHERE currency_name = '{}' ".format(currency_n))
    x = cursor.fetchall()
    connection.commit()
    connection.close()
    return (x)


def Delete_one(currency_n):
    connection = sqlite3.connect('wallet.db')
    cursor = connection.cursor()
    cursor.execute("""UPDATE wallet  
                    SET currency_amount = 0 
                    WHERE currency_name = '{}' """.format(currency_n))
    cursor.execute("SELECT * FROM wallet WHERE currency_name ='{}'  ".format(currency_n))
    x = cursor.fetchall()
    connection.commit()
    connection.close()
    return (x)


def Delete_all():
    connection = sqlite3.connect('wallet.db')
    cursor = connection.cursor()
    cursor.execute("""UPDATE wallet  
                    SET currency_amount = 0 """)
    cursor.execute("SELECT * FROM wallet ")
    x = cursor.fetchall()
    connection.commit()
    connection.close()
    return (x)

def Show_owned_currencies():
    connection = sqlite3.connect('wallet.db')
    cursor = connection.cursor()
    cursor.execute(""" SELECT *
                        FROM wallet 
                        WHERE currency_amount != 0""")
    x = cursor.fetchall()
    connection.commit()
    connection.close()
    return (x)
