import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QStackedWidget, QScrollArea, QWidget, QVBoxLayout, QApplication, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
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
        
    # 캐릭터 목록 불러오기
    def load_character(self):
        self.clear_layout(self.character_load_layout)
        
        svld = SAVE_LOADS()
        player_data = svld.data_load()
        
        # print(player_data)
        
        self.character_load_layout.setSpacing(5)  # 레이아웃 간 간격 설정
        self.character_load_layout.setContentsMargins(5, 5, 5, 5)  # 여백 설정
        
        for data in player_data.values():
            # horizontal 레이아웃 만들기
            h_layout = QHBoxLayout()
            
            # 이미지 공간 (현재는 Label로 대체)
            image_label = QLabel("이미지")
            image_label.setFixedSize(50, 50)  # 이미지 크기 설정
            image_label.setStyleSheet("border: 1px solid black;")  # 임시 스타일
            h_layout.addWidget(image_label)
            
            # 수직 레이아웃 (텍스트 정보)
            v_layout = QVBoxLayout()
            lv_label = QLabel(f"Level: {data['LV']}")
            lv_label.setFixedSize(200, 60)  # 고정 크기 설정
            name_label = QLabel(f"이름: {data['name']}")
            name_label.setFixedSize(200, 60)  # 고정 크기 설정
            class_label = QLabel(f"클래스: {data['CLASS']}")
            class_label.setFixedSize(200, 60)  # 고정 크기 설정
            
            v_layout.addWidget(lv_label)
            v_layout.addWidget(name_label)
            v_layout.addWidget(class_label)
            
            h_layout.addLayout(v_layout)
            
            v_layout = QVBoxLayout()
            hp_label = QLabel(f"HP: {data['hp']}")
            hp_label.setFixedSize(200, 60)  # 고정 크기 설정
            mp_label = QLabel(f"MP: {data['mp']}")
            mp_label.setFixedSize(200, 60)  # 고정 크기 설정
            money_label = QLabel(f"소지금액: {data['money']}")
            money_label.setFixedSize(200, 60)  # 고정 크기 설정
            
            v_layout.addWidget(hp_label)
            v_layout.addWidget(mp_label)
            v_layout.addWidget(money_label)
            
            h_layout.addLayout(v_layout)
            
            # 테두리용 컨테이너 생성
            container = QWidget()
            container.setLayout(h_layout)

            # container에만 테두리 설정
            container.setStyleSheet("QWidget { border: 1px solid black; margin: 5px; }")  
            
            
            self.character_load_layout.addWidget(container)
            
        for _ in range(5-len(player_data)):
            # horizontal 레이아웃 만들기
            h_layout = QHBoxLayout()
            label = QLabel('데이터 없음')
            
            label.setFixedSize(200, 60)  # 고정 크기 설정
            h_layout.addWidget(label)
            
            container = QWidget()
            container.setLayout(h_layout)
            container.setStyleSheet("border: 1px solid black; margin: 5px;")  # 테두리 및 여백 설정
            
            self.character_load_layout.addWidget(container)