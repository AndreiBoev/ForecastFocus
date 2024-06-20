import os
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import maindesign  # Это наш конвертированный файл дизайна

from GetForecast import Ui_MainWindow

class App(QtWidgets.QMainWindow, maindesign.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        #self.pushButton_2.clicked.connect(self.getforecast())
        
        '''for obj in os.listdir("C://ForecastFocus"):
                 self.listWidget.addItem(obj)
'''
    def getforecast(self):
        self.new_window = Ui_MainWindow()
        self.new_window.show()  

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()