#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import locale
import numpy as np

import config
import utils
import vkapi

from ui import auth
from ui import tech_info
from ui import mainwindow


from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, \
    QMessageBox, QFileDialog, QInputDialog, QStyleFactory
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QThread, Qt, pyqtSignal


locale.setlocale(locale.LC_ALL, "")

# Главное окно приложения
window = None
# Техническая информация(окно)
tech_info_window = None
# Окно авторизации
auth_window = None

# стиль окна
sys.argv += ['--style', 'fusion']


# Окно авторизации
class Auth(QtWidgets.QMainWindow, auth.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(config.IconPath))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.statusBar().showMessage("2fa isn't supported")

        self.pushButton.clicked.connect(self.autorizations)
        self.pushButton.setShortcut("Return")


    def autorizations(self):
        try:
            login = self.lineEdit.text()
            password = self.lineEdit_2.text()

            path_api = utils.get_host_api(self.action.isChecked())
            path_oauth = utils.get_host_oauth(self.action.isChecked())

            self.statusBar().showMessage('Loading...')

            r = vkapi.autorization(login, password,
                vkapi.client_keys[0][0], vkapi.client_keys[0][1],
                None, None, path_oauth)

            # QMessageBox.about(self, "Message", str(r))

            json_str = json.dumps(r)
            resp = json.loads(json_str)

            if (resp.get('access_token') != None):

                self.statusBar().showMessage('Done!')
                access_token = resp['access_token']

                self.statusBar().showMessage('Getting refresh_token')

                getRefreshToken = vkapi.refreshToken(access_token, path_api)
                refresh_token = getRefreshToken["response"]["token"]

                DATA = {'access_token': access_token, 'token': refresh_token}
                utils.save_json("DATA", DATA)

                #Запуск главного окна
                self.window = MainWindow()
                self.hide()
                self.window.show()

            else:
                self.statusBar().showMessage('Login failed :(')
                QMessageBox.critical(self, "F*CK", str(resp))

        except Exception as e:
            self.statusBar().showMessage('Login failed :(')
            QMessageBox.critical(self, "F*CK", str(r))
            #self.window = MainWindow()
            #self.hide()
            #self.window.show()


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
        self.label.setText("Внутренний IP: " + ip)

    @pyqtSlot(str)
    def set_external_ip(self, ip):
        self.label_2.setText("Внешний IP: " + ip)

    @pyqtSlot(str)
    def set_hostname(self, hostname):
        self.label_4.setText("Hostname: " + hostname)

    @pyqtSlot(str)
    def set_location(self, location):
        self.label_3.setText("Location: " + location)


    def exit(self): self.close()


