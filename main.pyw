#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import datetime
import locale
import numpy as np

import config
import utils
import vkapi

import auth 
import tech_info
import mainwindow

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, \
     QMessageBox, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt


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
        self.setWindowFlags(Qt.WindowCloseButtonHint |
                            Qt.WindowMinimizeButtonHint)
        self.statusBar()
        
        self.pushButton.clicked.connect(self.autorizations)
        self.pushButton.setShortcut("Return")


    def autorizations(self):
        try:
            login = self.lineEdit.text()
            password = self.lineEdit_2.text()
            
            if self.action.isChecked():
                path_oauth = vkapi.OAUTH_PROXY
                path_api = vkapi.HOST_API_PROXY
            else:
                path_oauth = vkapi.OAUTH
                path_api = vkapi.HOST_API

            self.statusBar().showMessage('Loading...')
            r = vkapi.autorization(login, password, 
                vkapi.client_keys[0][0], vkapi.client_keys[0][1], path_oauth)
            
            # QMessageBox.about(self, "Message", str(r))
            
            json_str = json.dumps(r)
            resp = json.loads(json_str)

            if (resp.get('access_token') != None):
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

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(config.IconPath))
        self.setWindowFlags(Qt.WindowCloseButtonHint |
                            Qt.WindowMinimizeButtonHint)

        self.pushButton_3.clicked.connect(self.exit)
        self.pushButton_3.setShortcut("Return")

    def exit(self):
        self.close()


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


    def LoadsListMusic(self):
        try:
            with open('DATA', encoding='utf-8') as data_json:
                data_token = json.loads(data_json.read())

            access_token = data_token["access_token"]
            refresh_token = data_token["token"]

            try:
                if(self.action_5.isChecked()):
                    path_api = vkapi.HOST_API_PROXY
                else:
                    path_api = vkapi.HOST_API

                data = vkapi.get_audio(refresh_token, path_api)
                utils.save_json('response.json', data)

                count_track = data['response']['count']
                i = 0

                #QtWidgets.QTreeWidget.clear()
                for count in data['response']['items']:
                    test = QtWidgets.QTreeWidgetItem(self.treeWidget)

                    test.setText(0, str(i + 1))
                    test.setText(1, data['response']['items'][i]['artist'])
                    test.setText(2, data['response']['items'][i]['title'])
                    test.setText(3, utils.time_duration(data['response']['items'][i]['duration']))
                    test.setText(4, utils.unix_time_stamp_convert(data['response']['items'][i]['date']))

                    if (data['response']['items'][i]['is_hq']):
                        test.setText(5, "HQ")

                    if (data['response']['items'][i]['url'] == ""):
                        test.setText(6, "Недоступно")

                    i += 1

                self.label.setText(f"Всего аудиозаписей: {count_track}  Выбрано: {0}  Загружено: {0}")

            except Exception as e:
                QMessageBox.critical(self, "F*CK", str(data))

        except OSError as e:
            QMessageBox.critical(self, "F*CK", str(data))


    def Downloads(self):
        try:
            if (self.action_7.isChecked()):
                PATH = QFileDialog.getExistingDirectory(
                    self, "Выберите папку для скачивания", "", 
                    QFileDialog.ShowDirsOnly
                )

                if PATH == "":
                    QMessageBox.warning(
                        self, "Внимание",
                        "Вы не выбрали папку для скачивания, поэтому "+
                        "аудиозапиcи будут загружены в директорию с программой"
                    )

                    PATH = os.getcwd()

                self.label_2.setText("Путь для скачивания: " + PATH)

            else:
                PATH = os.getcwd()
                self.label_2.setText("Путь для скачивания: " + PATH)

            self.completed = 0
            downloads_list = []
            getSelected = self.treeWidget.selectedItems()
            
            for i in getSelected:
                downloads_list.append(int(i.text(0)))

            with open('response.json', encoding='utf-8') as data_json:
                data = json.loads(data_json.read())

            self.progressBar.setRange(0, np.size(downloads_list))
            count_track = data['response']['count']

            QApplication.processEvents()

            if (np.size(downloads_list) == 0):
                    QMessageBox.information(self, "Информация",
                     "Ничего не выбрано.")

            for item in downloads_list:           
                self.completed += 1

                artist = data['response']['items'][item-1]['artist']
                title = data['response']['items'][item-1]['title']

                song_name = artist + " - " + title

                filename = PATH + "/" + utils.remove_symbols(song_name) + ".mp3"
                url = data['response']['items'][item-1]['url']

                self.label_3.setText(f"Загружается: {song_name}")
                self.label.setText(f"Всего аудиозаписей: " + str(count_track) 
                    + "  Выбрано: " + str(np.size(downloads_list)) 
                    + "  Загружено: "+ str(self.completed))

                if (data['response']['items'][item-1]['url'] == ""):
                    QMessageBox.warning(self, "Внимание", "Аудиозапись: " 
                        + song_name + " недоступна в вашем регионе") 
                else:
                    QApplication.processEvents()
                    utils.downloads_files_in_wget(url, filename)

                    self.progressBar.setValue(self.completed)

            QMessageBox.information(self, "Информация", "Аудиозаписи загружены")
            self.label_3.setText("Загружается:")
                         
        except Exception as e:
            QMessageBox.critical(self, "F*CK", str(e))


    def AboutMessage(self):
        QMessageBox.about(
            self, "О программе",
             "<b>" + config.ApplicationName 
            + "</b> - " + config.Description + "<br><br><b>Версия: </b>"
            + config.ApplicationVersion
            + "<br><b>Стадия: </b> " 
            + config.ApplicationBranch
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
            + config.YandexMoney +">410017272872402</a>"
        )


    def TechInformation(self):
        self.tech_info_window = TechInfo()
        self.tech_info_window.show()


    def Logout(self):
        reply = QMessageBox.question(self, "Выход из аккаунта",
         "Вы точно хотите выйти из аккаунта?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            os.remove("DATA")

            if (utils.check_file_path("response.json")):
                os.remove("response.json")    

            self.auth_window = Auth()
            self.auth_window.show()
            self.hide()
        else:
            pass


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
