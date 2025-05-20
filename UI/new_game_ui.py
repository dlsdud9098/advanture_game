from PySide6.QtWidgets import (
    QMessageBox, 
    QStackedWidget,
    QPushButton, 
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from data.save_load import Player_SAVELOAD
from unit.player import Player


class NewGameWindow(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.player_svld = Player_SAVELOAD()
        
        # .ui 파일 로드
        loader = QUiLoader()
        ui_file = QFile("./UI/ui_files/new_game_ui.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        self.setLayout(self.ui.layout())  # QDialog에 로드한 UI 배치

        self.setCentralWidget(self.ui) if hasattr(self, 'setCentralWidget') else None

        # UI 위젯 멤버로 가져오기
        self.BACK_BTN = self.ui.findChild(type(self.ui), "BACK_BTN")
        self.CREATE_BTN = self.ui.findChild(type(self.ui), "CREATE_BTN")
        self.CHARACTER_NAME = self.ui.findChild(type(self.ui), "CHARACTER_NAME")
        self.CLASS = self.ui.findChild(type(self.ui), "CLASS")

        self.syncClass()

        self.BACK_BTN = self.ui.findChild(QPushButton, "BACK_BTN")
        self.CREATE_BTN = self.ui.findChild(QPushButton, "CREATE_BTN")
        
        # 버튼 시그널 연결
        self.BACK_BTN.clicked.connect(self.BackPage)
        self.CREATE_BTN.clicked.connect(self.CreateCharacter)

    def BackPage(self):
        self.parent.switch_to_main_menu()

    def CreateCharacter(self):
        name = self.CHARACTER_NAME.text()
        character_class = self.CLASS.currentText()

        set_class = None
        if character_class == 'Warrior':
            set_class = '전사'

        player = Player(name=name, class_=set_class, unit_type='player')
        data = player.GetStatus()

        character_exist = self.player_svld.AddData(data)

        if character_exist == 1:
            QMessageBox.information(self, "Error", "닉네임이 이미 존재합니다.")
            return
        elif character_exist == 2:
            QMessageBox.information(self, "Error", "캐릭터의 생성 개수를 초과하였습니다.")
            return

        self.parent.StartMain(name)

    def syncClass(self):
        self.CLASS.addItem("Warrior")
