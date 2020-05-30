import requests
import json
import time
import datetime as dt
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
from math import fabs

currencies = ['BTC', 'ETH', 'BCC']
markets = ['PLN']
start_collecting_data_date = (2019, 5, 15)  # ( int(input('input YEAR')), int(input('input MONTH')), int(input('input DAY')))
finish_collecting_data_date = (2020, 5, 15)  # ( int(input('input YEAR')), int(input('input MONTH')), int(input('input DAY')))4
resolution = 86400
end_of_symulation_date = (2020, 5, 26)
number_of_days = int(abs((dt.date(end_of_symulation_date[0], end_of_symulation_date[1], end_of_symulation_date[2]) - dt.date(finish_collecting_data_date[0], finish_collecting_data_date[1],finish_collecting_data_date[2])).days))
number_of_symulations = 100


def time_converter(date):
    d = dt.datetime(date[0], date[1], date[2])
    unixtime_s = time.mktime(d.timetuple())
    unixtime_ms = unixtime_s * 1000
    return (int(unixtime_ms))


def get_data(from_start_date, finish_date, currency_name, market, resolution):
    url = "https://api.bitbay.net/rest/trading/candle/history/"
    url = url + str(currency_name) + '-' + str(market) + '/' + str(resolution)
    querystring = {"from": str(time_converter(from_start_date)), "to": str(time_converter(finish_date))}
    response = requests.get(url, params=querystring)
    data = response.json()
    return data


def pct_change(data):
    df_pct_change = []
    for i in range(len(data)):
        if i == 0:
            df_pct_change.append(0)
        else:
            df_pct_change.append(data[i] / data[i - 1] - 1)
    return df_pct_change


negative_interwals = [-1, -0.85], [-0.85, -0.5], [-0.5, 0]
positive_interwals = [0, 0.5], [0.5, 1], [1, 1.5], [1.5, 2], [2, 4], [4, 8], [8, 12], [12, 20]
interwals = negative_interwals + positive_interwals


def probability(data, interwals):
    probability = {str(interwals[0]): [], str(interwals[1]): [], str(interwals[2]): [], str(interwals[3]): [],
                   str(interwals[4]): [], str(interwals[5]): [],
                   str(interwals[6]): [], str(interwals[7]): [], str(interwals[8]): [], str(interwals[9]): [],
                   str(interwals[10]): []}

    count_positive = 0
    count_negative = 0
    for i in range(len(data)):
        for j in range(len(interwals)):
            if data[i] >= interwals[j][0] and data[i] < interwals[j][1]:
                probability[str(interwals[j])].append(data[i])
                break
        if data[i] < 0:
            count_negative += 1
        else:
            count_positive += 1

    growth_probability = count_positive / len(data)
    fall_probability = count_negative / len(data)

    for i in range(len(interwals)):
        if interwals[i][0] < 0:
            probability[str(interwals[i])] = round(len(probability[str(interwals[i])]) / count_negative, 3)
        else:
            probability[str(interwals[i])] = round(len(probability[str(interwals[i])]) / count_positive, 2)

    compartments = {str(interwals[0]): [], str(interwals[1]): [], str(interwals[2]): [], str(interwals[3]): [],
                    str(interwals[4]): [], str(interwals[5]): [],
                    str(interwals[6]): [], str(interwals[7]): [], str(interwals[8]): [], str(interwals[9]): [],
                    str(interwals[10]): []}

    for i in range(len(interwals)):
        if i == 0 and interwals[i][0] < 0:
            compartments[str(interwals[i])] = [0, probability[str(interwals[i])]]
        elif interwals[i - 1][0] < 0 and interwals[i][0] >= 0:
            compartments[str(interwals[i])] = [0, probability[str(interwals[i])]]

        else:
            compartments[str(interwals[i])] = [compartments[str(interwals[i - 1])][1],
                                               compartments[str(interwals[i - 1])][1] + probability[str(interwals[i])]]

            if compartments[str(interwals[i])][1] == 1.0 and interwals[i][0] >= 0:
                break

    return compartments, growth_probability, probability


def get_result(compartments):
    result = None
    x = random.uniform(0, 1)
    if x >= 0 and x <= compartments[1]:
        x = random.uniform(0, 1)
        for i in range(len(interwals)):
            if interwals[i][0] < 0:
                pass
            else:
                if compartments[0][str(interwals[i])][1] == 1.0:
                    result = random.uniform(float(interwals[i][0]), float(interwals[i][1]))
                    break
                if x > compartments[0][str(interwals[i])][0] and x <= compartments[0][str(interwals[i])][1]:
                    result = random.uniform(float(interwals[i][0]), float(interwals[i][1]))
                    break

    else:
        x = random.uniform(0, 1)
        for i in range(len(interwals)):
            if interwals[i][0] >= 0:
                break
            if compartments[0][str(interwals[i])][1] == 1.0:
                result = random.uniform(float(interwals[i][0]), float(interwals[i][1]))
                break
            if x > compartments[0][str(interwals[i])][0] and x <= compartments[0][str(interwals[i])][1]:
                result = random.uniform(float(interwals[i][0]), float(interwals[i][1]))
                break

    return result


