# Системные библиотеки
import configparser, sys, os, webbrowser, time

# Сторонние библиотеки
from PyQt5 import QtWidgets  # pip install pyqt5
from PyQt5.QtCore import QThread
import yaml  # pip install pyyaml
from yaml.loader import SafeLoader

# Локальные модули
from resources.visual.ui_main import Ui_MainWindow
from resources.visual.ui_settings import Ui_SettingsWindow
from resources.visual.ui_help import Ui_HelpWindow
import modules.win32 as FileInfo
from modules.aes import Encryptor as SyncEncr
from modules.rsa import Encryptor as ASyncEncr
from modules.stego import Steganography as Stego

# Глобальные переменные
import resources.var.globals
_STATE = False


class LoadingThread(QThread):
    def __init__(self, QWindow, parent=None):
        super(LoadingThread, self).__init__(parent=parent)
        self.QWindow = QWindow

    def run(self):
        while _STATE:
            self.QWindow.btn_enc.setText('Подождите')
            time.sleep(0.25)
            self.QWindow.btn_enc.setText('Подождите.')
            time.sleep(0.25)
            self.QWindow.btn_enc.setText('Подождите..')
            time.sleep(0.25)
            self.QWindow.btn_enc.setText('Подождите...')
            time.sleep(0.25)


