#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import locale

import config
import utils
import vkapi

from ui import auth
from ui import tech_info
from ui import mainwindow

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMessageBox, QFileDialog, QInputDialog, QStyleFactory
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QThread, QObject, Qt, pyqtSignal


locale.setlocale(locale.LC_ALL, "")


# Окно авторизации
class Auth(QtWidgets.QMainWindow, auth.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(config.IconPath))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.statusBar().showMessage("2fa is supported :)")

        self.pushButton.clicked.connect(self.autorizations)
        self.pushButton.setShortcut("Return")


    def autorizations(self):
        try:
            
            login = self.lineEdit.text()
            password = self.lineEdit_2.text()

            isProxyOauth = utils.get_proxy_host(self.action.isChecked(), False)
            isProxyAPI = self.action.isChecked()

            self.statusBar().showMessage('Loading...')

            r = vkapi.autorization(login, password, isProxyOauth)

            # QMessageBox.about(self, "Message", str(r))

            if (r =="Error: 2fa isn't supported"):
                code, ok = QInputDialog.getText(self, "Код потверждения", "Введите код из СМС")

                if ok:
                    r = vkapi.autorization(login, password, isProxyOauth, str(code))
                else:
                    r = vkapi.autorization(login, password, isProxyOauth, "")

            resp = json.loads(json.dumps(r))

            if (resp.get('access_token') != None):

                self.statusBar().showMessage('Done!')
                access_token = resp['access_token']

                self.statusBar().showMessage('Getting refresh_token')

                getRefreshToken = vkapi.refreshToken(access_token, isProxyAPI)
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
        
        except vkapi.VKException as ex:
            QMessageBox.critical(self, "F*CK VK", str(ex))

        except Exception as e:
            self.statusBar().showMessage('Login failed :(')
            QMessageBox.critical(self, "F*CK", str(e))


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
        self.label_2.setText("Внешний IP: " + (ip or "Недоступно"))

    @pyqtSlot(str)
    def set_hostname(self, hostname):
        self.label_4.setText("Hostname: " + (hostname or "Недоступно"))
        
    @pyqtSlot(str)
    def set_location(self, location):
        self.label_3.setText("Location: " + (location or "Недоступно"))


    def exit(self): self.close()


