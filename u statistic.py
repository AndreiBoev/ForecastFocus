from functools import reduce
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import datetime
from dateutil import parser as dtparser
import matplotlib.pyplot as plt
import pygetwindow as gw
import pyautogui

load_dotenv()
WEATHER_API_KEY = str(os.getenv('WEATHER_API_KEY'))


def change(date, number):
    date_string = date
    date_obj = dtparser.parse(date_string)
    date_obj += datetime.timedelta(days=number)
    return date_obj.strftime('%Y-%m-%d')


def real_data(lat, lon, start, end):
    url = 'http://api.weatherapi.com/v1//history.json'
    params = {'q': f'{lat},{lon}', 'KEY': WEATHER_API_KEY, 'dt': start, 'end_dt': end, 'wind100kph': 'yes'}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()

            def value(parametr, st, lst):
                sm = 0
                for d in lst[st:st + 6]:
                    sm += d[parametr]
                return round(sm / 6, ndigits=2)

            df2 = pd.DataFrame(columns=['temp', 'wind', 'pressure', 'humidity'])
            for day in data['forecast']['forecastday']:
                n = 0
                for time in ['morning', 'day', 'evening', 'night']:
                    df2.loc[day['date'] + time] = [value('temp_c', n, day['hour']),
                                                   round(value('wind_kph', n, day['hour']) / 3.6, 2),
                                                   value('pressure_in', n, day['hour']) * 25.4,
                                                   value('humidity', n, day['hour'])]
                    n += 6
            return df2
        else:
            print(f"request execution error, error code == {response.status_code}")
        return
    except Exception as e:
        print(f'request execution error: {e}')


def u_statistics(listf, listy):
    e = (sum((y - x) ** 2 for y, x in zip(listy, listf)) / len(listf)) ** 0.5
    f = (reduce(lambda x, y: x + y ** 2, listf) / len(listf)) ** 0.5
    y = (reduce(lambda x, y: x + y ** 2, listy) / len(listy)) ** 0.5

    return e / (y + f)


forecast_df = pd.read_csv("2024-05-22_RedSquar.csv", sep=';')
forecast_df.set_index('time', inplace=True)


# real = real_data('55.75697232932146', '37.614235566135356', change(df.iloc[0].name[0:10:], -1), change(df.iloc[-1].name[0:10:], 1))
# real = real[df.iloc[0].name:df.iloc[-1].name]
# real.to_csv(f'real_data_test.csv', sep=';', index_label="time")
# for column in df.columns:
#    print(column, u_statistics(df[column].tolist(), real[column].tolist()))

def graph(column, forecast_df, real_df):
    y2 = forecast_df[column].tolist()
    y1 = real_df[column].tolist()
    x = list(map(lambda x: x[8::], forecast_df.index.tolist()))
    plt.plot(x, y1, '-', x, y2, '--', marker='o', markersize=7)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # fig = plt.gcf()
    # fig.set_size_inches(18.5, 10.5)
    plt.show()


def report():
    active_window = gw.getActiveWindow()
    left, top, right, bottom = active_window.left, active_window.top, active_window.right, active_window.bottom

    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    screenshotPath = 'report.pdf'
    screenshot.save(screenshotPath)

# graph('temp', forecast_df, real_df)
# report()
