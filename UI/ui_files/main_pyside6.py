# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1700, 850)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(320, 260, 202, 314))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.NEWGAME_BTN = QPushButton(self.verticalLayoutWidget)
        self.NEWGAME_BTN.setObjectName(u"NEWGAME_BTN")
        self.NEWGAME_BTN.setMinimumSize(QSize(200, 100))

        self.verticalLayout.addWidget(self.NEWGAME_BTN)

        self.LOADGAME_BTN = QPushButton(self.verticalLayoutWidget)
        self.LOADGAME_BTN.setObjectName(u"LOADGAME_BTN")
        self.LOADGAME_BTN.setMinimumSize(QSize(200, 100))

        self.verticalLayout.addWidget(self.LOADGAME_BTN)

        self.EXITGAME_BTN = QPushButton(self.verticalLayoutWidget)
        self.EXITGAME_BTN.setObjectName(u"EXITGAME_BTN")
        self.EXITGAME_BTN.setMinimumSize(QSize(200, 100))

        self.verticalLayout.addWidget(self.EXITGAME_BTN)

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
        self.NEWGAME_BTN.setText(QCoreApplication.translate("Form", u"\uc0c8\ub85c \ub9cc\ub4e4\uae30", None))
        self.LOADGAME_BTN.setText(QCoreApplication.translate("Form", u"\ubd88\ub7ec\uc624\uae30", None))
        self.EXITGAME_BTN.setText(QCoreApplication.translate("Form", u"\uc885\ub8cc\ud558\uae30", None))
    # retranslateUi

