from PyQt5.QtWidgets import (
    QApplication, 
    QTableWidget, 
    QTableWidgetItem, 
    QMainWindow, 
    QMenu
)
from PyQt5.QtCore import Qt, QEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget(5, 3, self)
        self.table.setGeometry(10, 10, 400, 300)
        for i in range(5):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(f"Item {i},{j}"))

        # 우클릭 이벤트 연결
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        # 마우스 위치에 따라 메뉴 생성
        menu = QMenu(self)
        action1 = menu.addAction("Action 1")
        action2 = menu.addAction("Action 2")

        # 선택된 메뉴 항목 처리
        action = menu.exec_(self.table.viewport().mapToGlobal(pos))
        if action == action1:
            print("Action 1 selected")
        elif action == action2:
            print("Action 2 selected")

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