class MainWndProc(QtWidgets.QMainWindow):
    def __init__(self):
        # Подключение окна
        super(MainWndProc, self).__init__()  # Наследуем инициализацию окна от прородителя QtWidgets
        self.ui = Ui_MainWindow()  # Создаем объект класса, описывающего интерфейс
        self.ui.setupUi(self)  # Позиционируем все элементы интерфейса
        self.load_properties()
        # Обработчики кнопок
        self.ui.btn_show_settings.clicked.connect(self.show_settings)
        self.ui.btn_show_info.clicked.connect(self.show_help)
        self.ui.btn_enc_choose.clicked.connect(self.choose_carrier_enc)
        self.ui.btn_enc.clicked.connect(self.encode)
        self.ui.btn_dec.clicked.connect(self.decode)
        self.ui.btn_dec_choose_1.clicked.connect(self.choose_carrier_dec)
        self.ui.btn_dec_choose_2.clicked.connect(self.choose_license)
        self.LoadingThread_instance = LoadingThread(QWindow=self)

    @staticmethod
    def load_properties():
        global DEGREE, FRAME_START, FRAME_COUNT, OUTPUT_DIR, \
            U_FNAME, U_SNAME, U_LNAME, U_EMAIL, \
            GLOBAL_DECODING
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
        GLOBAL_DECODING = config.getboolean("SETTINGS", "inquiry")


    def show_settings(self):
        self.next = SettingsWndProc()

    def show_help(self):
        self.next = HelpWndProc()

    def choose_carrier_enc(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите видео файл", "",
                                                            "Видео файл (*.mp4 *.avi)",
                                                            options=QtWidgets.QFileDialog.Options())
        if fileName:
            self.ui.le_enc_path_input.setText(fileName)
            self.ui.copyright.setPlainText(self.fill_copyright(fileName))

    def choose_carrier_dec(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите видео файл", "",
                                                            "Видео файл (*.mp4 *.avi)",
                                                            options=QtWidgets.QFileDialog.Options())
        if fileName:
            self.ui.le_dec_path_input_1.setText(fileName)

    def choose_license(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл сертификата лицензированного файла", "",
                                                            "Сертификат лицензии файла (*.yml)",
                                                            options=QtWidgets.QFileDialog.Options())
        if fileName:
            self.ui.le_dec_path_input_2.setText(fileName)

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

        def enc_stego(copyright_encrypted, path=self.ui.le_enc_path_input.text()):
            global OUTPUT_DIR, F_NAME, DEGREE, FRAME_START, FRAME_COUNT
            s = Stego(degree=DEGREE,
                      i=FRAME_COUNT,
                      n=FRAME_START,
                      enc_copyright=copyright_encrypted)
            return s.encode_video(path_in=path,
                                  path_out=OUTPUT_DIR,
                                  fname=F_NAME)

        def enc_eds(path_to_video):
            RSA = ASyncEncr()
            return RSA.get_eds(path_to_video)

        def generate_props_key(copyright_encrypted):
            global DEGREE, FRAME_START, FRAME_COUNT
            return f'{DEGREE};{FRAME_COUNT};{FRAME_START}'.encode()

        def create_license(copyright_encrypted, EDS, output_dir, props_key):
            global F_NAME, F_OWNER, F_DATE_CREATE, F_DATE_MODIFY, \
                U_FNAME, U_SNAME, U_LNAME, U_EMAIL
            license = {'FileInfo':
                           {'FileName': F_NAME,
                            'FileCreateDate': F_DATE_CREATE,
                            'FileModifyDate': F_DATE_MODIFY,
                            'FileOwner': F_OWNER},
                       'AdditionalInfo':
                           {'EDS': EDS,
                            'Copyright': copyright_encrypted,
                            'Key': props_key},
                       'UserInfo':
                           {'UserName': U_FNAME,
                            'UserSurname': U_SNAME,
                            'UserFathername': U_LNAME,
                            'UserEmail': U_EMAIL}}
            # открываем файл на запись
            with open(f'{output_dir}/{F_NAME[:F_NAME.rindex(".")]}_license.yml', 'w') as fw:
                # сериализуем словарь `license` в формат YAML и записываем все в файл
                yaml.dump(license, fw, sort_keys=False, default_flow_style=False)  # data = ...

        if self.ui.le_enc_path_input.text() == '':
            QtWidgets.QMessageBox.warning(self, 'Ошибка!',
                                          'Невозможно выполнить процесс защиты файла авторским правом - не выбран видео файл',
                                          QtWidgets.QMessageBox.Ok)
            return 0

        _STATE = True
        self.LoadingThread_instance.start()
        self.load_properties()
        global F_NAME, OUTPUT_DIR
        copyright_encrypted = enc_crypt()
        enc_stego(copyright_encrypted)
        signature = enc_eds(f'{OUTPUT_DIR}/{F_NAME}')
        create_license(copyright_encrypted, signature, OUTPUT_DIR, generate_props_key(copyright_encrypted))
        _STATE = False
        webbrowser.open(os.path.realpath(OUTPUT_DIR))  # открываем папку в проводнике

    def decode(self):
        def dec_eds(signature, path=self.ui.le_dec_path_input_1.text()):
            RSA = ASyncEncr()
            return RSA.verify_eds(path, signature)

        def read_license(path=self.ui.le_dec_path_input_2.text()):
            with open(path) as f:
                return yaml.load(f, Loader=SafeLoader)

        if self.ui.le_dec_path_input_1.text() == '' or self.ui.le_dec_path_input_2.text() == '':
            QtWidgets.QMessageBox.warning(self, 'Ошибка!',
                                          'Невозможно выполнить процесс проверки авторского права - не все файлы выбраны.',
                                          QtWidgets.QMessageBox.Ok)
            return 0

        self.load_properties()
        global GLOBAL_DECODING
        certificate = read_license()
        if not GLOBAL_DECODING:
            license_status = dec_eds(certificate.get('AdditionalInfo').get('EDS'))
            license_status_msg = 'Лицензионная копия!' if license_status else 'Пиратская копия!'
            QtWidgets.QMessageBox.warning(self, 'Заключение проверки ЭЦП', license_status_msg, QtWidgets.QMessageBox.Ok)
        else:
            license_status = dec_eds(certificate.get('AdditionalInfo').get('EDS'))
            report = f'Электронно цифровая подпись видеофайла {"" if license_status else "не "}совпала со значением в сертификате.\n'
            properties = certificate.get('AdditionalInfo').get('Key')
            properties = properties.decode().split(';')
            s = Stego(degree=int(properties[0]),
                      i=int(properties[1]),
                      n=int(properties[2]),
                      enc_copyright=certificate.get('AdditionalInfo').get('Copyright'))
            report += f'Копирайт {"" if not s.decode_video(path_in=self.ui.le_dec_path_input_1.text()) else "не "}аутентичен. Целостность видеофайла не нарушена.'
            QtWidgets.QMessageBox.warning(self, 'Заключение глубокой проверки', report, QtWidgets.QMessageBox.Ok)


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
        if degree_name == "Worst":  self.ui.radio1.setChecked(True)
        elif degree_name == "Low":  self.ui.radio2.setChecked(True)
        elif degree_name == "Mid":  self.ui.radio3.setChecked(True)
        elif degree_name == "High": self.ui.radio4.setChecked(True)
        else: self.ui.radio2.setChecked(True)
        self.ui.spin_N.setProperty("value", self.config.getint("SETTINGS", "frame_start"))
        self.ui.spin_I.setProperty("value", self.config.getint("SETTINGS", "Frame_count"))
        self.ui.chb_inquiry.setChecked(True) if self.config.getboolean("SETTINGS", "inquiry") else self.ui.chb_inquiry.setChecked(False)

    def save_changes(self):
        self.config.set("SETTINGS", "output_dir", self.ui.path_output.text())
        degree_name, degree_value = "Low", 4
        if self.ui.radio1.isChecked():
            degree_name = "Worst"
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
        self.config.set("SETTINGS", "inquiry", self.ui.chb_inquiry.isChecked())
        self.config.write(open(self.PATH_TO_CFG, "w"))
        self.close()

    def undo_changes(self):
        self.close()

    def out_dir(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Укажите папку для сохранения результата")
        if dirName:
            self.ui.path_output.setText(dirName)


if __name__ == '__main__':
    # Точка вход в программу
    app = QtWidgets.QApplication([])  # Инициализируем сам Qt
    application = MainWndProc()  # Инициализируем объект класса FRONTEND-а
    application.show()  # Отображаем окно
    sys.exit(app.exec())  # Закрываем процесс приложения по выходу
