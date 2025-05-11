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
        
        # scrollAreaWidgetContents 안의 레이아웃 초기화
        self.scroll_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.scroll_layout)
        
        self.SyncData()
        
    
    def SyncData(self):
        svld = SAVE_LOADS()
        datas = svld.data_load()
        
        # 기존 레이아웃 초기화
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # print(datas.values())
        
        for data in datas.values():
            # 수평 레이아웃 생성
            horizontal_layout = QHBoxLayout()
            
            # 이미지 공간 (현재는 Label로 대체)
            image_label = QLabel("이미지")
            image_label.setFixedSize(50, 50)  # 이미지 크기 설정
            image_label.setStyleSheet("border: 1px solid black;")  # 임시 스타일
            horizontal_layout.addWidget(image_label)
            
            # 수직 레이아웃 (텍스트 정보)
            vertical_layout_1 = QVBoxLayout()
            # 수직 레이아웃
            vertical_layout_2 = QVBoxLayout()
            
            # 레이아웃에 삽입할 데이터
            name_label = QLabel(f"이름: {data['name']}")
            class_label = QLabel(f"클래스: {data['CLASS']}")
            hp_label = QLabel(f"HP: {data['hp']}")
            mp_label = QLabel(f"MP: {data['mp']}")
            money_label = QLabel(f"소지금액: {data['money']}")\
            
            # 라벨 크기 조정 (최대 크기를 지정하여 늘어나지 않도록)
            for label in [name_label, hp_label, mp_label, money_label, class_label]:
                # label.setSizePolicy(QLabel.Fixed, QLabel.Fixed)
                label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            # 수직 레이아웃에 데이터 넣기
            vertical_layout_1.addWidget(name_label)
            vertical_layout_1.addWidget(class_label)
            

            # 수직 레이아웃에 데이터 넣기
            vertical_layout_2.addWidget(hp_label)
            vertical_layout_2.addWidget(mp_label)
            vertical_layout_2.addWidget(money_label)

            # 수평 레이아웃에 수직 레이아웃 추가
            horizontal_layout.addLayout(vertical_layout_1)
            horizontal_layout.addLayout(vertical_layout_2)

            # 최종적으로 위젯으로 묶어서 ScrollArea에 추가
            character_widget = QWidget()
            character_widget.setLayout(horizontal_layout)

            self.scroll_layout.addWidget(character_widget)
