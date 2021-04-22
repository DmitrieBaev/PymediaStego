# Конвертация .ui в .py
# python -m PyQt5.uic.pyuic -x ui\diploma.ui -o ui\frame.py

# Системные библиотеки
import configparser, sys, os, webbrowser, time

# Сторонние библиотеки
from PyQt5 import QtWidgets  # pip install pyqt5
import yaml # pip install pyyaml

# Локальные модули
from resources.visual.ui_main import Ui_MainWindow
from resources.visual.ui_settings import Ui_SettingsWindow
#from inputdlg import Ui_InDialogWindow
from resources.visual.ui_help import Ui_HelpWindow
import modules.win32 as FileInfo
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
        global DEGREE, FRAME_START, FRAME_COUNT, OUTPUT_DIR, \
            U_FNAME, U_SNAME, U_LNAME, U_EMAIL
        config = configparser.RawConfigParser()
        config.read('resources/var/config.ini')
        DEGREE = config.getint("SETTINGS", "degree_value")
        FRAME_START = config.getint("SETTINGS", "frame_start")
        FRAME_COUNT = config.getint("SETTINGS", "frame_count")
        OUTPUT_DIR = config.get("SETTINGS", "output_dir")
        U_FNAME = config.get("LICENSE", "user_first_name")
        U_SNAME = config.get("LICENSE", "user_second_name")
        U_LNAME = config.get("LICENSE", "user_last_name")
        U_EMAIL = config.get("LICENSE", "user_email")


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
        global COPYRIGHT, F_DATE_CREATE, F_DATE_MODIFY, F_OWNER, F_NAME
        F_DATE_CREATE = time.strftime("%d.%m.%Y %H:%M", time.localtime(os.path.getctime(path)))
        F_DATE_MODIFY = time.strftime("%d.%m.%Y %H:%M", time.localtime(os.path.getmtime(path)))
        F_OWNER = FileInfo.get_file_info(path, 'short')
        F_NAME = os.path.basename(path)

        COPYRIGHT = f'Copyright: © {F_NAME},\n{F_DATE_CREATE}, {F_OWNER}\nAll Rights Reserved.'
        return COPYRIGHT

    def encode(self):
        def enc_crypt():
            global COPYRIGHT, U_FNAME, U_SNAME, U_LNAME, U_EMAIL
            AES = SyncEncr(option='generate', key_data=(U_FNAME + U_SNAME + U_LNAME))
            return AES.encrypt(COPYRIGHT.encode())

        def enc_stego():
            pass

        def enc_eds(path_to_file):
            RSA = ASyncEncr()
            return RSA.get_eds(path_to_file)

        def create_license(copyright_encrypted, EDS):
            global OUTPUT_DIR, \
                F_NAME, F_OWNER, F_DATE_CREATE, F_DATE_MODIFY, \
                U_FNAME, U_SNAME, U_LNAME, U_EMAIL
            license = {'FileInfo':
                           {'FileName': F_NAME,
                            'FileCreateDate': F_DATE_CREATE,
                            'FileModifyDate': F_DATE_MODIFY,
                            'FileOwner': F_OWNER},
                       'AdditionalInfo':
                           {'EDS': EDS,
                            'Copyright': copyright_encrypted},
                       'UserInfo':
                           {'UserName': U_FNAME,
                            'UserSurname': U_SNAME,
                            'UserFathername': U_LNAME,
                            'UserEmail': U_EMAIL}}
            # открываем файл на запись
            with open(f'{OUTPUT_DIR}/{F_NAME[:F_NAME.rindex(".")]}_license.yml', 'w') as fw:
                # сериализуем словарь `license` в формат YAML и записываем все в файл
                data = yaml.dump(license, fw, sort_keys=False, default_flow_style=False)

        self.loading('---ЗАЩИТА-ВИДЕО-АП---', 3)
        if self.ui.le_enc_path_input.text() == '':
            QtWidgets.QMessageBox.warning(self, 'Ошибка!', 'Невозможно выполнить процесс защиты файла авторским правом - не выбран видео файл', QtWidgets.QMessageBox.Ok)
            self.loading('Ошибка! Нехватка данных<br/>', 2)
            return 0

        global OUTPUT_DIR
        self.loading('Шифрование копирайта')
        copyright_encrypted = enc_crypt()

        self.loading('Получение ЭЦП')
        signature = enc_eds(self.ui.le_enc_path_input.text())

        self.loading('Конфигурация сертификата')
        create_license(copyright_encrypted, signature)

        self.loading()
        webbrowser.open(os.path.realpath(OUTPUT_DIR))  # открываем папку в проводнике

        # self.loading('---ЗАЩИТА-ВИДЕО-АП---', 3)
        # if self.ui.le_enc_path_input.text() == '':
        #     QtWidgets.QMessageBox.warning(self, 'Ошибка!', 'Невозможно выполнить процесс защиты файла авторским правом - не выбран видео файл', QtWidgets.QMessageBox.Ok)
        #     self.loading('Ошибка! Нехватка данных<br/>', 2)
        #     return 0
        # global OUTPUT_DIR, F_NAME, COPYRIGHT, F_DATE_CREATE
        # self.loading('Шифрование копирайта')
        # # Ключ симметричного алгоритма шифрования
        # key = b""  # 16 байт - длина ключа в байтах
        # copyright_byte = COPYRIGHT.encode()
        # AES = SyncEncr(option='generate')
        # copyright_encrypted = AES.encrypt(copyright_byte)
        # copyright_decrypted = AES.decrypt(copyright_encrypted)
        # open(os.path.realpath(f'{OUTPUT_DIR}/tmp/{NAME}.AES.enc'), 'wb').write(copyright_encrypted)
        # open(os.path.realpath(f'{OUTPUT_DIR}/tmp/{NAME}.AES.dec'), 'wb').write(copyright_decrypted)
        #
        # self.loading('Получение ЭЦП')
        # RSA = ASyncEncr()
        # signature = RSA.encrypt(self.ui.le_enc_path_input.text())
        # correct = RSA.decrypt(self.ui.le_enc_path_input.text(), signature)
        # self.loading('Лицензионная копия!', 1) if correct else self.loading('Пиратская копия!', 2)
        #
        # self.loading('Сохранение ключей ЭЦП')
        #
        # self.loading('Подготавка видео файла')
        #
        # self.loading('Выполнение процесса стеганографии')
        #
        # self.loading()
        # webbrowser.open(os.path.realpath(OUTPUT_DIR))  # открываем папку в проводнике
        # os.system(f'start {os.path.realpath(self.ui.tb_out_folder.text())}')  # альтернатива
        #
        # Правильная последовательность:
        # 1. Шифрование копирайта
        # 2. Стеганография
        # 3. ЭЦП
        # 4. Сертификат

    def decode(self):
        pass
        # self.loading('---ПРОВЕРКА-АП-ВИДЕО---', 3)
        # if self.ui.le_dec_path_input_1.text() == '' or self.ui.le_dec_path_input_2.text() == '':
        #     QtWidgets.QMessageBox.warning(self, 'Ошибка!', 'Невозможно выполнить процесс проверки авторского права - не все файлы выбраны.', QtWidgets.QMessageBox.Ok)
        #     self.loading('Ошибка! Нехватка данных', 2)
        #     return 0

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
        self.PATH_TO_CFG = 'resources/var/config.ini'
        self.config = configparser.RawConfigParser()  # Объект файла конфигурации
        self.config.read(self.PATH_TO_CFG)
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
        self.config.write(open(self.PATH_TO_CFG, "w"))
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
