import sys
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QMessageBox,
    QPushButton, 
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MainMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # .ui 파일 로드
        loader = QUiLoader()
        ui_file = QFile("./UI/ui_files/main.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        # self.setLayout(self.ui.layout())  # QDialog에 로드한 UI 배치
        self.setCentralWidget(self.ui)

        # UI 위젯을 멤버로 바로 할당 (예: NEWGAME_BTN)
        self.NEWGAME_BTN = self.ui.findChild(QMainWindow, "NEWGAME_BTN") or self.ui.findChild(type(self.ui), "NEWGAME_BTN")
        self.LOADGAME_BTN = self.ui.findChild(QMainWindow, "LOADGAME_BTN") or self.ui.findChild(type(self.ui), "LOADGAME_BTN")
        self.EXITGAME_BTN = self.ui.findChild(QMainWindow, "EXITGAME_BTN") or self.ui.findChild(type(self.ui), "EXITGAME_BTN")

        # 만약 버튼이 None이면, 아래처럼 찾기
        self.NEWGAME_BTN = self.ui.findChild(type(self.ui), "NEWGAME_BTN")
        self.LOADGAME_BTN = self.ui.findChild(type(self.ui), "LOADGAME_BTN")
        self.EXITGAME_BTN = self.ui.findChild(type(self.ui), "EXITGAME_BTN")
        
        self.NEWGAME_BTN = self.ui.findChild(QPushButton, "NEWGAME_BTN")
        self.LOADGAME_BTN = self.ui.findChild(QPushButton, "LOADGAME_BTN")
        self.EXITGAME_BTN = self.ui.findChild(QPushButton, "EXITGAME_BTN")

        # 버튼 이벤트 연결
        self.NEWGAME_BTN.clicked.connect(self.create_game)
        self.LOADGAME_BTN.clicked.connect(self.load_game)
        self.EXITGAME_BTN.clicked.connect(self.exit_game)

        self.setCentralWidget(self.ui)

    def create_game(self):
        self.parent.NewGame()

    def load_game(self):
        self.parent.LoadGame()

    def exit_game(self):
        reply = QMessageBox.question(
            self,
            "종료 확인",
            "종료하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def syncdata(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 부모를 None으로 했으니 실제 쓰는 MainWindow에 맞게 조정하세요
    window = MainMenu()
    window.show()
    sys.exit(app.exec())
