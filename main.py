# from unit.player import Player
# from display.display_select import MainDisplay
# from game.main_game import MAIN_GAME

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from UI.main_menu_ui import MainMenu
from UI.load_game_ui import LoadGameWindow
from UI.new_game_ui import NewGameWindow
from saves.save_loads import SAVE_LOADS

# form_class = uic.loadUiType("./UI/ui_files/main.ui")[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("게임 화면 전환")
        self.setGeometry(100, 100, 850, 850)

        # QStackedWidget 생성
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # 페이지 추가
        self.main_menu = MainMenu(self)
        self.load_game = LoadGameWindow(self)
        self.new_game = NewGameWindow(self)
        
        # 페이지 연결하기
        self.stackedWidget.addWidget(self.main_menu)    # 메인 페이지
        self.stackedWidget.addWidget(self.load_game)    # 캐릭터 로드
        self.stackedWidget.addWidget(self.new_game)     # 새로 만들기

        # 기본 페이지 설정
        self.stackedWidget.setCurrentWidget(self.main_menu)

    def switch_to_main_menu(self):
        self.stackedWidget.setCurrentWidget(self.main_menu)

    # 로드 페이지로 가기
    def LoadGame(self):
        self.load_game.load_character()
        self.stackedWidget.setCurrentWidget(self.load_game)
    
    # 새로 만들기 페이지로 가기
    def NewGame(self):
        self.stackedWidget.setCurrentWidget(self.new_game)
        svld = SAVE_LOADS()


if __name__ == "__main__":
    # main = MAIN_GAME()
    # main.GAMESTART()
    # MainDisplay()
    
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()