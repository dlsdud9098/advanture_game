import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QStackedWidget, QScrollArea, QWidget, QVBoxLayout, QApplication, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

from saves.save_loads import SAVE_LOADS

load_window = uic.loadUiType("./UI/ui_files/character_load_ui.ui")[0]

class LoadGameWindow(QStackedWidget,load_window):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        
        # ScrollArea 설정
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # 콘텐츠 크기에 맞게 스크롤 조정
        self.scroll_area_widget = QWidget()  # ScrollArea 내부에 들어갈 위젯
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)  # 내부 레이아웃
        self.scroll_area.setWidget(self.scroll_area_widget)  # ScrollArea에 위젯 추가
        
        self.SyncData()
        
    
    def SyncData(self):
        svld = SAVE_LOADS()
        datas = svld.data_load()
        
        # print(datas)
        
        # 이미지 추가
        # image_label = QLabel()
        # pixmap = QPixmap(char["image"]) if char["image"] else QPixmap(100, 100)
        # pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # image_label.setPixmap(pixmap)
        # character_widget = QWidget()
        # character_data_layout = QVBoxLayout(character_widget)

        # for data in datas.values():
            
        #     # 이미지 추가
        #     image_label = QLabel()
        #     pixmap = QPixmap(80, 80)  # 기본 크기의 빈 이미지를 생성
        #     pixmap.fill(Qt.gray)  # 기본 이미지는 회색
        #     image_label.setPixmap(pixmap)
        #     image_label.setFixedSize(80, 80)  # 이미지 크기 설정
        #     image_label.setStyleSheet("border: 1px solid black;")  # 테두리 스타일
            
        #     # 텍스트 레이아웃 (수직 레이아웃)
        #     text_layout = QVBoxLayout()
            
        #     # 데이터 레이블 추가
        #     name_label = QLabel(f"이름: {data['name']}")
        #     class_label = QLabel(f"클래스: {data['CLASS']}")
        #     hp_label = QLabel(f"HP: {data['hp']}   MP: {data['mp']}")
        #     money_label = QLabel(f"소지금액: {data['money']}")

        #     # 폰트 크기 및 스타일 지정 (옵션)
        #     for label in [name_label, class_label, hp_label, money_label]:
        #         label.setStyleSheet("font-size: 12pt; margin: 2px;")

        #     # 텍스트 레이아웃 (수직 레이아웃)
        #     text_layout = QVBoxLayout()
            
        #     # 수직 레이아웃에 레이블 추가
        #     text_layout.addWidget(name_label)
        #     text_layout.addWidget(class_label)
        #     text_layout.addWidget(hp_label)
        #     text_layout.addWidget(money_label)
            
        #     # 수평 레이아웃에 이미지와 텍스트 추가
        #     character_data_layout.addWidget(image_label)
        #     character_data_layout.addLayout(text_layout)
            
            
            
            
            
            
            
            
            
        # # ScrollArea 레이아웃에 추가
        # self.scroll_area_layout.addWidget(character_widget)