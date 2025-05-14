from PyQt5 import uic
from PyQt5.QtWidgets import (
    QStackedWidget, 
    QVBoxLayout, 
    QLabel, 
    QWidget, 
    QPushButton,
    QGridLayout
    )
import os

from saves.save_loads import SAVE_LOADS

load_window = uic.loadUiType("./UI/ui_files/character_load_ui.ui")[0]

class LoadGameWindow(QStackedWidget,load_window):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        
        self.SyncData()
        self.parent = parent
        
        self.character_load_layout = self.findChild(QVBoxLayout, "character_load_layout")
        
        # 뒤로가기 버튼 연결하기
        self.BACK_BTN.clicked.connect(self.BackPage)
        
        # self.load_character()
        
    def SyncData(self):
        svld = SAVE_LOADS()
        datas = svld.data_load()
        
    # 뒤로 가기(메인 페이지)
    def BackPage(self):
        self.parent.switch_to_main_menu()
    
    # 리프레시
    def clear_layout(self, layout):
        """레이아웃의 모든 위젯 및 하위 레이아웃 제거"""
        while layout.count():
            item = layout.takeAt(0)  # 레이아웃에서 아이템 가져오기
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # 위젯 삭제
            elif item.layout() is not None:
                self.clear_layout(item.layout())  # 하위 레이아웃에 대해 재귀 호출
    
    # 현재 창 새로고침
    def refresh_content(self):
        # 데이터 새로고침 로직
        new_data = "새로운 데이터"  # 새로 가져온 데이터로 갱신
        self.data_label.setText(new_data)
    
    # 텍스트 라벨 크기 조절
    def setFixedSize(self, widgetList):
        for widget in widgetList:
            widget.setFixedSize(100,60)
            
    def delete_character(self, name):
        svld = SAVE_LOADS()  # 데이터 관리 객체
        svld.delete_player(name)
        self.load_character()  # 데이터 갱신 및 UI 업데이트
    
    # 캐릭터 데이터 넣기
    def create_character_widget(self, data):
        charater_layout = QGridLayout()

        # 이미지 공간 (현재는 Label로 대체)
        image_label = QLabel("이미지")
        image_label.setFixedSize(50, 50)  # 이미지 크기 설정
        image_label.setStyleSheet("border: 1px solid black;")  # 임시 스타일

        # 이미지 라벨을 0번째 열에서 세 줄을 차지하도록 추가
        charater_layout.addWidget(image_label, 0, 0, 3, 1)  # rowSpan 3, colSpan 1로 설정

        # 데이터 라벨
        lv_label = QLabel(f"LV: {data['LV']}")
        name_label = QLabel(f"Name: {data['name']}")
        class_label = QLabel(f"class: {data['CLASS']}")

        # 라벨을 1번째 열에 추가
        charater_layout.addWidget(lv_label, 0, 1)
        charater_layout.addWidget(name_label, 1, 1)
        charater_layout.addWidget(class_label, 2, 1)

        # HP, MP, Money 라벨 추가
        hp_label = QLabel(f"HP: {data['hp']}")
        mp_label = QLabel(f"MP: {data['mp']}")
        money_label = QLabel(f"Money: {data['money']}")

        # 라벨 추가
        charater_layout.addWidget(hp_label, 0, 2)
        charater_layout.addWidget(mp_label, 1, 2)
        charater_layout.addWidget(money_label, 2, 2)
        
        # 삭제, 실행 버튼 만들기
        delete_character_btn = QPushButton("Delete")
        play_character_btn = QPushButton("Play")
        
        delete_character_btn.clicked.connect(lambda: self.delete_character(data['name']))
        
        delete_character_btn.setFixedSize(70, 30)
        play_character_btn.setFixedSize(70, 30)
        
        charater_layout.addWidget(delete_character_btn, 0, 3)
        charater_layout.addWidget(play_character_btn, 0, 4)
        
        widgetList = [lv_label, name_label, class_label, hp_label, mp_label, money_label]
        self.setFixedSize(widgetList=widgetList)

        # QGridLayout을 감싸는 QWidget 생성
        grid_widget = QWidget()
        grid_widget.setLayout(charater_layout)
        grid_widget.setMaximumSize(1000, 200)

        # 레이아웃 추가
        self.character_load_layout.addWidget(grid_widget)
    
    # 빈 데이터 공간 넣기
    def create_emtpy_character(self):
        charater_layout = QGridLayout()

        # 데이터 라벨
        lv_label = QLabel(f"데이터 없음")

        # 라벨을 1번째 열에 추가
        charater_layout.addWidget(lv_label, 0, 0)

        lv_label.setFixedSize(200, 40)

        # QGridLayout을 감싸는 QWidget 생성
        grid_widget = QWidget()
        grid_widget.setLayout(charater_layout)
        grid_widget.setMaximumSize(1000, 200)

        # QWidget에 테두리 스타일 추가
        # grid_widget.setStyleSheet("border: 1px solid black;")  # 테두리 추가

        # 레이아웃 추가
        self.character_load_layout.addWidget(grid_widget)
    
    # 캐릭터 목록 불러오기
    def load_character(self):
        self.clear_layout(self.character_load_layout)
        
        svld = SAVE_LOADS()
        player_data = svld.data_load()

        for data in player_data.values():
            self.create_character_widget(data)
        
        for _ in range(5-len(player_data)):
            self.create_emtpy_character()