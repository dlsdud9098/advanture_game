import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QStackedWidget
import os
from saves.save_loads import SAVE_LOADS
from unit.player.player import Player

new_window = uic.loadUiType("./UI/ui_files/new_game_ui.ui")[0]

class NewGameWindow(QStackedWidget,new_window):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.set_class = None
        self.parent = parent
        
        # 클래스 목록 동기화
        self.syncClass()
        
        # 버튼 연결
        self.BACK_BTN.clicked.connect(self.BackPage)
        self.CREATE_BTN.clicked.connect(self.CreateCharacter)
        
        
    # 뒤로 가기(메인 페이지)
    def BackPage(self):
        self.parent.switch_to_main_menu()
    
    # 캐릭터 새로 만들기 버튼
    def CreateCharacter(self):
        self.name = self.CHARACTER_NAME.text()
        self.character_class = self.CLASS.currentText()
    
        # print(self.name, self.character_class)
        
        if self.character_class == 'Warrior':
            set_class = '전사'
        
    
        # 캐릭터 만들기
        player = Player(name=self.name, CLASS=set_class)
        data = player.get_status()
        
        svld = SAVE_LOADS()
        character_exist = svld.data_add(data)
        
        if character_exist:
            QMessageBox.information(self, "Error", "닉네임이 이미 존재합니다.")
            
        self.parent.switch_to_main_menu()
        
            
    # 클래스 콤보박스 동기화
    def syncClass(self):
        self.CLASS.addItem("Warrior")
        