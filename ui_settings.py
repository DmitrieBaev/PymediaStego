# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("MainWindow")
        SettingsWindow.resize(291, 281)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 16))
        self.label.setObjectName("label")
        self.path_output = QtWidgets.QLineEdit(self.centralwidget)
        self.path_output.setGeometry(QtCore.QRect(30, 30, 171, 20))
        self.path_output.setReadOnly(True)
        self.path_output.setObjectName("path_output")
        self.btn_choose = QtWidgets.QPushButton(self.centralwidget)
        self.btn_choose.setGeometry(QtCore.QRect(210, 29, 75, 23))
        self.btn_choose.setObjectName("btn_choose")
        self.spin_N = QtWidgets.QSpinBox(self.centralwidget)
        self.spin_N.setGeometry(QtCore.QRect(230, 150, 51, 26))
        self.spin_N.setMinimum(5)
        self.spin_N.setMaximum(25)
        self.spin_N.setSingleStep(5)
        self.spin_N.setObjectName("spin_N")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 211, 16))
        self.label_2.setObjectName("label_2")
        self.radio1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radio1.setGeometry(QtCore.QRect(30, 90, 82, 17))
        self.radio1.setObjectName("radio1")
        self.radio2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radio2.setGeometry(QtCore.QRect(30, 110, 82, 17))
        self.radio2.setChecked(True)
        self.radio2.setObjectName("radio2")
        self.radio3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radio3.setGeometry(QtCore.QRect(140, 90, 82, 17))
        self.radio3.setObjectName("radio3")
        self.radio4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radio4.setGeometry(QtCore.QRect(140, 110, 82, 17))
        self.radio4.setObjectName("radio4")
        self.spin_I = QtWidgets.QSpinBox(self.centralwidget)
        self.spin_I.setGeometry(QtCore.QRect(230, 200, 51, 26))
        self.spin_I.setMinimum(1)
        self.spin_I.setMaximum(5)
        self.spin_I.setSingleStep(1)
        self.spin_I.setProperty("value", 1)
        self.spin_I.setObjectName("spin_I")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 150, 221, 26))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 200, 201, 26))
        self.label_4.setObjectName("label_4")
        self.btn_OK = QtWidgets.QPushButton(self.centralwidget)
        self.btn_OK.setGeometry(QtCore.QRect(120, 250, 75, 23))
        self.btn_OK.setObjectName("btn_OK")
        self.btn_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancel.setGeometry(QtCore.QRect(210, 250, 75, 23))
        self.btn_cancel.setObjectName("btn_cancel")
        SettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("MainWindow", "Настройки"))
        self.label.setText(_translate("MainWindow", "Выходной каталог:"))
        self.btn_choose.setText(_translate("MainWindow", "Указать"))
        self.label_2.setText(_translate("MainWindow", "Качество выходного видео файла:"))
        self.radio1.setText(_translate("MainWindow", "Хучшее"))  # degree = Worth; DEGREE = 8
        self.radio2.setText(_translate("MainWindow", "Низкое"))  # degree = Low; DEGREE = 4
        self.radio3.setText(_translate("MainWindow", "Среднее"))  # degree = Mid; DEGREE = 2
        self.radio4.setText(_translate("MainWindow", "Высокое"))  # degree = High; DEGREE = 1
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p>Встраивать информацию в каждые<br/>n кадров:</p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p>Количество подписуемых кадров:</p></body></html>"))
        self.btn_OK.setText(_translate("MainWindow", "ОК"))
        self.btn_cancel.setText(_translate("MainWindow", "Отмена"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QMainWindow()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec_())