def symulation(number_of_days, number_of_symulations, data, currency, market):
    pct_change_data = pct_change(data)
    last_value = data[-1]
    compartments = probability(pct_change_data, interwals)
    simulation_df = pd.DataFrame()

    for i in range(number_of_symulations):
        count = 0
        data_series = []
        factor = get_result(compartments)
        value = last_value * (1 + factor)
        data_series.append(value)

        for j in range(number_of_days):
            if count == number_of_days - 1:
                break
            factor = get_result(compartments)
            value = data_series[count] * (1 + factor)
            data_series.append(value)
            count += 1

        simulation_df[i] = data_series
    return simulation_df


def statistic(data):
    mean = np.mean(data)
    median = np.median(data)
    standard_deviation = np.std(data)
    variance = np.var(data)
    stat_data = {'mean': [mean], 'median': [median], 'standard_deviation': [standard_deviation], 'variance': [variance]}
    return stat_data


def main_program(number_of_days, number_of_symulations, currency, market):
    api_data = get_data(start_collecting_data_date, finish_collecting_data_date, currency, market, 86400)
    data = []
    for i in range(len(api_data['items'])):
        data.append(float(api_data['items'][i][1]['v']))

    data_symulation_1 = symulation(number_of_days, 1, data, currency, market)
    data_symulation_2 = symulation(number_of_days, number_of_symulations, data, currency, market)

    data_symulation_2 = data_symulation_2.T
    statistic_data_2 = statistic(data_symulation_2)

    data_1 = []
    data_2 = []

    for i in range(data_symulation_1.shape[0]):
        data_1.append(data_symulation_1[0][i])

    for i in range(len(statistic_data_2['mean'][0])):
        data_2.append(statistic_data_2['mean'][0][i])

    average2 = np.average(data_2)
    return (data_1, data_2, average2)





def charts(number_of_days, number_of_symulations, todays_date, currency, market):
    symulation_data = main_program(number_of_days, number_of_symulations, currency, market)
    api_data = get_data(finish_collecting_data_date, todays_date, currency, market, resolution)
    oryginal_data = []
    for i in range(len(api_data['items'])):
        oryginal_data.append(float(api_data['items'][i][1]['v']))

    data_1 = symulation_data[0]
    data_2 = symulation_data[1]
    for i in range(len(data_1)):
        data_1[i] = round(data_1[i], 2)
        data_2[i] = round(data_2[i], 2)
    average = symulation_data[2]
    x = pd.date_range(start=dt.datetime(finish_collecting_data_date[0], finish_collecting_data_date[1], finish_collecting_data_date[2] + 1),
                      end=dt.datetime(todays_date[0], todays_date[1], todays_date[2]))
    plt.title("Symulation of volume ")  # + str(currency) + '-' + str(market))
    plt.plot(x, data_1, label='single sim')
    plt.plot(x, data_2, label='multiple sim')
    plt.plot(x, oryginal_data, label='oryginal_data')
    plt.axhline(y=average, color='r', linestyle='-', label='avg of multiple sim')
    plt.axhline(y=np.mean(data_1), color='black', linestyle='-', label='avg of single sim')
    plt.xlabel('Days')
    plt.ylabel('Volume')
    plt.legend()
    plt.show()

    length_1 = [[], []]
    length_2 = [[], []]
    pct_change_data_1 = pct_change(data_1)
    pct_change_data_2 = pct_change(data_2)
    pct_change_oryginal_data = pct_change(oryginal_data)

    for i in range(len(oryginal_data)):
        length_1[0].append(fabs(oryginal_data[i] - data_1[i]))
        length_2[0].append(fabs(oryginal_data[i] - data_2[i]))
        length_1[1].append(pct_change_oryginal_data[i] - pct_change_data_1[i])
        length_2[1].append(pct_change_oryginal_data[i] - pct_change_data_2[i])

    print(length_1[0], '\n', '\n', length_2[0], '\n', '\n', length_1[1], '\n', '\n', length_2[1])


charts(number_of_days, number_of_symulations, end_of_symulation_date, currencies[0], markets[0])