import json
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# import datetime
load_dotenv()

YANDEX_KEY = str(os.getenv('YANDEX_API_KEY'))
OPEN_WEATHER_KEY = str(os.getenv('OPEN_WEATHER_API_KEY'))
WEATHER_API_KEY = str(os.getenv('WEATHER_API_KEY'))


def api(response):
    if response.status_code == 200:
        return response.json()
    else:
        print(f"request execution error, error code == {response.status_code}")
        return


def yandex(KEY):
    access_key = KEY
    headers = {
        "X-Yandex-API-Key": access_key
    }
    location = {'lat: 55.75697232932146,  lon: 37.614235566135356': 'RedSquare',
                'lat: 55.803788, lon: 37.402695': 'Strogino',
                'lat: 55.67012,  lon: 337.27954': 'shamrock'}
    for place in location.keys():
        query = """{
          weatherByPoint(request: {""" + place + """ }) {
          forecast {
            days(limit: 30) {
              time
              parts {
                morning {
                  avgTemperature
                  windSpeed
                  pressure
                  humidity
                }
                day {
                  avgTemperature
                  windSpeed
                  pressure
                  humidity
                }
                evening {
                  avgTemperature
                  windSpeed
                  pressure
                  humidity
                }
                night {
                  avgTemperature
                  windSpeed
                  pressure
                  humidity
                }
              }
            }
          }
        }
      }"""
        try:
            response = api(
                requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers, json={'query': query}))
            if (data := response):
                df = pd.DataFrame(columns=['temp', 'wind', 'pressure', 'humidity'])
                for day in data['data']['weatherByPoint']['forecast']['days']:
                    for time in day['parts']:
                        df.loc[day['time'][0:10:] + time] = [day['parts'][time]['avgTemperature'],
                                                             day['parts'][time]['windSpeed'],
                                                             day['parts'][time]['pressure'],
                                                             day['parts'][time]['humidity']]
                df.to_csv(location['place'] + '.csv', sep=';')
            else:
                print("Oh no, I couldn't get the data.")
        except Exception as e:
            print(f'request execution error: {e}')


def open_weather(KEY):
    params = {'lat': lat, 'lon': lon, 'APPID': KEY, 'cnt': days, 'units': 'metric'}
    url = 'https://pro.openweathermap.org/data/2.5/forecast/climate'
    try:
        response = api(requests.get(url, params=params))
        if (data := response):
            df3 = pd.DataFrame(columns=['temp', 'wind', 'pressure', 'humidity'])
            for day in data['list']:
                for time in ['morn', 'day', 'eve', 'night']:
                    df3.loc[str(datetime.fromtimestamp(day['dt'])) + time] = [day['temp'][time], day['speed'],
                                                                              day['pressure'],
                                                                              day['humidity']]
            df3.to_csv('name.csv', sep=';')
        else:
            print("Oh no, I couldn't get the data.")
    except Exception as e:
        print(f'request execution error: {e}')


def weather_api(KEY):
    url = 'http://api.weatherapi.com/v1/forecast.json'
    params = {'q': '55.803788,37.402695', 'KEY': KEY, 'days': '10', 'wind100kph': 'yes'}
    try:
        response = api(requests.get(url, params=params))
        if (data := response):
            def value(parametr, start, list):
                sum = 0
                for dict in list[start:start + 6]:
                    sum += dict[parametr]
                return round(sum / 6, ndigits=2)

            df2 = pd.DataFrame(columns=['temp', 'wind', 'pressure', 'humidity'])
            for day in data['forecast']['forecastday']:
                n = 0
                for time in ['morning', 'day', 'evening', 'night']:
                    df2.loc[time + day['date']] = [value('temp_c', n, day['hour']), value('wind_kph', n, day['hour']),
                                                   value('pressure_in', n, day['hour']) * 25.4,
                                                   value('humidity', n, day['hour'])]
                    n += 6
            df2.to_csv('name.csv', sep=';')
        else:
            print("Oh no, I couldn't get the data.")
    except Exception as e:
        print(f'request execution error: {e}')


