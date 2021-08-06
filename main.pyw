#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import sys
import locale

import utils
from config import config

from ui import Auth
from ui import TechInfo
from ui import MainWindow
from cli import ExportMusic

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon


locale.setlocale(locale.LC_ALL, "")


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
                ExportMusic().export(user_id=args.user_id)
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
