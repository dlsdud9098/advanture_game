from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QTableWidgetItem,
    QTableWidget,
    QMenu,
    QSizePolicy,
    QTabWidget
    )
from data.save_load import Player_SAVELOAD
from data.item_data import Item_SAVELOAD
from PyQt5.QtCore import Qt

from .item_view_ui import ItemViewWindow

from entity.item import Item
from entity.armor import Armor
from entity.consum import Consum

form_class = uic.loadUiType("./UI/ui_files/start_game_main_ui.ui")[0]

class StartMainWindow(QMainWindow, form_class):
    def __init__(self, parent, name):
        super().__init__()
        
        self.setupUi(self)
        self.load_ui = None