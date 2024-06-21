from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QDate, QRegExp
from PyQt5.QtWidgets import QMessageBox, qApp
from PyQt5.QtGui import QRegExpValidator, QIcon
import json
import requests
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

YANDEX_KEY = str(os.getenv('YANDEX_API_KEY'))
OPEN_WEATHER_KEY = str(os.getenv('OPEN_WEATHER_API_KEY'))
WEATHER_API_KEY = str(os.getenv('WEATHER_API_KEY'))


class GetForecastWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(450, 520)
        MainWindow.setMaximumSize(QtCore.QSize(700, 600))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(13)
        MainWindow.setFont(font)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off) # изменение иконки
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowIcon(QIcon('logo.ico'))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.LELng = QtWidgets.QLineEdit(self.centralwidget)

        reg_exp = QRegExp("[0-9.]*")                                        # только числа и точка на ввод координат
        validator = QRegExpValidator(reg_exp)
        self.LELng.setValidator(validator)

        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.LELng.setFont(font)
        self.LELng.setObjectName("LELng")
        self.LELng.setStyleSheet("selection-background-color: rgb(73, 140, 81)")
        self.gridLayout.addWidget(self.LELng, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.LELat = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.LELat.setFont(font)
        self.LELat.setStyleSheet("")
        self.LELat.setObjectName("LELat")
        self.LELat.setStyleSheet("selection-background-color: rgb(73, 140, 81)")

        reg_exp = QRegExp("[0-9.]*")                                        # только числа и точка на ввод координат
        validator = QRegExpValidator(reg_exp)
        self.LELat.setValidator(validator)

        self.gridLayout.addWidget(self.LELat, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.CalChoose = QtWidgets.QCalendarWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.CalChoose.setFont(font)
        self.CalChoose.setStyleSheet("selection-background-color: rgb(118, 227, 131);\n"
"selection-color: rgb(255, 255, 255);")
        self.CalChoose.setObjectName("CalChoose")
        self.CalChoose.setSelectedDate(QDate.currentDate().addDays(10)) # начальная выбранная дата больше на 10 дней
        self.selected_date = self.CalChoose.selectedDate()
        self.verticalLayout_3.addWidget(self.CalChoose)
        self.LabChoose = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.LabChoose.setFont(font)
        self.LabChoose.setObjectName("LabChoose")
        self.verticalLayout_3.addWidget(self.LabChoose)
        self.BtnGet = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(13)
        self.BtnGet.setFont(font)
        self.BtnGet.setStyleSheet("background-color: rgb(118, 227, 131);\n"
"color: rgb(255, 255, 255);")
        self.BtnGet.setObjectName("BtnGet")
        self.verticalLayout_3.addWidget(self.BtnGet)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        
        qApp.setStyleSheet("QMessageBox QPushButton { color: white; background-color: rgb(73, 140, 81); font: 13pt \"Comic Sans MS\";} \
                           QMessageBox QLabel { font: 13pt \"Comic Sans MS\"; }")                                                            # изменение стиля окна об ошибке

        self.CalChoose.clicked.connect(self.show_selected_interval)                    # выбор даты

        self.BtnGet.clicked.connect(self.getting)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Получение прогноза погоды"))
        self.label.setText(_translate("MainWindow", "Координаты"))
        self.label_2.setText(_translate("MainWindow", "Lat:"))
        self.label_3.setText(_translate("MainWindow", "Lng:"))
        self.label_4.setText(_translate("MainWindow", "Конечная дата"))
        self.LabChoose.setText(_translate("MainWindow", "Выбрано на 10 дней вперёд"))
        self.BtnGet.setText(_translate("MainWindow", "Получить"))


    def show_selected_interval(self):
        days_diff = QDate.currentDate().daysTo(self.CalChoose.selectedDate())
        if days_diff >= 2 and days_diff <=10:
            self.LabChoose.setText(f'Выбрано на {days_diff} дней вперёд')
            self.selected_date = self.CalChoose.selectedDate()
        else:                                                                               
            self.CalChoose.setSelectedDate(self.selected_date)                         # обработка неверной даты
            error = QMessageBox()
            error.setWindowTitle("Некорректная дата")
            error.setText("Указана некорректная дата")
            error.setIcon(QMessageBox.Warning)

            error.setStandardButtons(QMessageBox.Ok)

            if days_diff < 2:
                error.setInformativeText("Выбранный промежуток не может быть короче 2-х дней")
            else:
                error.setInformativeText("Выбранный промежуток не может быть длиннее 10-и дней\n (Для прогнозирования на больший период необходимо приобрести премиум-ключ)")

            error.exec()

    def clear_cord(self, cord):
        if cord == "Lat":
            self.LELat.setText("")
        else:
            self.LELng.setText("")  


    def NoCord(self, cord):
        error = QMessageBox()
        error.setWindowTitle("Некорректные координаты")
        
        if cord == "Lat":
            error.setText("Не существует такого значения ширины")
            error.setInformativeText("Пожалуйста, введите значение, принадлежащее промежутку (-180; 180)")
        else:
            error.setText("Не существует такого значения долготы")
            error.setInformativeText("Пожалуйста, введите значение, принадлежащее промежутку (-90; 90)")
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.buttonClicked.connect(self.clear_cord)
        self.clear_cord(cord)
        error.exec()

    def nonumbers(self, cord):
        error = QMessageBox()
        error.setWindowTitle("Некорректные координаты")
        if cord == "Lat":
            error.setText("Значение широты указаны некорректно")
            error.buttonClicked.connect(lambda: self.clear_cord("Lat"))
            error.setInformativeText("Пожалуйста, вводите только действительные числа, принадлежащее промежутку\n (-180; 180)")
        else:
            error.setText("Значение долготы указаны некорректно")
            error.buttonClicked.connect(lambda: self.clear_cord("Lng"))
            error.setInformativeText("Пожалуйста, вводите только действительные числа, принадлежащее промежутку\n (-90; 90)")
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec()

    def api(self, response, webs):
        if response.status_code == 200:
            return response.json()
        else:
            self.cant_do_request(response.status_code, webs)
            return
        
    def cant_do_request(self, e, webs):
        error = QMessageBox()
        error.setWindowTitle("Ошибка выполнения запроса")
        error.setText(f"Запрос на {webs} не может быть выполнен")
        error.setInformativeText(f"Ошибка получения запроса: {e}")
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec()
    
    def cant_get_data(self, webs):
        error = QMessageBox()
        error.setWindowTitle("Ошибка получения данных")
        error.setText(f"Данные c {webs} не могут быть получены")
        error.setInformativeText("Попробуйте запросить данные ещё раз позже")
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec()

    def succ_get(self):
        succ = QMessageBox()
        succ.setWindowTitle("Запрос выполнен")
        succ.setText(f"Данные успешно получены")
        succ.setIcon(QMessageBox.Information)
        succ.setStandardButtons(QMessageBox.Ok)
        succ.exec()

    def yandex(self, KEY, name, days, lat, lon):
        access_key = KEY
        headers = {
            "X-Yandex-API-Key": access_key
        }
        query = """{
        weatherByPoint(request: {""" + f'lat:{lat}, lon:{lon}' + """ }) {
        forecast {
            days(limit:""" + str(days) + """) {
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
            response = self.api(
                requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers, json={'query': query}), "YanexWeather")
            if (data := response):
                df = pd.DataFrame(columns=['temp', 'wind', 'pressure', 'humidity'])
                for day in data['data']['weatherByPoint']['forecast']['days']:
                    for time in day['parts']:
                        df.loc[day['time'][0:10:] + time] = [day['parts'][time]['avgTemperature'],
                                                            day['parts'][time]['windSpeed'],
                                                            day['parts'][time]['pressure'],
                                                            day['parts'][time]['humidity']]
                df.to_csv(f'{name}.csv', sep=';', index_label="time")
            else:
                self.cant_get_data("YandexWeather")
        except Exception as e:
            self.cant_do_request(e, "YanexWeather")


    def open_weather(self, KEY, name, days, lat, lon, ):
        params = {'lat': lat, 'lon': lon, 'APPID': KEY, 'cnt': days, 'units': 'metric'}
        url = 'https://pro.openweathermap.org/data/2.5/forecast/climate'
        try:
            response = self.api(requests.get(url, params=params), "OpenWeather")
            if (data := response):
                df3 = pd.DataFrame(columns=['temp', 'wind', 'pressure', 'humidity'])
                for day in data['list']:
                    for time in ['morn', 'day', 'eve', 'night']:
                        df3.loc[str(datetime.fromtimestamp(day['dt']))[0:10:] + (
                            time if time == 'day' or time == 'night' else time + 'ing')] = [day['temp'][time], day['speed'],
                                                                                day['pressure'],
                                                                                day['humidity']]
                df3.to_csv(f'{name}.csv', sep=';', index_label="time")
            else:
                self.cant_get_data("OpenWeather")
        except Exception as e:
            self.cant_do_request(e, "OpenWeather")


    def weather_api(self, KEY, name, days, lat, lon):
        url = 'http://api.weatherapi.com/v1/forecast.json'
        params = {'q': f'{lat},{lon}', 'KEY': KEY, 'days': days, 'wind100kph': 'yes'}
        try:
            response = self.api(requests.get(url, params=params), "WeatherAPI")
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
                        df2.loc[day['date'] + time] = [value('temp_c', n, day['hour']), value('wind_kph', n, day['hour']),
                                                    value('pressure_in', n, day['hour']) * 25.4,
                                                    value('humidity', n, day['hour'])]
                        n += 6
                df2.to_csv(f'{name}.csv', sep=';', index_label="time")
            else:
                self.cant_get_data("WeatherAPI")
        except Exception as e:
            self.cant_do_request(e, "WeatherAPI")

    def date_to_str(self, date):
        if date < 10:
            return "0" + str(date)
        return str(date)

    def do_folder_name(self, day, mon, year, lday, lmon, lyear, lat, lng):
        day_s = self.date_to_str(day)
        mon_s = self.date_to_str(mon)
        year_s = self.date_to_str(year)
        lday_s = self.date_to_str(lday)
        lmon_s = self.date_to_str(lmon)
        lyear_s = self.date_to_str(lyear)
        
        lat_s = f"{lat:.6f}"
        lng_s = f"{lng:.6f}"

        return day_s + '.' + mon_s + '.' + year_s + "-" + lday_s + '.' + lmon_s + '.' + lyear_s + '_' + lat_s + '.' + lng_s

    def getting(self):
        try:
            Lat = float(str(self.LELat.text()))
        except:
            self.nonumbers("Lat")
            return
        try:
            Lng = float(str(self.LELng.text()))
        except:
            self.nonumbers("Lng")
            return 
        if Lat <= 180 and Lat >= -180:
            if Lng <= 90 and Lng >= -90:
                days = QDate.currentDate().daysTo(self.CalChoose.selectedDate())
                cur_day = QDate.currentDate().day()
                cur_mon = QDate.currentDate().month()
                cur_year = QDate.currentDate().year()
                last_day = self.selected_date.day()
                last_mon = self.selected_date.month()
                last_year = self.selected_date.year()

                folder_name = self.do_folder_name(cur_day, cur_mon, cur_year, last_day, last_mon, last_year, Lat, Lng)
                path = f"data/{folder_name}"
                os.makedirs(path)

                self.open_weather(OPEN_WEATHER_KEY, path + "/OpenWeather",  days, str(Lat), str(Lng) )
                self.weather_api(WEATHER_API_KEY, path + "/WeatherAPI", days, str(Lat), str(Lng))
                self.yandex(YANDEX_KEY, path + "/YandexWeather", days, str(Lat), str(Lng))

                self.succ_get()


            else:
                self.NoCord("Lng")
        else:
            self.NoCord("Lat")
            
        


'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GetForecastWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())'''
