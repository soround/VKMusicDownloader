#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

import cli
import utils
from cli import ExportMusic
from config import config
from ui import Auth
from ui import MainWindow


def start():
    try:
        args = cli.get_args()
        if args.version:
            sys.exit(config.ApplicationFullName)

        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(config.IconPath))
        app.setApplicationName(config.ApplicationName)
        app.setApplicationVersion(config.ApplicationVersion)
        app.setStyle('Fusion')
        auth_file = config.AuthFile

        if utils.file_exists(auth_file):
            if args.user_id:
                ExportMusic().export()
                exit()

            ex = MainWindow()
            ex.show()
            sys.exit(app.exec())

        else:
            ex = Auth()
            ex.show()
            sys.exit(app.exec())

    except Exception as e:
        print("F*CK: " + str(e))
        exit()


if __name__ == '__main__':
    start()
