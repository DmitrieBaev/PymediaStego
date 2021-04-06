# Конвертация .ui в .py
# python -m PyQt5.uic.pyuic -x ui\diploma.ui -o ui\frame.py

# Системные библиотеки
import sys, os, webbrowser

# Сторонние библиотеки
# pip install hurry.filesize
from hurry.filesize import size  # Конвертор размеров файлов
# pip install pyqt5
from PyQt5 import QtWidgets

from mainframe import Ui_MainWindow
from settings import Ui_SettingsWindow
from inputdlg import Ui_InDialogWindow
from help import Ui_HelpWindow


class MainWndProc(QtWidgets.QMainWindow):
    def __init__(self):
        # Подключение окна
        super(MainWndProc, self).__init__()  # Наследуем инициализацию окна от прородителя QtWidgets
        self.ui = Ui_MainWindow()  # Создаем объект класса, описывающего интерфейс
        self.ui.setupUi(self)  # Позиционируем все элементы интерфейса
        # Обработчики кнопок
        self.ui.btn_settings.clicked.connect(self.show_settings)
        self.ui.btn_help.clicked.connect(self.show_help)
        self.ui.btn_enc.clicked.connect(self.encode)
        self.ui.btn_dec.clicked.connect(self.decode)

    def debug(self, msg):
        QtWidgets.QMessageBox.warning(self, "Debug message", msg, QtWidgets.QMessageBox.Ok)

    def show_settings(self):
        self.next = SettingsWndProc()
        # settings = SettingsWndProc()
        # settings.show()

    def show_help(self):
        self.next = HelpWndProc()

    # def choose_carrier(self):
    #     fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите видео файл", "", "TEST!!! (*.png)", options=QtWidgets.QFileDialog.Options())
    #     if fileName:
    #         self.ui.tb_carrier.setText(fileName)
    #         self.ui.lbl_free_space.setText(f'UNKNOWN/{size(os.path.getsize(fileName))}')

    # def choose_folder(self):
    #     dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Укажите папку")
    #     if dirName:
    #         self.ui.tb_out_folder.setText(dirName)

    def encode(self):
        self.debug('Корректно ;)')
        # print(self.ui.tb_out_folder.text())
        # webbrowser.open(os.path.realpath(self.ui.tb_out_folder.text()))  # открываем папку в проводнике
        # os.system(f'start {os.path.realpath(self.ui.tb_out_folder.text())}')  # альтернатива

    def decode(self):
        self.debug('Корректно ;)')


class HelpWndProc(QtWidgets.QMainWindow):
    def __init__(self):
        # Подключение окна
        super(HelpWndProc, self).__init__()  # Наследуем инициализацию окна от прородителя QtWidgets
        self.ui = Ui_HelpWindow()  # Создаем объект класса, описывающего интерфейс
        self.ui.setupUi(self)  # Позиционируем все элементы интерфейса
        self.show()


class SettingsWndProc(QtWidgets.QMainWindow):
    def __init__(self):
        # Подключение окна
        super(SettingsWndProc, self).__init__()  # Наследуем инициализацию окна от прородителя QtWidgets
        self.ui = Ui_SettingsWindow()  # Создаем объект класса, описывающего интерфейс
        self.ui.setupUi(self)  # Позиционируем все элементы интерфейса
        self.show()
        # Обработчики кнопок
        self.ui.btn_OK.clicked.connect(self.save_changes)
        self.ui.btn_cancel.clicked.connect(self.undo_changes)

    def save_changes(self):
        self.close()

    def undo_changes(self):
        self.close()


class InputDialogProc(QtWidgets.QMainWindow):
    def __init__(self):
        # Подключение окна
        super(InputDialogProc, self).__init__()  # Наследуем инициализацию окна от прородителя QtWidgets
        self.ui = Ui_InDialogWindow()  # Создаем объект класса, описывающего интерфейс
        self.ui.setupUi(self)  # Позиционируем все элементы интерфейса
        self.show()
        # Обработчики кнопок
        self.ui.btn_OK.clicked.connect(self.save_changes)

    def save_changes(self):
        self.close()


if __name__ == '__main__':
    # Точка вход в программу
    app = QtWidgets.QApplication([])  # Инициализируем сам Qt
    application = MainWndProc()  # Инициализируем объект класса FRONTEND-а
    application.show()  # Отображаем окно
    sys.exit(app.exec())  # Закрываем процесс приложения по выходу
