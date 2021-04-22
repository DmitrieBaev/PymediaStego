# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InDialogWindow(object):
    def setupUi(self, InDialogWindow):
        InDialogWindow.setObjectName("MainWindow")
        InDialogWindow.resize(361, 91)
        self.centralwidget = QtWidgets.QWidget(InDialogWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.owner = QtWidgets.QLineEdit(self.centralwidget)
        self.owner.setGeometry(QtCore.QRect(10, 30, 341, 21))
        self.owner.setObjectName("owner")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 301, 16))
        self.label.setObjectName("label")
        self.btn_OK = QtWidgets.QPushButton(self.centralwidget)
        self.btn_OK.setGeometry(QtCore.QRect(277, 60, 75, 23))
        self.btn_OK.setObjectName("btn_OK")
        InDialogWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(InDialogWindow)
        QtCore.QMetaObject.connectSlotsByName(InDialogWindow)

    def retranslateUi(self, InDialogWindow):
        _translate = QtCore.QCoreApplication.translate
        InDialogWindow.setWindowTitle(_translate("MainWindow", "Редактирование копирайта"))
        self.label.setText(_translate("MainWindow", "Укажите владельца:"))
        self.btn_OK.setText(_translate("MainWindow", "ОК"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InDialogWindow = QtWidgets.QMainWindow()
    ui = Ui_InDialogWindow()
    ui.setupUi(InDialogWindow)
    InDialogWindow.show()
    sys.exit(app.exec_())
