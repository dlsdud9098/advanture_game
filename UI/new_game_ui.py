
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QStackedWidget

from data.save_load import Player_SAVELOAD
from unit.player import Player


new_window = uic.loadUiType("./UI/ui_files/new_game_ui.ui")[0]

class NewGameWindow(QStackedWidget,new_window):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.set_class = None
        self.parent = parent
        
        self.player_svld = Player_SAVELOAD()
        
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
        player = Player(name=self.name, class_=set_class, unit_type='player')
        data = player.GetStatus()
        
        character_exist = self.player_svld.AddData(data)
        
        if character_exist == 1:
            QMessageBox.information(self, "Error", "닉네임이 이미 존재합니다.")
            return
        elif character_exist == 2:
            QMessageBox.information(self, "Error", "캐릭터의 생성 개수를 초과하였습니다.")
            return
        
        self.parent.StartMain(self.name)
        
            
    # 클래스 콤보박스 동기화
    def syncClass(self):
        self.CLASS.addItem("Warrior")
        