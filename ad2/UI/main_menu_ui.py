import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox



form_class = uic.loadUiType("./UI/ui_files/main.ui")[0]

class MainMenu(QMainWindow, form_class):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.load_ui = None
        
        self.parent = parent

        # 버튼 이벤트 연결
        self.NEWGAME_BTN.clicked.connect(self.create_game)
        self.LOADGAME_BTN.clicked.connect(self.load_game)
        self.EXITGAME_BTN.clicked.connect(self.exit_game)

    def create_game(self):
        # QMessageBox.information(self, "새로 만들기", "새로운 파일을 만듭니다!")
        self.parent.NewGame()

    def load_game(self):
        # 불러오기 페이지로 이동
        # 부모(MainWindow)의 메서드를 호출하여 페이지 전환
        # self.parent.load_character()
        self.parent.LoadGame()

    def exit_game(self):
        reply = QMessageBox.question(
            self,
            "종료 확인",
            "종료하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QApplication.quit()
            
    def syncdata(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()