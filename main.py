# Конвертация .ui в .py
# python -m PyQt5.uic.pyuic -x ui\diploma.ui -o ui\frame.py

# Системные библиотеки
import configparser, sys, os, webbrowser, time
from multiprocessing import Process
from threading import Thread

# Сторонние библиотеки
# pip install hurry.filesize
from hurry.filesize import size  # Конвертор размеров файлов
# pip install pyqt5
from PyQt5 import QtWidgets, QtGui

# Локальные модули
from ui_main import Ui_MainWindow
from ui_settings import Ui_SettingsWindow
#from inputdlg import Ui_InDialogWindow
from ui_help import Ui_HelpWindow
import modules.stego as Steganography, modules.win32 as FileInfo
from modules.aes import Encryptor as SyncEncr
from modules.rsa import Encryptor as ASyncEncr

# Глобальные переменные
import resources.var.globals


class MainWndProc(QtWidgets.QMainWindow):
    def __init__(self):
        # Подключение окна
        super(MainWndProc, self).__init__()  # Наследуем инициализацию окна от прородителя QtWidgets
        self.ui = Ui_MainWindow()  # Создаем объект класса, описывающего интерфейс
        self.ui.setupUi(self)  # Позиционируем все элементы интерфейса
        self.statement = False
        self.load_properties()
        # Обработчики кнопок
        self.ui.btn_show_settings.clicked.connect(self.show_settings)
        self.ui.btn_show_info.clicked.connect(self.show_help)
        self.ui.btn_enc_choose.clicked.connect(self.choose_carrier)
        self.ui.btn_enc.clicked.connect(self.encode)
        self.ui.btn_dec.clicked.connect(self.decode)
        self.ui.btn_show_log.clicked.connect(self.show_hide_changelog)

    def show_hide_changelog(self):
        if not self.statement:
            self.statement = True
            self.ui.btn_show_log.setIcon(self.ui.icon_hide)
            self.ui.resizeUi(self)
        else:
            self.statement = False
            self.ui.btn_show_log.setIcon(self.ui.icon_show)
            self.ui.resizeUi(self, Height=285)

    @staticmethod
    def load_properties():
        global DEGREE, FRAME_START, FRAME_COUNT, OUTPUT_DIR
        config = configparser.RawConfigParser()
        config.read("resources/conf/properties.ini")
        DEGREE = config.getint("SETTINGS", "degree_value")
        FRAME_START = config.getint("SETTINGS", "frame_start")
        FRAME_COUNT = config.getint("SETTINGS", "frame_count")
        OUTPUT_DIR = config.get("SETTINGS", "output_dir")

    def show_settings(self):
        self.next = SettingsWndProc()

    def show_help(self):
        self.next = HelpWndProc()

    def choose_carrier(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите видео файл", "", "TEST!!! (*.txt *.png *.jpg)", options=QtWidgets.QFileDialog.Options())
        if fileName:
            self.ui.le_enc_path_input.setText(fileName)
            self.ui.copyright.setPlainText(self.fill_copyright(fileName))

    @staticmethod
    def fill_copyright(path):
        global COPYRIGHT, DATE_CREATE, DATE_MODIFY, OWNER, NAME
        DATE_CREATE = time.strftime("%d.%m.%Y %H:%M", time.localtime(os.path.getctime(path)))
        DATE_MODIFY = time.strftime("%d.%m.%Y %H:%M", time.localtime(os.path.getmtime(path)))
        OWNER = FileInfo.get_file_info(path, 'short')
        NAME = os.path.basename(path)

        COPYRIGHT = f'Copyright: © {NAME},\n{DATE_CREATE}, {OWNER}\nAll Rights Reserved.'
        return COPYRIGHT

    def encode(self):
        self.loading('---ЗАЩИТА-ВИДЕО-АП---', 3)
        if self.ui.le_enc_path_input.text() == '':
            QtWidgets.QMessageBox.warning(self, 'Ошибка!', 'Невозможно выполнить процесс защиты файла авторским правом - не выбран видео файл', QtWidgets.QMessageBox.Ok)
            self.loading('Ошибка! Нехватка данных<br/>', 2)
            return 0
        global OUTPUT_DIR, NAME, COPYRIGHT, DATE_CREATE
        self.loading('Шифрование копирайта')
        # Ключ симметричного алгоритма шифрования
        key = '2yDynDCk5Njsvq2m'.encode()  # 16 байт - длина ключа в байтах
        copyright_byte = COPYRIGHT.encode()
        AES = SyncEncr(key)
        copyright_encrypted = AES.encrypt(copyright_byte)
        copyright_decrypted = AES.decrypt(copyright_encrypted)
        open(os.path.realpath(f'{OUTPUT_DIR}/tmp/{NAME}.AES.enc'), 'wb').write(copyright_encrypted)
        open(os.path.realpath(f'{OUTPUT_DIR}/tmp/{NAME}.AES.dec'), 'wb').write(copyright_decrypted)

        self.loading('Получение ЭЦП')
        RSA = ASyncEncr()
        signature = RSA.encrypt(self.ui.le_enc_path_input.text())
        correct = RSA.decrypt(self.ui.le_enc_path_input.text(), signature)
        self.loading('Лицензионная копия!', 1) if correct else self.loading('Пиратская копия!', 2)

        self.loading('Сохранение ключей ЭЦП')

        self.loading('Подготавка видео файла')

        self.loading('Выполнение процесса стеганографии')

        self.loading()
        webbrowser.open(os.path.realpath(OUTPUT_DIR))  # открываем папку в проводнике
        # os.system(f'start {os.path.realpath(self.ui.tb_out_folder.text())}')  # альтернатива

    def decode(self):
        self.loading('---ПРОВЕРКА-АП-ВИДЕО---', 3)
        if self.ui.le_dec_path_input_1.text() == '' or self.ui.le_dec_path_input_2.text() == '':
            QtWidgets.QMessageBox.warning(self, 'Ошибка!', 'Невозможно выполнить процесс проверки авторского права - не все файлы выбраны.', QtWidgets.QMessageBox.Ok)
            self.loading('Ошибка! Нехватка данных', 2)
            return 0

    def loading(self, msg='<p></p>', color=0):
        if not msg == '<p></p>':
            colors = ['rgb(250, 250, 250)', 'rgb(55, 250, 55)', 'rgb(250, 55, 55)', 'rgb(55, 55, 250)']
            self.ui.pte_change_log.appendHtml(f'<p style="color:{colors[color]}">[{time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())}]   {msg}</p>')
        else:
            self.ui.pte_change_log.appendHtml('<p></p>')


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
        self.show()  # Отобразить форму настроек
        self.config = configparser.RawConfigParser()  # Объект файла конфигурации
        self.config.read("resources/conf/properties.ini")
        self.load_properties()  # Подготовить последние сохраненные настройки приложения
        # Обработчики кнопок
        self.ui.btn_OK.clicked.connect(self.save_changes)  # Применение настроек
        self.ui.btn_cancel.clicked.connect(self.undo_changes)  # Откат настроек
        self.ui.btn_choose.clicked.connect(self.out_dir)

    def load_properties(self):
        self.ui.path_output.setText(self.config.get("SETTINGS", "output_dir"))
        degree_name = self.config.get("SETTINGS", "degree_name")
        if degree_name == "Worth":  self.ui.radio1.setChecked(True)
        elif degree_name == "Low":  self.ui.radio2.setChecked(True)
        elif degree_name == "Mid":  self.ui.radio3.setChecked(True)
        elif degree_name == "High": self.ui.radio4.setChecked(True)
        else: self.ui.radio2.setChecked(True)
        self.ui.spin_N.setProperty("value", self.config.getint("SETTINGS", "frame_start"))
        self.ui.spin_I.setProperty("value", self.config.getint("SETTINGS", "Frame_count"))

    def save_changes(self):
        self.config.set("SETTINGS", "output_dir", self.ui.path_output.text())
        degree_name, degree_value = "Low", 4
        if self.ui.radio1.isChecked():
            degree_name = "Worth"
            degree_value = 8
        if self.ui.radio2.isChecked():
            degree_name = "Low"
            degree_value = 4
        if self.ui.radio3.isChecked():
            degree_name = "Mid"
            degree_value = 2
        if self.ui.radio4.isChecked():
            degree_name = "High"
            degree_value = 1
        self.config.set("SETTINGS", "degree_name", degree_name)
        self.config.set("SETTINGS", "degree_value", degree_value)
        self.config.set("SETTINGS", "frame_start", self.ui.spin_N.value())
        self.config.set("SETTINGS", "frame_count", self.ui.spin_I.value())
        self.config.write(open("resources\conf\properties.ini", "w"))
        self.close()

    def undo_changes(self):
        self.close()

    def out_dir(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Укажите папку для сохранения результата")
        if dirName:
            self.ui.path_output.setText(dirName)


# class InputDialogProc(QtWidgets.QMainWindow):
#     def __init__(self):
#         # Подключение окна
#         super(InputDialogProc, self).__init__()  # Наследуем инициализацию окна от прородителя QtWidgets
#         self.ui = Ui_InDialogWindow()  # Создаем объект класса, описывающего интерфейс
#         self.ui.setupUi(self)  # Позиционируем все элементы интерфейса
#         self.show()
#         # Обработчики кнопок
#         self.ui.btn_OK.clicked.connect(self.save_changes)
#
#     def save_changes(self):
#         self.close()


if __name__ == '__main__':
    # Точка вход в программу
    app = QtWidgets.QApplication([])  # Инициализируем сам Qt
    application = MainWndProc()  # Инициализируем объект класса FRONTEND-а
    application.show()  # Отображаем окно
    sys.exit(app.exec())  # Закрываем процесс приложения по выходу
