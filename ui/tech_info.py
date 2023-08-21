#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget

from config import config
from threads import NetworkInfo
from .window import tech_info


# Техническая информация
class TechInfo(QWidget, tech_info.Ui_Form):

    def __init__(self, host_api, host_oauth):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(config.IconPath))
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)

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
