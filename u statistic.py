from functools import reduce
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import datetime
from dateutil import parser as dtparser

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
                                                   value('wind_kph', n, day['hour']) / 3.6,
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


df = pd.read_csv(r"file.csv", sep=';')
df.set_index('time', inplace=True)

real = real_data('55.803788', '37.402695', change(df.iloc[0].name[0:10:], -1), change(df.iloc[-1].name[0:10:], 1))
real = real[df.iloc[0].name:df.iloc[-1].name]

for column in df.columns:
    print(column, u_statistics(df[column].tolist(), real[column].tolist()))
