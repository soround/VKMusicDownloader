# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt6 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!


import os
from config import config
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self):
        self.action_4 = None
        self.action_2 = None
        self.action = None
        self.menu_3 = None
        self.menu_2 = None
        self.menu = None
        self.menubar = None
        self.progressBar = None
        self.label_2 = None
        self.label_3 = None
        self.frame_3 = None
        self.label = None
        self.verticalLayout_4 = None
        self.frame_2 = None
        self.action_7 = None
        self.verticalLayout_2 = None
        self.pushButton_2 = None
        self.treeWidget = None
        self.verticalLayout_3 = None
        self.frame = None
        self.gridLayout = None
        self.centralwidget = None
        self.pushButton = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(710, 495)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeWidget = QtWidgets.QTreeWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(621, 262))
        self.treeWidget.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.treeWidget.setFont(font)
        self.treeWidget.setMouseTracking(True)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
        self.treeWidget.setAcceptDrops(True)
        self.treeWidget.setAutoFillBackground(False)
        self.treeWidget.setLocale(QtCore.QLocale(QtCore.QLocale.Language.Russian, QtCore.QLocale.Country.Ukraine))
        self.treeWidget.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.treeWidget.setMidLineWidth(1)
        self.treeWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.treeWidget.setTabKeyNavigation(False)
        self.treeWidget.setProperty("showDropIndicator", True)
        self.treeWidget.setDragEnabled(False)
        self.treeWidget.setDragDropOverwriteMode(False)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.treeWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.treeWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.treeWidget.setRootIsDecorated(True)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setAllColumnsShowFocus(True)
        self.treeWidget.setColumnCount(7)
        self.treeWidget.setObjectName("treeWidget")

        self.treeWidget.header().setDefaultSectionSize(119)
        self.treeWidget.header().setHighlightSections(True)
        self.treeWidget.header().setSortIndicatorShown(False)

        self.treeWidget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.treeWidget.header().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.treeWidget.header().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.treeWidget.header().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.treeWidget.header().setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.verticalLayout_3.addWidget(self.treeWidget)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)

        self.verticalLayout_3.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setTabletTracking(False)
        self.label_2.setToolTipDuration(0)
        self.label_2.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.progressBar = QtWidgets.QProgressBar(self.frame_3)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.Direction.BottomToTop)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.progressBar.raise_()
        self.label_2.raise_()
        self.verticalLayout_3.addWidget(self.frame_3)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)
        self.pushButton.raise_()
        self.frame_3.raise_()
        self.pushButton_2.raise_()
        self.treeWidget.raise_()
        self.frame_2.raise_()
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 708, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)

        self.action = QtWidgets.QWidgetAction(MainWindow)
        self.action.setObjectName("action")

        self.action_2 = QtWidgets.QWidgetAction(MainWindow)
        self.action_2.setObjectName("action_2")

        self.action_4 = QtWidgets.QWidgetAction(MainWindow)
        self.action_4.setObjectName("action_4")

        self.action_7 = QtWidgets.QWidgetAction(MainWindow)
        self.action_7.setObjectName("action_7")
        self.action_7.setCheckable(True)

        self.menu.addAction(self.action_2)
        self.menu_2.addAction(self.action_4)
        self.menu_2.addAction(self.action)

        self.menu_3.addAction(self.action_7)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", config.ApplicationFullName))

        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Номер"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Исполнитель"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "Название"))
        self.treeWidget.headerItem().setText(3, _translate("MainWindow", "Длительность"))
        self.treeWidget.headerItem().setText(4, _translate("MainWindow", "Дата добавления"))
        self.treeWidget.headerItem().setText(5, _translate("MainWindow", "Tags"))
        self.treeWidget.headerItem().setText(6, _translate("MainWindow", "Доступность"))

        self.pushButton_2.setText(_translate("MainWindow", "Загрузить список аудиозаписей"))

        self.label.setText(_translate("MainWindow", "Всего аудиозаписей: Выбрано: Загружено:"))
        self.label_3.setText(_translate("MainWindow", "Загружается: "))
        self.label_2.setText(_translate("MainWindow", f"Путь для скачивания: {os.getcwd()}"))

        self.progressBar.setFormat(_translate("MainWindow", ""))

        self.pushButton.setText(_translate("MainWindow", "Скачать"))

        self.menu.setTitle(_translate("MainWindow", "Аккаунт"))
        self.menu_2.setTitle(_translate("MainWindow", "Помощь"))
        self.menu_3.setTitle(_translate("MainWindow", "Настройки"))

        self.action.setText(_translate("MainWindow", "О программе"))
        self.action_2.setText(_translate("MainWindow", "Выйти из аккаунта"))
        self.action_4.setText(_translate("MainWindow", "Техническая информация"))
        self.action_7.setText(_translate("MainWindow", "Выбрать папку для скачивания"))