# Главное окно приложения         
class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(config.IconPath))
        self.setWindowFlags(QtCore.Qt.Window)

        self.pushButton_2.clicked.connect(self.LoadsListMusic)
        self.pushButton.clicked.connect(self.Downloads)
        self.action.triggered.connect(self.AboutMessage)
        self.action_2.setShortcut("Ctrl+Q")
        self.action_2.triggered.connect(self.Logout)
        self.action_3.triggered.connect(self.Donate)
        self.action_4.triggered.connect(self.TechInformation)
        #self.progressBar.setFormat("%{.2f}%".format('p'))
        self.progressBar.setFormat("%p%")
        self.action_4.setShortcut("Ctrl+T")


    def LoadsListMusic(self):
        try:
            with open('DATA', encoding='utf-8') as data_json:
                data_token = json.loads(data_json.read())

            access_token = data_token["access_token"]
            refresh_token = data_token["token"]

            try:
                path_api = utils.get_host_api(self.action_5.isChecked())
                path_oauth = utils.get_host_oauth(self.action_5.isChecked())

                data = vkapi.get_audio(refresh_token, path_api)
                utils.save_json('response.json', data)

                count_track = data['response']['count']
                i = 0

                QtWidgets.QTreeWidget.clear(self.treeWidget)

                for count in data['response']['items']:

                    test = QtWidgets.QTreeWidgetItem(self.treeWidget)

                    test.setText(0, str(i + 1))
                    test.setText(1, data['response']['items'][i]['artist'])
                    test.setText(2, data['response']['items'][i]['title'])
                    test.setText(3, utils.time_duration(data['response']['items'][i]['duration']))
                    test.setText(4, utils.unix_time_stamp_convert(data['response']['items'][i]['date']))

                    if (data['response']['items'][i]['is_hq']):
                        if (data['response']['items'][i]['is_explicit']):
                            test.setText(5, "HQ (E)")
                        else:
                            test.setText(5, "HQ")

                    if (data['response']['items'][i]['url'] == ""):
                        test.setText(6, "Недоступно")

                    i += 1

                self.label.setText("Всего аудиозаписей: " + str(count_track)
                    + " Выбрано: " + str(0) + " Загружено: " + str(0))

            except Exception as e:
                QMessageBox.critical(self, "F*CK", str(data))

        except OSError as e:
            QMessageBox.critical(self, "F*CK", str(e))


    def Downloads(self):
        try:  
            PATH = utils.get_path(self, self.action_7.isChecked(), QFileDialog)
            self.label_2.setText("Путь для скачивания: " + PATH)

            self.completed = 0
            downloads_list = []
            getSelected = self.treeWidget.selectedItems()

            for i in getSelected:
                downloads_list.append(int(i.text(0)))

            with open('response.json', encoding='utf-8') as data_json:
                data = json.loads(data_json.read())

            count_track = data['response']['count']

            #QApplication.processEvents()

            if (np.size(downloads_list) == 0):
                    QMessageBox.information(self, "Информация",
                     "Ничего не выбрано.")

            self.th = Downloads_file(downloads_list, PATH)
            self.th.progress_range.connect(self.progress)
            self.th.progress.connect(self.progressBar.setValue)
            self.th.loading_audio.connect(self.loading_audio)
            self.th.message.connect(self.label.setText)
            self.th.unavailable_audio.connect(self.unavailable_audio)
            self.th.finished.connect(self.finished_loader)
            self.th.start()

            #self.label_3.setText("Загружается:3")

        except Exception as e:
            QMessageBox.critical(self, "F*CK", str(e))


    @pyqtSlot()
    def finished_loader(self):
        QMessageBox.information(self, "Информация", "Аудиозаписи загружены")

    @pyqtSlot(str)
    def loading_audio(self, song_name):
        self.label_3.setText("Загружается: " + song_name)

    @pyqtSlot(str)
    def unavailable_audio(self, song_name):
        QMessageBox.warning(self, "Внимание",
         "Аудиозапись: " + song_name + " недоступна в вашем регионе")

    @pyqtSlot(int)
    def progress(self, range):
        self.progressBar.setRange(0, range)


    def AboutMessage(self):
        QMessageBox.about(
            self, "О программе",
            "<b>" + config.ApplicationName
            + "</b> - " + config.Description + "<br><br><b>Версия: </b>"
            + config.ApplicationVersion
            + "<br><b>Стадия: </b> "
            + config.ApplicationBranch
            + "<br><br>Данное ПО распространяется по лицензии "
            + "<a href=" + config.License +">MIT</a>, исходный код доступен"
            + " на <a href=" + config.SourceСode +">GitHub</a>"
        )


    def Donate(self):
        QMessageBox.about(
            self, "Помощь проекту",
            "<b>Дать разработчику на чай</b>"
            + "<br><br><b>QIWI: </b> <a href="
            + config.Qiwi
            + ">" + config.Qiwi + "</a>"
            + "<br><b>Яндекс.Деньги: "
            + "</b> <a href="
            + config.YandexMoney + ">410017272872402</a>"
        )


    def TechInformation(self):
        path_api = utils.get_host_api(self.action_5.isChecked())
        path_oauth = utils.get_host_oauth(self.action_5.isChecked())
        
        self.tech_info_window = TechInfo(path_api, path_oauth)


    def Logout(self):
        reply = QMessageBox.question(self, "Выход из аккаунта",
         "Вы точно хотите выйти из аккаунта?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if (utils.check_file_path("DATA")):
                os.remove("DATA")
            else:
                print("WTF?")

            if (utils.check_file_path("response.json")):
                os.remove("response.json")

            self.auth_window = Auth()
            self.auth_window.show()
            self.hide()
        else:
            pass


class Downloads_file(QThread):

    finished = pyqtSignal()
    progress_range = pyqtSignal(int)
    progress = pyqtSignal(int)
    loading_audio = pyqtSignal(str)
    message = pyqtSignal(str)
    unavailable_audio = pyqtSignal(str)

    def __init__(self, downloads_list, PATH):
        super().__init__()
        self.downloads_list = downloads_list
        self.PATH = PATH


    def __del__(self):
        #print(".... end thread.....")
        self.wait()


    def run(self):
        try:
            with open('response.json', encoding='utf-8') as data_json:
                data = json.loads(data_json.read())

            self.completed = 0

            count_track = data['response']['count']
            selected = np.size(self.downloads_list)


            for item in self.downloads_list:
                self.completed += 1
                
                artist = data['response']['items'][item-1]['artist']
                title = data['response']['items'][item-1]['title']

                msg = "Всего аудиозаписей: " + str(count_track) + " Выбрано: "\
                 + str(selected) + " Загружено: " + str(self.completed)

                song_name = artist + " - " + title

                filename = self.PATH + "/" + utils.remove_symbols(song_name) + ".mp3"
                url = data['response']['items'][item-1]['url']

                #total = int(utils.get_size_content(url))
                #self.progress_range.emit(total)

                if (data['response']['items'][item-1]['url'] == ""):
                    self.unavailable_audio.emit(song_name)

                else:
                    self.message.emit(msg)
                    self.loading_audio.emit(song_name)
                    utils.downloads_files_in_wget(url, filename, self.update_progress)
                    #utils.downloads_files(url, filename, self.progress)

            self.finished.emit()
            self.loading_audio.emit('')

        except Exception as e:
            pass


    def update_progress(self, current, total, width=80):
        self.progress_range.emit(total)
        self.progress.emit(current)


class NetworkInfo(QThread):

    internal_ip = pyqtSignal(str)
    external_ip = pyqtSignal(str)
    hostname = pyqtSignal(str)
    location = pyqtSignal(str)
    api = pyqtSignal(str)
    oauth = pyqtSignal(str)

    def __init__(self, host_api, host_oauth):
        super().__init__()
        self.host_api = host_api
        self.host_oauth = host_oauth


    def run(self):
        try:
            self.internal_ip.emit(utils.get_internal_ip())

            data = utils.get_network_info()
            loc = data['country'] + ", " + data['region'] + ", " + data['city']

            self.external_ip.emit(data['ip'])
            self.hostname.emit(data['hostname'])
            self.location.emit(loc)

        except:
            self.internal_ip.emit(utils.get_internal_ip())
            self.external_ip.emit(None)
            self.hostname.emit(None)
            self.location.emit(None)

        if utils.check_connection(self.host_api):
            status = "Хост: [" + self.host_api + "] - Доступен"
            self.api.emit(status)
        else:
            status = "Хост: [" + self.host_api + "] - Недоступен"
            self.api.emit(status)

        if utils.check_connection(self.host_oauth):
            status = "Хост: [" + self.host_oauth + "] - Доступен"
            self.oauth.emit(status)
        else:
            status = "Хост: [" + self.host_oauth + "] - Недоступен"
            self.oauth.emit(status)


    def __del__(self):
        print("Never Say Goodbye")
        self.wait()


def start():
    try:
        sys.dont_write_bytecode = True
        path = "DATA"
        app = QApplication(sys.argv)

        if (utils.check_file_path(path)):
            ex = MainWindow()
            ex.show()
            sys.exit(app.exec_())
        else:
            ex = Auth()
            ex.show()
            sys.exit(app.exec_())

    except Exception as e:
        sys.exit(app.exec_())


if __name__ == '__main__':
    start()
