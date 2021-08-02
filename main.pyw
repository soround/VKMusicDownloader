#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import json
import locale

import utils

from datetime import datetime

from ui import auth
from ui import tech_info
from ui import mainwindow

from config import config
from vkapi import VKLightOauth, VKLight, VKLightError, VKLightOauthError

from threads import DownloadsFile, NetworkInfo, LoadMusic

from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

locale.setlocale(locale.LC_ALL, "")


# Окно авторизации
class Auth(QtWidgets.QMainWindow, auth.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.window = None
        self.setupUi(self)
        self.setWindowIcon(QIcon(config.IconPath))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.statusBar().showMessage("2fa is supported :)")

        self.pushButton.clicked.connect(self.go)
        self.pushButton.setShortcut("Return")

        self.oauth = VKLightOauth(dict())

    def go(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        r = None

        self.statusBar().showMessage('Loading...')

        self.oauth = VKLightOauth(
            dict(
                login=login,
                password=password,
                proxy=self.action.isChecked()
            )
        )

        try:
            try:
                r = self.oauth.go()

            except VKLightOauthError as e:
                if 'need_validation' in e.error:
                    if 'ban_info' in dir(e):
                        return QMessageBox.critical(self, "F*CK", str(e))

                    code, ok = QInputDialog.getText(
                        self,
                        "Подтвердите номер",
                        "Мы отправили SMS с кодом на номер"
                    )

                    if ok:
                        self.oauth = VKLightOauth(
                            dict(
                                login=login,
                                password=password,
                                proxy=self.action.isChecked(),
                                code=code
                            )
                        )
                        r = self.oauth.go()
                else:
                    raise e

            except Exception as e:
                raise e

            self.statusBar().showMessage('Done!')

        except VKLightOauthError as e:

            if 'need_captcha' in e.error:
                return QMessageBox.critical(self, 'F*CK', 'F*CKING CAPTHA')
            else:
                return QMessageBox.critical(self, 'F*CK', str(e))

        except Exception as e:
            self.statusBar().showMessage('Login failed :(')
            QMessageBox.critical(self, "F*CK", str(e))

        else:

            access_token = r['access_token']
            refresh_token = ""
            user_id = r['user_id'] or ''

            api = VKLight(dict(
                    access_token=access_token,
                    proxy=self.action.isChecked()
                )
            )

            if not api.is_usage_domain_me():
                from vkapi import receipt
                self.statusBar().showMessage('Getting refresh_token')
                refresh_token = api.call(
                    "auth.refreshToken",
                    dict(
                        access_token=access_token,
                        receipt=receipt
                    )
                )['response']['token']

            data = {
                'access_token': access_token,
                'token': refresh_token,
                'user_id': user_id
            }
            utils.save_json(config.AuthFile, data)

            # Запуск главного окна
            self.window = MainWindow()
            self.hide()
            self.window.show()


# Техническая информация
class TechInfo(QWidget, tech_info.Ui_Form):

    def __init__(self, host_api, host_oauth):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(config.IconPath))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.pushButton_3.clicked.connect(self.exit)
        self.pushButton_3.setShortcut("Return")
        self.show()

        self.host_api = host_api
        self.host_oauth = host_oauth

        self.th = NetworkInfo(self.host_api, self.host_oauth)

        self.th.internal_ip.connect(self.set_internal_ip)
        self.th.external_ip.connect(self.set_external_ip)
        self.th.hostname.connect(self.set_hostname)
        self.th.location.connect(self.set_location)
        self.th.api.connect(self.label_5.setText)
        self.th.oauth.connect(self.label_6.setText)

        self.th.start()

    @pyqtSlot(str)
    def set_internal_ip(self, ip):
        self.label.setText(f"Внутренний IP: {ip}")

    @pyqtSlot(str)
    def set_external_ip(self, ip):
        self.label_2.setText("Внешний IP: " + (ip or "Недоступно"))

    @pyqtSlot(str)
    def set_hostname(self, hostname):
        self.label_4.setText("Hostname: " + (hostname or "Недоступно"))

    @pyqtSlot(str)
    def set_location(self, location):
        self.label_3.setText("Location: " + (location or "Недоступно"))

    def exit(self): self.close()


# Главное окно приложения         
class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.auth_window = None
        self.tech_info_window = None
        self.completed = 0
        self.setupUi(self)
        self.setWindowIcon(QIcon(config.IconPath))
        self.setWindowFlags(QtCore.Qt.Window)

        self.pushButton_2.clicked.connect(self.loads_list_music)
        self.pushButton.clicked.connect(self.download)
        self.pushButton.setCheckable(True)
        self.action.triggered.connect(self.about_message)
        self.action_2.setShortcut("Ctrl+Q")
        self.action_2.triggered.connect(self.logout)
        self.action_4.triggered.connect(self.tech_information)
        self.action_4.setShortcut("Ctrl+T")
        self.progressBar.setFormat("%p% (%v/%m)")

        self.api = VKLight(dict())
        self.data = None
        self.lm = None
        self.th = None
        self.is_loaded = False
        self.getSelected = []
        self.downloads_list = []
        self.PATH = ""
        self.count_track = 0
        self.user_id = None

    def loads_list_music(self):
        try:
            data_token = utils.read_json(config.AuthFile)
            access_token = data_token["access_token"]
            refresh_token = data_token["token"]
            self.user_id = data_token.get('user_id', None)

            self.api = VKLight(dict(
                    access_token=access_token,
                    proxy=self.action_5.isChecked()
                )
            )

            if not self.api.is_usage_domain_me():
                from vkapi import receipt
                if refresh_token == "":
                    refresh_token = self.api.call(
                        "auth.refreshToken",
                        dict(
                            access_token=access_token,
                            receipt=receipt
                        )
                    )['response']['token']

                self.api.access_token = refresh_token
                utils.save_json(config.AuthFile, dict(
                        access_token=access_token,
                        token=refresh_token,
                        user_id=self.user_id
                    )
                )

            self.lm = LoadMusic(self.api, self.user_id)

            self.lm.music.connect(self.fill_table)
            self.lm.error.connect(self.show_error)
            self.lm.count_tracks.connect(self.set_text)
            self.lm.warning_message_count_audios.connect(self.show_warning)
            self.lm.loaded.connect(self.pushButton_2.setEnabled)

            self.lm.start()
            self.is_loaded = True

        except (Exception, VKLightError)as ex:
            QMessageBox.critical(self, "F*CK", str(ex))

    def download(self, started):
        try:
            if not self.is_loaded:
                self.pushButton.setChecked(False)
                return QMessageBox.information(
                    self,
                    "Информация",
                    "Вы не загрузили список аудиозаписей"
                )

            self.downloads_list = [int(i.text(0)) - 1 for i in self.treeWidget.selectedItems()]

            if len(self.downloads_list) == 0:
                self.pushButton.setChecked(False)
                return QMessageBox.information(
                    self, "Информация", "Ничего не выбрано."
                )

            if started:

                self.PATH = utils.get_path(self,
                                           self.action_7.isChecked(), QFileDialog
                                           )
                self.label_2.setText("Путь для скачивания: " + self.PATH)
                self.pushButton.setText("Остановить")

                self.th = DownloadsFile(
                    self.count_track,
                    self.PATH,
                    self.downloads_list,
                    self.data
                )

                self.th.progress_range.connect(self.progress)
                self.th.progress.connect(self.progress_set_value)
                self.th.loading_audio.connect(self.loading_audio)
                self.th.message.connect(self.label.setText)
                self.th.unavailable_audio.connect(self.unavailable_audio)
                self.th.content_restricted.connect(self.content_restricted)
                self.th.finished.connect(self.finished_loader)
                self.th.abort_download.connect(self.aborted_download)
                self.th.start()

            else:
                self.th.terminate()
                self.set_ui_default()
                QMessageBox.information(self, "Информация", "Загрузка остановлена.")
                del self.th

        except Exception as e:
            QMessageBox.critical(self, "F*CK", str(e))
            self.pushButton.setText("Скачать")

    def set_ui_default(self):
        self.downloads_list = []
        self.pushButton.setText("Скачать")
        self.pushButton.setChecked(False)
        self.progressBar.setValue(0)
        self.progressBar.setRange(0, 100)
        self.progressBar.setFormat("%p% (%v/%m)")
        self.label_3.setText("Загружается: ")
        self.label.setText(
            f"Всего аудиозаписей: {str(self.count_track)}" +
            f" Выбрано: {0}" +
            f" Загружено: {0}"
        )

    @pyqtSlot(list)
    def fill_table(self, data):
        self.data = data
        QtWidgets.QTreeWidget.clear(self.treeWidget)

        for i, count in enumerate(data, 1):

            test = QtWidgets.QTreeWidgetItem(self.treeWidget)

            test.setText(0, str(i))
            test.setText(1, count.artist)
            test.setText(2, count.title)
            test.setText(3, utils.time_duration(count.duration))
            test.setText(4, utils.unix_time_stamp_convert(count.date))

            if count.is_hq:
                if count.is_explicit:
                    test.setText(5, "HQ (E)")
                else:
                    test.setText(5, "HQ")
            else:
                if count.is_explicit:
                    test.setText(5, "E")

            if count.url == "":
                test.setText(6, "Недоступно")

    @pyqtSlot(str)
    def show_error(self, error):
        # self.pushButton_2.setEnabled(True)
        QMessageBox.critical(self,
                             "F*CK", f"{error}"
                             )

    @pyqtSlot(str)
    def show_warning(self, msg):
        QMessageBox.warning(self,
                            "Внимание",
                            msg
                            )

    @pyqtSlot(int)
    def set_text(self, count_track):
        self.count_track = count_track
        self.label.setText(
            f"Всего аудиозаписей: {str(self.count_track)}" +
            f" Выбрано: {0}" +
            f" Загружено: {0}"
        )

    @pyqtSlot()
    def finished_loader(self):
        QMessageBox.information(self, "Информация", "Аудиозаписи загружены")
        self.set_ui_default()

    @pyqtSlot(str)
    def aborted_download(self, err_msg):
        QMessageBox.critical(self,
                             "F*CK", f"Загрузка прервана. Причина: {err_msg}"
                             )
        self.set_ui_default()

    @pyqtSlot(str)
    def loading_audio(self, song_name):
        self.label_3.setText(f"Загружается: {song_name[0:100]}")

    @pyqtSlot(str)
    def unavailable_audio(self, song_name):
        QMessageBox.warning(self,
                            "Внимание",
                            f"Аудиозапись: {song_name} недоступна в вашем регионе"
                            )

    @pyqtSlot(int, str)
    def content_restricted(self, id_restrict, song_name):
        message = ""
        if id_restrict == 1:
            message = f"Аудиозапись: {song_name} недоступна по решению правообладателя"
        elif id_restrict == 2:
            message = f"Аудиозапись: {song_name} недоступна в вашем регионе по решению правообладателя"
        elif id_restrict == 5:
            message = f"Доступ к аудиозаписи: {song_name} вскоре будет открыт." + \
                      "\nВы сможете её послушать после официального релиза"

        QMessageBox.warning(self, "Внимание", message)

    @pyqtSlot(int)
    def progress(self, _range):
        self.progressBar.setFormat("%p% ( %v KB / %m KB )")
        self.progressBar.setRange(0, int(_range / 1024))

    @pyqtSlot(int)
    def progress_set_value(self, value):
        self.progressBar.setValue(int(value / 1024))

    def about_message(self):
        QMessageBox.about(
            self, "О программе",
            "<b>" + config.ApplicationName
            + "</b> - " + config.Description + "<br><br><b>Версия: </b>"
            + config.ApplicationVersion
            + "<br><b>Стадия: </b> "
            + config.ApplicationBranch
            + "<br><br>Данное ПО распространяется по лицензии "
            + "<a href=" + config.License + ">MIT</a>, исходный код доступен"
            + " на <a href=" + config.SourceCode + ">GitHub</a>"
        )

    def tech_information(self):
        self.tech_info_window = TechInfo(
            VKLight(dict(proxy=self.action_5.isChecked())).baseURL,
            VKLightOauth(dict(proxy=self.action_5.isChecked())).baseURL
        )

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Выход из аккаунта", "Вы точно хотите выйти из аккаунта?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if utils.file_exists(config.AuthFile):
                os.remove(config.AuthFile)
            else:
                print("WTF?")

            if utils.file_exists("response.json"):
                os.remove("response.json")

            self.auth_window = Auth()
            self.auth_window.show()
            self.hide()
        else:
            pass


class CommandLineOptions():

    def __init__(self):
        super().__init__()
        self.api = None
        self.user_id = 0
        self.COUNT_LOADING_AUDIO = 200

    def export(self, user_id=0, filename=""):
        from math import ceil
        from models import Audio
        self.user_id = user_id if user_id else ...
    
        access_token = utils.read_json(config.AuthFile)['token']
        self.api = VKLight(dict(access_token=access_token))

        data = []
        count_calls = 1
        count_audios = 0
        try:
            count_audios = self.api.call("audio.get", {
                "user_id": self.user_id,
                "count": 0,
            })['response']['count']
            
            print(f"Получаю список аудиозаписей...")
            if count_audios > self.COUNT_LOADING_AUDIO:
                count_calls = ceil(count_audios / self.COUNT_LOADING_AUDIO)
                for i in range(count_calls):
                    try:
                        audios = self.api.call('audio.get', {
                                "user_id": self.user_id,
                                "offset": self.COUNT_LOADING_AUDIO * i
                            }
                        )
                        _data = [
                            Audio(item) for item in audios['response']['items']
                        ]
                        data = [*data, *_data]

                    except VKLightError as e:
                        exit(e)

                    if i != 0 and i % 10 == 0:
                        sleep(9)
            else:
                audios = self.api.call('audio.get', {"user_id": self.user_id})
                data = [Audio(item) for item in audios['response']['items']]
        except Exception as e:
            exit(e)

        audios_list = []
        for audio in data:
            audios_list.append(audio.__dict__)

        filename = f'{self.user_id}_EXPORTED_AUDIOS.json'
        utils.save_json(filename, {
            'expoted_time': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            'user_id': self.user_id,
            'count': count_audios,
            'items': audios_list
        })

        exit(f'Список аудиозаписей сохранен в {filename}')


def start():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-v', '--version', 
            action="store_true", 
            help='show this application version and exit'
        )
        parser.add_argument(
            '-e', '--export',
            dest='user_id',
            default=0,
            type=int,
            help='export user music in JSON format'
        )

        args = parser.parse_args()

        if args.version:
            sys.exit(config.ApplicationFullName)

        auth_file = config.AuthFile

        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(config.IconPath))
        app.setApplicationName(config.ApplicationName)
        app.setApplicationVersion(config.ApplicationVersion)
        app.setStyle('Fusion')

        if utils.file_exists(auth_file):
            
            if args.user_id:
                CommandLineOptions().export(user_id=args.user_id)
                exit()

            ex = MainWindow()
            ex.show()
            sys.exit(app.exec_())

        else:
            ex = Auth()
            ex.show()
            sys.exit(app.exec_())

    except Exception as e:
        print("F*CK: " + str(e))
        exit()


if __name__ == '__main__':
    start()
