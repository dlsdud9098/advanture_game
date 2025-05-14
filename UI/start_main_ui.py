from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel
    )
from saves.save_loads import SAVE_LOADS
from UI.inventory_ui import InventoryWindow

form_class = uic.loadUiType("./UI/ui_files/start_game_main_ui.ui")[0]

class StartMainWindow(QMainWindow, form_class):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.load_ui = None
        
        self.parent = parent
        self.player_data = None
        
        self.lv_label = self.findChild(QLabel, 'LV_LABEL')
        self.name_label = self.findChild(QLabel, 'NAME_LABEL')
        self.class_label = self.findChild(QLabel, 'CLASS_LABEL')
        self.hp_label = self.findChild(QLabel, 'HP_LABEL')
        self.mp_label = self.findChild(QLabel, 'MP_LABEL')
        self.money_label = self.findChild(QLabel, 'MONEY_LABEL')
        
        self.INVENTORY_BTN.clicked.connect(self.ViewInventory)

        self.name = None
        self.player_inventory = None
    # 플레이어 정보에 대한 내용을 새로고침(업데이트) 합니다.
    def refresh_widget(self):
        pass
    
    def ViewInventory(self):
        if not self.load_ui:  # 창이 이미 열려 있는지 확인
            self.load_ui = InventoryWindow(self, self.player_inventory)  # 부모로 현재 창을 전달
        self.load_ui.show()  # 새 창 표시
    
    # 메인 창에서 캐릭터 데이터 입력하기
    def load_player_data(self, name):     
        self.name = name   
        svld = SAVE_LOADS()
        player_data = svld.player_load(name)
        
        self.lv_label.setText(str(player_data['LV']))
        self.name_label.setText(str(player_data['name']))
        self.class_label.setText(str(player_data['CLASS']))
        self.hp_label.setText(str(player_data['hp']))
        self.mp_label.setText(str(player_data['mp']))
        self.money_label.setText(str(player_data['money']))
        
        self.player_inventory = player_data['inventory']