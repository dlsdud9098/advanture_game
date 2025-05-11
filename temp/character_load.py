from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton

class CharacterLoad(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 캐릭터 리스트
        self.character_list = QListWidget()
        characters = ["Warrior", "Mage", "Archer"]
        self.character_list.addItems(characters)

        # 뒤로 가기 버튼
        back_button = QPushButton("뒤로 가기")
        back_button.clicked.connect(self.go_back)

        # 레이아웃에 위젯 추가
        layout.addWidget(self.character_list)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def go_back(self):
        # 부모(MainWindow)의 메서드를 호출하여 메인 메뉴로 전환
        self.parent.switch_to_main_menu()
