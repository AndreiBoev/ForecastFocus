import json
import requests
import pandas as pd


# import datetime
def Yandex(KEY):
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

    response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers, json={'query': query})
    data = response.json()
    df = pd.DataFrame(columns=['temp', 'wind', 'pressure', 'humidity'])
    for day in data['data']['weatherByPoint']['forecast']['days']:
        for time in day['parts']:
            df.loc[day['time'][0:10:] + time] = [day['parts'][time]['avgTemperature'], day['parts'][time]['windSpeed'],
                                                 day['parts'][time]['pressure'], day['parts'][time]['humidity']]
    df.to_csv('name.csv', sep=';')


def OpenWeather(KEY):
    params = {'lat': lat, 'lon': lon, 'APPID': KEY, 'cnt': days, 'units': 'metric'}
    url = 'https://pro.openweathermap.org/data/2.5/forecast/climate'
    response = requests.get(url, params=params)
    data = response.json()
    df3 = pd.DataFrame(columns=['temp', 'wind', 'pressure', 'humidity'])
    for day in data['list']:
        for time in ['morn', 'day', 'eve', 'night']:
            df3.loc[str(datetime.fromtimestamp(day['dt'])) + time] = [day['temp'][time], day['speed'], day['pressure'],
                                                                      day['humidity']]
    df3.to_csv('name.csv', sep=';')
def WeatherApi(KEY):
    url = 'http://api.weatherapi.com/v1/forecast.json'
    params = {'q': '55.803788,37.402695', 'KEY': KEY, 'days': '10', 'wind100kph': 'yes'}
    response = requests.get(url, params=params)

    data = response.json()

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