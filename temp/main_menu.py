from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class MainMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 버튼 생성
        new_game_btn = QPushButton("새로 만들기")
        load_game_btn = QPushButton("불러오기")
        exit_game_btn = QPushButton("종료하기")

        # 버튼 클릭 이벤트 연결
        new_game_btn.clicked.connect(self.create_game)
        load_game_btn.clicked.connect(self.load_game)
        exit_game_btn.clicked.connect(self.exit_game)

        # 레이아웃에 버튼 추가
        layout.addWidget(new_game_btn)
        layout.addWidget(load_game_btn)
        layout.addWidget(exit_game_btn)
        self.setLayout(layout)

    def create_game(self):
        print("새로운 게임을 만듭니다!")  # 여기서 새로운 게임 생성 로직 추가 가능

    def load_game(self):
        # 부모(MainWindow)의 메서드를 호출하여 페이지 전환
        self.parent.switch_to_character_load()

    def exit_game(self):
        self.parent.close()
