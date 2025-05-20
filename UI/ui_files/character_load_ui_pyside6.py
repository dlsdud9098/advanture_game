# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'character_load_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(850, 850)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(3, 10, 831, 821))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.BACK_BTN = QPushButton(self.verticalLayoutWidget)
        self.BACK_BTN.setObjectName(u"BACK_BTN")
        self.BACK_BTN.setMaximumSize(QSize(250, 25))

        self.gridLayout.addWidget(self.BACK_BTN, 0, 0, 1, 1)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMaximumSize(QSize(250, 25))

        self.gridLayout.addWidget(self.pushButton_3, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.character_load_layout = QVBoxLayout()
        self.character_load_layout.setObjectName(u"character_load_layout")

        self.verticalLayout.addLayout(self.character_load_layout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.BACK_BTN.setText(QCoreApplication.translate("Form", u"\ub4a4\ub85c\uac00\uae30", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"PushButton", None))
    # retranslateUi