# Главное окно приложения         
class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow, QObject):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(config.IconPath))
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.pushButton_2.clicked.connect(self.LoadsListMusic)
        self.pushButton.clicked.connect(self.Downloads)
        self.pushButton.setCheckable(True)
        self.action.triggered.connect(self.AboutMessage)
        self.action_2.setShortcut("Ctrl+Q")
        self.action_2.triggered.connect(self.Logout)
        self.action_4.triggered.connect(self.TechInformation)
        self.progressBar.setFormat("%p% (%v/%m)")
        self.action_4.setShortcut("Ctrl+T")

        self.th = None
        self.is_loaded = False
        self.data = None
        self.getSelected = []
        self.downloads_list = []
        self.PATH = ""


    def LoadsListMusic(self):
        try:
            self.pushButton.setEnabled(True)
            
            with open('DATA', encoding='utf-8') as data_json:
                data_token = json.loads(data_json.read())

            
            refresh_token = data_token["token"]
            
            isProxyAPI = self.action_5.isChecked()
            
            self.data = vkapi.get_audio(refresh_token, isProxyAPI)

            if(config.SaveToFile):
                utils.save_json('response.json', self.data)

            count_track = self.data['response']['count']
            i = 0

            QtWidgets.QTreeWidget.clear(self.treeWidget)

            for count in self.data['response']['items']:

                test = QtWidgets.QTreeWidgetItem(self.treeWidget)

                test.setText(0, str(i + 1))
                test.setText(1, count['artist'])
                test.setText(2, count['title'])
                test.setText(3, utils.time_duration(count['duration']))
                test.setText(4, utils.unix_time_stamp_convert(count['date']))

                if (count.get('is_hq')):
                    if (count.get('is_explicit')):
                        test.setText(5, "HQ (E)")
                    else:
                        test.setText(5, "HQ")

                else:
                    if count.get('is_explicit'):
                        test.setText(5, "E")


                if not (count.get('url', False)):
                    test.setText(6, "Недоступно")

                i += 1

            self.label.setText("Всего аудиозаписей: " + str(count_track) + " Выбрано: " + str(0) + " Загружено: " + str(0))
            self.is_loaded = True

        except vkapi.VKException as ex:
            QMessageBox.critical(self, "F*CK VK", str(ex))

        except Exception as e:
            QMessageBox.critical(self, "F*CK", str(e))


    def Downloads(self, started):
        try:
            if self.is_loaded != True:
                self.pushButton.setChecked(False)
                raise Exception("Вы не загрузили список аудиозаписей")

            if started:

                self.PATH = utils.get_path(self, self.action_7.isChecked(), QFileDialog)
                self.label_2.setText("Путь для скачивания: " + self.PATH)

                self.completed = 0
                self.getSelected = self.treeWidget.selectedItems()

                for i in self.getSelected:
                    self.downloads_list.append(int(i.text(0)))

                if (config.SaveToFile):
                    if (utils.file_exists('response.json')):
                        with open('response.json', encoding='utf-8') as data_json:
                            self.data = json.loads(data_json.read())
                    else:
                        raise Exception("File \"response.json\" not found")

                if (self.downloads_list.__len__() == 0):
                    QMessageBox.information(self, "Информация", "Ничего не выбрано.")

                self.pushButton.setText("Остановить")
                
                if(config.SaveToFile):
                    self.th = Downloads_file(self.PATH, self.downloads_list)
                else:
                    self.th = Downloads_file(self.PATH, self.downloads_list, self.data)

                self.th.progress_range.connect(self.progress)
                self.th.progress.connect(self.progressBar.setValue)
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
        self.getSelected = []
        self.downloads_list = []
        self.pushButton.setText("Скачать")
        self.pushButton.setChecked(False)
        self.progressBar.setValue(0)
        self.progressBar.setRange(0, 100)
        self.label_3.setText("Загружается: ")
        self.label.setText("Всего аудиозаписей: " + str(self.data['response']['count']) + " Выбрано: " + str(0) + " Загружено: " + str(0))


    @pyqtSlot()
    def finished_loader(self):
        QMessageBox.information(self, "Информация", "Аудиозаписи загружены")
        self.set_ui_default()

    @pyqtSlot(str)
    def aborted_download(self, err_msg):
        QMessageBox.critical(self, "F*CK", "Загрузка прервана. Причина: " + err_msg)
        self.set_ui_default()

    @pyqtSlot(str)
    def loading_audio(self, song_name):
        if len(song_name) > 115:
            self.label_3.setText("Загружается: " + song_name[0:115])
        else:
            self.label_3.setText("Загружается: " + song_name)

    @pyqtSlot(str)
    def unavailable_audio(self, song_name):
        QMessageBox.warning(self, "Внимание",
         "Аудиозапись: " + song_name + " недоступна в вашем регионе")

    @pyqtSlot(int, str)
    def content_restricted(self, id_restrict,  song_name):
        if id_restrict == 1:
            message = "Аудиозапись: " + song_name + " недоступна по решению правообладателя"
        elif id_restrict == 2:
            message = "Аудиозапись: " + song_name + " недоступна в вашем регионе по решению правообладателя"
        elif id_restrict == 5:
            message = "Доступ к аудиозаписи: " + song_name + " скоро будет открыт"
        
        QMessageBox.warning(self, "Внимание", message)

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


    def TechInformation(self):
        if (self.action_5.isChecked()):
            path_api = 'https://' + vkapi.HOST_API_PROXY
            path_oauth = 'https://' + vkapi.HOST_OAUTH_PROXY
        else:
            path_api = 'https://' + vkapi.HOST_API
            path_oauth = 'https://' + vkapi.HOST_OAUTH
        
        self.tech_info_window = TechInfo(path_api, path_oauth)


    def Logout(self):
        reply = QMessageBox.question(self, "Выход из аккаунта","Вы точно хотите выйти из аккаунта?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if (utils.file_exists("DATA")):
                os.remove("DATA")
            else:
                print("WTF?")

            if (utils.file_exists("response.json")):
                os.remove("response.json")

            self.auth_window = Auth()
            self.auth_window.show()
            self.hide()
        else:
            pass


class Downloads_file(QThread):

    finished = pyqtSignal()
    abort_download = pyqtSignal(str)
    progress_range = pyqtSignal(int)
    progress = pyqtSignal(int)
    loading_audio = pyqtSignal(str)
    message = pyqtSignal(str)
    unavailable_audio = pyqtSignal(str)
    content_restricted = pyqtSignal(int, str)

    def __init__(self, PATH, downloads_list=None, data=None):
        super().__init__()
        self.downloads_list = downloads_list
        self.data = data
        self.PATH = PATH


    def run(self):
        try:
            if(config.SaveToFile):
                if (utils.file_exists('response.json')):
                    with open('response.json', encoding='utf-8') as data_json:
                        self.data = json.loads(data_json.read())
                else:
                    raise Exception("File \"response.json\" not found")

            self.completed = 0

            count_track = self.data['response']['count']
            selected = self.downloads_list.__len__()

            for item in self.downloads_list:
                
                artist = self.data['response']['items'][item-1]['artist']
                title = self.data['response']['items'][item-1]['title']

                msg = "Всего аудиозаписей: " + str(count_track) + " Выбрано: " + str(selected) + " Загружено: " + str(self.completed)

                song_name = artist + " - " + title

                filename = self.PATH + "/" + utils.fix_file_name(song_name) + ".mp3"
                url = self.data['response']['items'][item-1]['url']


                if (self.data['response']['items'][item-1]['url'] == ""):
                    
                    if (self.data['response']['items'][item-1]['content_restricted']):
                        self.content_restricted.emit(int(self.data['response']['items'][item-1]['content_restricted']), song_name)

                    else:
                        self.unavailable_audio.emit(song_name)

                else:
                    self.message.emit(msg)
                    self.loading_audio.emit(song_name)
                    utils.downloads_files_in_wget(url, filename, self.update_progress)
                    #utils.downloads_files(url, filename, self.progress)
                    self.completed += 1

            self.finished.emit()
            self.loading_audio.emit('')

        except Exception as e:
            self.abort_download.emit(str(e))

    # Magic. Do not touch.
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
            if 'hostname' in data: self.hostname.emit(data['hostname'])
            self.location.emit(loc)

        except Exception:
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
        # self.wait()


def start():
    try:
        if "--version" in sys.argv:
            sys.exit(config.ApplicationName + " " +config.ApplicationVersion + " " + config.ApplicationBranch)
        
        path = "DATA"
        
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(config.IconPath))
        app.setApplicationName(config.ApplicationName)
        app.setApplicationVersion(config.ApplicationVersion)
        app.setStyle('Fusion')

        if (utils.file_exists(path)):
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