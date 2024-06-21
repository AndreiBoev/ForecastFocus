import os
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import maindesign  # Это наш конвертированный файл дизайна
from u_statistic import real_data, change, u_statistics, graph
import pandas as pd
from dateutil import parser as dtparser
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from GetForecast import GetForecastWindow

class App(QtWidgets.QMainWindow, maindesign.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        #self.pushButton_2.clicked.connect(self.getforecast()

        current_directory = os.getcwd() + "/data"
        for obj in os.listdir(current_directory):
            self.LWForecast.addItem(obj)    

        self.LWForecast.setCurrentRow(0)

        self.BtnCalculate.clicked.connect(self.make_statistic)

        self.BtnGetForecast.clicked.connect(self.open_getforecast_window)
        

    def open_getforecast_window(self):
        self.second_main_window = QMainWindow()
        self.second_window = GetForecastWindow()
        self.second_window.setupUi(self.second_main_window)
        self.second_main_window.show()

        self.LWForecast.clear()
        current_directory = os.getcwd() + "/data"
        for obj in os.listdir(current_directory):
            self.LWForecast.addItem(obj)

    def selection_changed(self):
        return self.LWForecast.selectedItems()[0]

    def make_statistic(self):
        self.calculation(self)
    
    def change(self, date, number):
        date_string = date
        date_obj = dtparser.parse(date_string)
        date_obj += datetime.timedelta(days=number)
        return date_obj.strftime('%Y-%m-%d')



    def calculation(cls, self):
        param = {'Давление': 'pressure', 'Влажность': 'humidity', 'Температура': 'temp', 'Скорость ветра': 'wind'}
        parameter = param[self.CBParameter.currentText()]
        folder_name = str(self.LWForecast.currentItem().text())
        lat = folder_name[22:32]
        lon = folder_name[32:43]

        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        fig3, ax3 = plt.subplots()

        fig11, ax11 = plt.subplots()
        fig21, ax21 = plt.subplots()
        fig31, ax31 = plt.subplots()
        
        
        canvas1 = FigureCanvas(fig1)
        layout1 = QVBoxLayout()
        layout1.addWidget(canvas1)
        self.frame.setLayout(layout1)

        canvas2 = FigureCanvas(fig2)
        layout2 = QVBoxLayout()
        layout2.addWidget(canvas2)
        self.frame_2.setLayout(layout2)

        canvas3 = FigureCanvas(fig3)
        layout3 = QVBoxLayout()
        layout3.addWidget(canvas3)
        self.frame_3.setLayout(layout3)
        
        canvas1 = FigureCanvas(fig11)
        layout1 = QVBoxLayout()
        layout1.addWidget(canvas1)
        self.frame.setLayout(layout1)
        


        for service_name in ["OpenWeather.csv", "YandexWeather.csv", "WeatherAPI.csv"]:

            df = pd.read_csv(f'data/{folder_name}/{service_name}', sep=';')
            df.set_index('time', inplace=True)

            real = real_data(lat, lon, change(df.iloc[0].name[0:10:], -1), change(df.iloc[-1].name[0:10:], 1))
            real = real[df.iloc[0].name:df.iloc[-1].name]

            u = u_statistics(df[parameter].tolist(), real[parameter].tolist())
            u = str(u)
            k = 3
            i = 0
            while True:
                if u[i] != '0' and u[i] != '.':
                    u = u[:i+3]
                    break
                i += 1

            

            if self.CBType.currentText() == "График":

                date_time =  list(map(lambda x: x[8::], real.index.tolist()))
                if service_name == "OpenWeather.csv":
                    self.LabOpenWeather.setText("OpenWeather = " + u)
                    ax1.plot(date_time, df[parameter].tolist(), marker='o', markersize=5)
                    ax1.plot(date_time, real[parameter].tolist(), marker='o', markersize=5)
                    ax1.set_xticks(date_time)
                    ax1.set_xticklabels(date_time, rotation=30)
                    ax1.set_xlabel('Date', fontsize=10)
                elif service_name == "YandexWeather.csv":
                    self.LabYandexWeather.setText(f"YandexWeather = " + u)
                    ax2.plot(date_time, df[parameter].tolist(), marker='o', markersize=5)
                    ax2.plot(date_time, real[parameter].tolist(), marker='o', markersize=5)
                    ax2.set_xticks(date_time)
                    ax2.set_xticklabels(date_time, rotation=30)
                    ax2.set_xlabel('Date', fontsize=10)
                    plt.tight_layout()
                else:
                    self.LabWeatherAPI.setText(f"WeatherAPI = " + u)
                    ax3.plot(date_time, df[parameter].tolist(), marker='o', markersize=5)
                    ax3.plot(date_time, real[parameter].tolist(), marker='o', markersize=5)
                    ax3.set_xticks(date_time)
                    ax3.set_xticklabels(date_time, rotation=30)
                    ax3.set_xlabel('Date', fontsize=10)
                    plt.tight_layout()
            else:

                date_time =  list(map(lambda x: x[8::], real.index.tolist()))
                if service_name == "OpenWeather.csv":
                    self.LabOpenWeather.setText("OpenWeather = " + u)
                    ax1.hist(df[parameter].tolist(), bins = 30)
                    ax1.hist(real[parameter].tolist(), bins = 30)
                elif service_name == "YandexWeather.csv":
                    self.LabYandexWeather.setText(f"YandexWeather = " + u)
                    ax21.hist(df[parameter].tolist(), bins = 30)
                    ax21.hist(real[parameter].tolist(), bins = 30)
                    plt.tight_layout()
                else:
                    self.LabWeatherAPI.setText(f"WeatherAPI = " + u)
                    ax31.hist(df[parameter].tolist(), bins = 30, color = 'blue')
                    ax31.hist(real[parameter].tolist(), bins = 30)
                    plt.tight_layout()
            


    def make_graph(column, forecast_df, real_df, mode):
        units_of_measurement = {'pressure': 'давление, мм.рт.ст.', 'humidity': 'влажность, %',
                                'wind': 'скорость ветра, м/с', 'temp': 'температура, °C'}
        y2 = forecast_df[column].tolist()
        y1 = real_df[column].tolist()
        x = list(map(lambda x: x[8::], forecast_df.index.tolist()))
        if mode == 'график':
            plt.title('реальные и прогнозируемые данные')
            plt.plot(x, y1, '-', x, y2, '--', marker='o', markersize=7)
            plt.xlabel('дата и время')
        else:
            width = 0.35
            fig, ax = plt.subplots()
            ax.bar(x, y1, width, label='реальные данные')
            ax.bar(x, y2, width, label='прогнозируемые данные')
            ax.set_title('реальные и прогнозируемые данные')
            ax.legend(loc='lower left', title='данные')

        plt.ylabel(units_of_measurement[column])
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        fig = plt.gcf()
        fig.set_size_inches(9, 6)
        plt.show()
         

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()