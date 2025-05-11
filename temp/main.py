import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from main_menu import MainMenu
from character_load import CharacterLoad

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("게임 화면 전환")
        self.setGeometry(100, 100, 800, 600)

        # QStackedWidget 생성
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # 페이지 추가
        self.main_menu = MainMenu(self)
        self.character_load = CharacterLoad(self)
        
        self.stackedWidget.addWidget(self.main_menu)       # 페이지 0
        self.stackedWidget.addWidget(self.character_load)  # 페이지 1

        # 기본 페이지 설정
        self.stackedWidget.setCurrentWidget(self.main_menu)

    def switch_to_main_menu(self):
        self.stackedWidget.setCurrentWidget(self.main_menu)

    def switch_to_character_load(self):
        self.stackedWidget.setCurrentWidget(self.character_load)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
