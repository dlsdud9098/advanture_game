from PySide6.QtWidgets import (
    QStackedWidget, 
    QVBoxLayout, 
    QLabel, 
    QWidget, 
    QPushButton, 
    QGridLayout
)

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

# from UI.ui_files.character_load_ui_pyside6 import Ui_LoadGameWindow
from data.save_load import Player_SAVELOAD

# class LoadGameWindow(QStackedWidget, Ui_LoadGameWindow):
class LoadGameWindow(QStackedWidget):
    def __init__(self, parent):
        super().__init__()
        # self.setupUi(self)
        
        # UI 파일 로드
        ui_file = QFile("./UI/ui_files/character_load_ui.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        self.setLayout(self.ui.layout())  # QDialog에 로드한 UI 배치
        
        self.player_svld = Player_SAVELOAD()
        self.parent = parent
        
        self.character_load_layout = self.ui.findChild(QVBoxLayout, "character_load_layout")
        self.BACK_BTN = self.ui.findChild(QPushButton, "BACK_BTN")
        self.BACK_BTN.clicked.connect(self.BackPage)

    def SyncData(self):
        datas = self.player_svld.data_load()

    def BackPage(self):
        self.parent.switch_to_main_menu()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())

    def refresh_content(self):
        new_data = "새로운 데이터"
        self.data_label.setText(new_data)

    def setFixedSize(self, widgetList):
        for widget in widgetList:
            widget.setFixedSize(100, 60)

    def delete_character(self, name):
        self.player_svld.DeleteData(name)
        self.load_character()

    def start_game(self, name):
        self.parent.StartMain(name)

    def create_character_widget(self, data):
        charater_layout = QGridLayout()

        image_label = QLabel("이미지")
        image_label.setFixedSize(50, 50)
        image_label.setStyleSheet("border: 1px solid black;")

        charater_layout.addWidget(image_label, 0, 0, 3, 1)

        lv_label = QLabel(f"LV: {data['lv']}")
        name_label = QLabel(f"Name: {data['name']}")
        class_label = QLabel(f"class: {data['class']}")

        charater_layout.addWidget(lv_label, 0, 1)
        charater_layout.addWidget(name_label, 1, 1)
        charater_layout.addWidget(class_label, 2, 1)

        hp_label = QLabel(f"HP: {data['hp']}")
        mp_label = QLabel(f"MP: {data['mp']}")
        money_label = QLabel(f"Money: {data['money']}")

        charater_layout.addWidget(hp_label, 0, 2)
        charater_layout.addWidget(mp_label, 1, 2)
        charater_layout.addWidget(money_label, 2, 2)

        delete_character_btn = QPushButton("Delete")
        play_character_btn = QPushButton("Play")

        delete_character_btn.clicked.connect(lambda: self.delete_character(data['name']))
        play_character_btn.clicked.connect(lambda: self.start_game(data['name']))

        delete_character_btn.setFixedSize(70, 30)
        play_character_btn.setFixedSize(70, 30)

        charater_layout.addWidget(delete_character_btn, 0, 3)
        charater_layout.addWidget(play_character_btn, 0, 4)

        widgetList = [lv_label, name_label, class_label, hp_label, mp_label, money_label]
        self.setFixedSize(widgetList=widgetList)

        grid_widget = QWidget()
        grid_widget.setLayout(charater_layout)
        grid_widget.setMaximumSize(1000, 200)

        self.character_load_layout.addWidget(grid_widget)

    def create_emtpy_character(self):
        charater_layout = QGridLayout()

        lv_label = QLabel(f"데이터 없음")
        charater_layout.addWidget(lv_label, 0, 0)

        lv_label.setFixedSize(200, 40)

        grid_widget = QWidget()
        grid_widget.setLayout(charater_layout)
        grid_widget.setMaximumSize(1000, 200)

        self.character_load_layout.addWidget(grid_widget)

    def load_character(self):
        self.clear_layout(self.character_load_layout)

        player_data = self.player_svld.LoadData()
        for data in player_data.values():
            self.create_character_widget(data)

        for _ in range(5 - len(player_data)):
            self.create_emtpy_character()
