import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from UI.main_menu_ui import MainMenu
from UI.load_game_ui import LoadGameWindow
from UI.new_game_ui import NewGameWindow
from UI.start_main_ui import StartMainWindow

# form_class = uic.loadUiType("./UI/ui_files/main.ui")[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1700, 850)

        # QStackedWidget 생성
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # 페이지 추가
        self.main_menu = MainMenu(self)
        self.new_game = NewGameWindow(self)
        self.load_game = LoadGameWindow(self)
        
        # 페이지 연결하기
        self.stackedWidget.addWidget(self.main_menu)    # 메인 페이지
        self.stackedWidget.addWidget(self.new_game)     # 새로 만들기
        self.stackedWidget.addWidget(self.load_game)    # 캐릭터 로드

        # 기본 페이지 설정
        self.stackedWidget.setCurrentWidget(self.main_menu)

    def switch_to_main_menu(self):
        self.stackedWidget.setCurrentWidget(self.main_menu)

    # 로드 페이지로 가기
    def LoadGame(self):
        # self.load_game.__init__()
        self.load_game.load_character()
        self.stackedWidget.setCurrentWidget(self.load_game)
    
    # 새로 만들기 페이지로 가기
    def NewGame(self):
        self.stackedWidget.setCurrentWidget(self.new_game)

    # 시작 메인 페이지로 가기
    def StartMain(self, name):
        self.start_main = StartMainWindow(self, name)
        self.stackedWidget.addWidget(self.start_main)   # 게임 메인 페이지
        self.stackedWidget.setCurrentWidget(self.start_main)
        # self.start_main.load_player_data(name)

if __name__ == "__main__":    
    os.system('clear')
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()