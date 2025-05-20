# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_game_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1700, 850)
        self.verticalLayoutWidget_2 = QWidget(Form)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(11, 14, 821, 821))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.CHARACTER_NAME = QLineEdit(self.verticalLayoutWidget_2)
        self.CHARACTER_NAME.setObjectName(u"CHARACTER_NAME")
        self.CHARACTER_NAME.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.CHARACTER_NAME)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.CLASS = QComboBox(self.verticalLayoutWidget_2)
        self.CLASS.setObjectName(u"CLASS")

        self.horizontalLayout_2.addWidget(self.CLASS)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.BACK_BTN = QPushButton(self.verticalLayoutWidget_2)
        self.BACK_BTN.setObjectName(u"BACK_BTN")

        self.horizontalLayout_3.addWidget(self.BACK_BTN)

        self.CREATE_BTN = QPushButton(self.verticalLayoutWidget_2)
        self.CREATE_BTN.setObjectName(u"CREATE_BTN")

        self.horizontalLayout_3.addWidget(self.CREATE_BTN)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(850, 0, 3, 851))
        self.line.setStyleSheet(u"background-color:black;max-width:1px;min-width:1px;")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Name:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Class: ", None))
        self.BACK_BTN.setText(QCoreApplication.translate("Form", u"\ub4a4\ub85c\uac00\uae30", None))
        self.CREATE_BTN.setText(QCoreApplication.translate("Form", u"\uc0c8\ub85c \ub9cc\ub4e4\uae30", None))
    # retranslateUi

