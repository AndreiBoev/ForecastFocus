from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QDate, QRegExp
from PyQt5.QtWidgets import QMessageBox, qApp
from PyQt5.QtGui import QRegExpValidator, QIcon


class Ui_MainWindow(object):
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
        icon.addPixmap(QtGui.QPixmap("logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
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

        reg_exp = QRegExp("[0-9,]*")                                        # только числа и запятая на ввод координат
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

        reg_exp = QRegExp("[0-9,]*")                                        # только числа и запятая на ввод координат
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

    def getting(self):
        try:
            Lat = float(str(self.LELat.text()))
            try:
                Lng = float(str(self.LELng.text()))
                if Lat <= 180 and Lat >= -180:
                    if Lng <= 90 and Lng >= -90:
                        pass                                                                            # тут выполняются запросы
                    else:
                        self.NoCord("Lng")
                else:
                    self.NoCord("Lat")
            except:
                self.nonumbers("Lng")
        except:
            self.nonumbers("Lat")

        

    def clear_cord(self, cord):
        if cord == "Lat":
            self.LELat.setText("")
        else:
            self.LELng.setText("")  



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
