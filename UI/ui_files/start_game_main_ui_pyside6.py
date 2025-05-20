# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'start_game_main_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1700, 850)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 821, 821))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.SAVE_BTN = QPushButton(self.verticalLayoutWidget)
        self.SAVE_BTN.setObjectName(u"SAVE_BTN")

        self.horizontalLayout.addWidget(self.SAVE_BTN)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.scrollArea = QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 817, 743))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Chat_Text = QLineEdit(self.verticalLayoutWidget)
        self.Chat_Text.setObjectName(u"Chat_Text")

        self.horizontalLayout_2.addWidget(self.Chat_Text)

        self.Chat_Spend_BTN = QPushButton(self.verticalLayoutWidget)
        self.Chat_Spend_BTN.setObjectName(u"Chat_Spend_BTN")

        self.horizontalLayout_2.addWidget(self.Chat_Spend_BTN)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayoutWidget_2 = QWidget(Form)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(869, 10, 811, 821))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.armor_grid = QGridLayout()
        self.armor_grid.setObjectName(u"armor_grid")
        self.LEGGINGS_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.LEGGINGS_LABEL.setObjectName(u"LEGGINGS_LABEL")
        self.LEGGINGS_LABEL.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.LEGGINGS_LABEL, 3, 2, 1, 1)

        self.RING1_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.RING1_LABEL.setObjectName(u"RING1_LABEL")
        self.RING1_LABEL.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.RING1_LABEL, 2, 1, 1, 1)

        self.SHOSE_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.SHOSE_LABEL.setObjectName(u"SHOSE_LABEL")
        self.SHOSE_LABEL.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.SHOSE_LABEL, 4, 2, 1, 1)

        self.HELMAT_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.HELMAT_LABEL.setObjectName(u"HELMAT_LABEL")
        self.HELMAT_LABEL.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.HELMAT_LABEL, 0, 2, 1, 1)

        self.NECK_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.NECK_LABEL.setObjectName(u"NECK_LABEL")
        self.NECK_LABEL.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.NECK_LABEL, 1, 2, 1, 1)

        self.ARMOR_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.ARMOR_LABEL.setObjectName(u"ARMOR_LABEL")
        self.ARMOR_LABEL.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.ARMOR_LABEL, 2, 2, 1, 1)

        self.RING2_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.RING2_LABEL.setObjectName(u"RING2_LABEL")
        self.RING2_LABEL.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.RING2_LABEL, 2, 3, 1, 1)

        self.WEAPON_LEFT_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.WEAPON_LEFT_LABEL.setObjectName(u"WEAPON_LEFT_LABEL")
        self.WEAPON_LEFT_LABEL.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.WEAPON_LEFT_LABEL, 2, 4, 1, 1)

        self.WEAPON_RIGHT_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.WEAPON_RIGHT_LABEL.setObjectName(u"WEAPON_RIGHT_LABEL")
        self.WEAPON_RIGHT_LABEL.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.WEAPON_RIGHT_LABEL, 2, 0, 1, 1)

        self.BACKPACK_LABEL_2 = QLabel(self.verticalLayoutWidget_2)
        self.BACKPACK_LABEL_2.setObjectName(u"BACKPACK_LABEL_2")
        self.BACKPACK_LABEL_2.setAlignment(Qt.AlignCenter)

        self.armor_grid.addWidget(self.BACKPACK_LABEL_2, 3, 3, 1, 1)


        self.verticalLayout_2.addLayout(self.armor_grid)

        self.player_stat_grid = QGridLayout()
        self.player_stat_grid.setObjectName(u"player_stat_grid")
        self.label_18 = QLabel(self.verticalLayoutWidget_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_18, 6, 0, 1, 1)

        self.label_30 = QLabel(self.verticalLayoutWidget_2)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_30, 7, 2, 1, 1)

        self.label_19 = QLabel(self.verticalLayoutWidget_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_19, 7, 0, 1, 1)

        self.LV_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.LV_LABEL.setObjectName(u"LV_LABEL")
        self.LV_LABEL.setMinimumSize(QSize(130, 25))

        self.player_stat_grid.addWidget(self.LV_LABEL, 2, 1, 1, 1)

        self.ATTACK_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.ATTACK_LABEL.setObjectName(u"ATTACK_LABEL")

        self.player_stat_grid.addWidget(self.ATTACK_LABEL, 7, 3, 1, 1)

        self.MONEY_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.MONEY_LABEL.setObjectName(u"MONEY_LABEL")

        self.player_stat_grid.addWidget(self.MONEY_LABEL, 4, 3, 1, 1)

        self.label_10 = QLabel(self.verticalLayoutWidget_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_10, 4, 0, 1, 1)

        self.MP_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.MP_LABEL.setObjectName(u"MP_LABEL")

        self.player_stat_grid.addWidget(self.MP_LABEL, 3, 3, 1, 1)

        self.label_12 = QLabel(self.verticalLayoutWidget_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_12, 4, 2, 1, 1)

        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(130, 25))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_33 = QLabel(self.verticalLayoutWidget_2)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_33, 2, 4, 1, 1)

        self.label_17 = QLabel(self.verticalLayoutWidget_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_17, 5, 0, 1, 1)

        self.DEFENSE_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.DEFENSE_LABEL.setObjectName(u"DEFENSE_LABEL")

        self.player_stat_grid.addWidget(self.DEFENSE_LABEL, 8, 3, 1, 1)

        self.NAME_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.NAME_LABEL.setObjectName(u"NAME_LABEL")

        self.player_stat_grid.addWidget(self.NAME_LABEL, 3, 1, 1, 1)

        self.label_6 = QLabel(self.verticalLayoutWidget_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(130, 0))
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_6, 2, 2, 1, 1)

        self.HP_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.HP_LABEL.setObjectName(u"HP_LABEL")

        self.player_stat_grid.addWidget(self.HP_LABEL, 2, 3, 1, 1)

        self.label_20 = QLabel(self.verticalLayoutWidget_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_20, 8, 0, 1, 1)

        self.label_7 = QLabel(self.verticalLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_7, 3, 2, 1, 1)

        self.LUCK_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.LUCK_LABEL.setObjectName(u"LUCK_LABEL")

        self.player_stat_grid.addWidget(self.LUCK_LABEL, 8, 1, 1, 1)

        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_3, 3, 0, 1, 1)

        self.CLASS_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.CLASS_LABEL.setObjectName(u"CLASS_LABEL")

        self.player_stat_grid.addWidget(self.CLASS_LABEL, 4, 1, 1, 1)

        self.AGI_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.AGI_LABEL.setObjectName(u"AGI_LABEL")

        self.player_stat_grid.addWidget(self.AGI_LABEL, 6, 1, 1, 1)

        self.STR_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.STR_LABEL.setObjectName(u"STR_LABEL")

        self.player_stat_grid.addWidget(self.STR_LABEL, 5, 1, 1, 1)

        self.INT_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.INT_LABEL.setObjectName(u"INT_LABEL")

        self.player_stat_grid.addWidget(self.INT_LABEL, 7, 1, 1, 1)

        self.BACKPACK_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.BACKPACK_LABEL.setObjectName(u"BACKPACK_LABEL")

        self.player_stat_grid.addWidget(self.BACKPACK_LABEL, 2, 5, 1, 1)

        self.label_31 = QLabel(self.verticalLayoutWidget_2)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label_31, 8, 2, 1, 1)

        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.player_stat_grid.addWidget(self.label, 3, 4, 1, 1)

        self.BACKPACKSIZE_LABEL = QLabel(self.verticalLayoutWidget_2)
        self.BACKPACKSIZE_LABEL.setObjectName(u"BACKPACKSIZE_LABEL")

        self.player_stat_grid.addWidget(self.BACKPACKSIZE_LABEL, 3, 5, 1, 1)


        self.verticalLayout_2.addLayout(self.player_stat_grid)

        self.XP_BAR = QProgressBar(self.verticalLayoutWidget_2)
        self.XP_BAR.setObjectName(u"XP_BAR")
        self.XP_BAR.setValue(0)

        self.verticalLayout_2.addWidget(self.XP_BAR)

        self.InventoryTab = QTabWidget(self.verticalLayoutWidget_2)
        self.InventoryTab.setObjectName(u"InventoryTab")
        self.InventoryTab.setMaximumSize(QSize(811, 541))
        self.all_items = QWidget()
        self.all_items.setObjectName(u"all_items")
        self.all_items.setMaximumSize(QSize(803, 535))
        self.InventoryTable = QTableWidget(self.all_items)
        self.InventoryTable.setObjectName(u"InventoryTable")
        self.InventoryTable.setGeometry(QRect(-2, -1, 811, 541))
        self.InventoryTable.setMaximumSize(QSize(811, 541))
        self.InventoryTab.addTab(self.all_items, "")
        self.armor_items = QWidget()
        self.armor_items.setObjectName(u"armor_items")
        self.armor_items.setMaximumSize(QSize(803, 535))
        self.ArmorTable = QTableWidget(self.armor_items)
        self.ArmorTable.setObjectName(u"ArmorTable")
        self.ArmorTable.setGeometry(QRect(-2, -1, 811, 541))
        self.ArmorTable.setMaximumSize(QSize(821, 551))
        self.InventoryTab.addTab(self.armor_items, "")
        self.consumable_items = QWidget()
        self.consumable_items.setObjectName(u"consumable_items")
        self.consumable_items.setMaximumSize(QSize(811, 16777215))
        self.ConsumableTable = QTableWidget(self.consumable_items)
        self.ConsumableTable.setObjectName(u"ConsumableTable")
        self.ConsumableTable.setGeometry(QRect(-2, -1, 811, 541))
        self.ConsumableTable.setMaximumSize(QSize(811, 541))
        self.InventoryTab.addTab(self.consumable_items, "")

        self.verticalLayout_2.addWidget(self.InventoryTab)


        self.retranslateUi(Form)

        self.InventoryTab.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.SAVE_BTN.setText(QCoreApplication.translate("Form", u"\uc800\uc7a5\ud558\uae30", None))
        self.Chat_Spend_BTN.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.LEGGINGS_LABEL.setText(QCoreApplication.translate("Form", u"leggings", None))
        self.RING1_LABEL.setText(QCoreApplication.translate("Form", u"ring1", None))
        self.SHOSE_LABEL.setText(QCoreApplication.translate("Form", u"shoses", None))
        self.HELMAT_LABEL.setText(QCoreApplication.translate("Form", u"Helmat", None))
        self.NECK_LABEL.setText(QCoreApplication.translate("Form", u"neck", None))
        self.ARMOR_LABEL.setText(QCoreApplication.translate("Form", u"armor", None))
        self.RING2_LABEL.setText(QCoreApplication.translate("Form", u"ring2", None))
        self.WEAPON_LEFT_LABEL.setText(QCoreApplication.translate("Form", u"weapon_left", None))
        self.WEAPON_RIGHT_LABEL.setText(QCoreApplication.translate("Form", u"weapon_right", None))
        self.BACKPACK_LABEL_2.setText(QCoreApplication.translate("Form", u"backpack", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"AGI: ", None))
        self.label_30.setText(QCoreApplication.translate("Form", u"Attack: ", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"INT: ", None))
        self.LV_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.ATTACK_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.MONEY_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Class: ", None))
        self.MP_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Money: ", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Lv: ", None))
        self.label_33.setText(QCoreApplication.translate("Form", u"BackPack: ", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"STR: ", None))
        self.DEFENSE_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.NAME_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Hp: ", None))
        self.HP_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"LUCK: ", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Mp: ", None))
        self.LUCK_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Name: ", None))
        self.CLASS_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.AGI_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.STR_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.INT_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.BACKPACK_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.label_31.setText(QCoreApplication.translate("Form", u"Defense: ", None))
        self.label.setText(QCoreApplication.translate("Form", u"Max BackPack Size: ", None))
        self.BACKPACKSIZE_LABEL.setText(QCoreApplication.translate("Form", u"None", None))
        self.InventoryTab.setTabText(self.InventoryTab.indexOf(self.all_items), QCoreApplication.translate("Form", u"\uc804\uccb4", None))
        self.InventoryTab.setTabText(self.InventoryTab.indexOf(self.armor_items), QCoreApplication.translate("Form", u"\uc7a5\ube44", None))
        self.InventoryTab.setTabText(self.InventoryTab.indexOf(self.consumable_items), QCoreApplication.translate("Form", u"\uc18c\ubaa8\ud488", None))
    # retranslateUi

