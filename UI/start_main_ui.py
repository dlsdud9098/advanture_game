from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QTableWidgetItem,
    QTableWidget,
    QMenu,
    QSizePolicy
    )
from saves.save_loads import SAVE_LOADS
from UI.inventory_ui import InventoryWindow
from PyQt5.QtCore import Qt
from unit.item import Item

form_class = uic.loadUiType("./UI/ui_files/start_game_main_ui.ui")[0]

class StartMainWindow(QMainWindow, form_class):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.load_ui = None
        
        self.parent = parent
        self.player_data = None
        
        # 캐릭터 스셋 정보 넣기
        self.lv_label = self.findChild(QLabel, 'LV_LABEL')
        self.name_label = self.findChild(QLabel, 'NAME_LABEL')
        self.class_label = self.findChild(QLabel, 'CLASS_LABEL')
        self.hp_label = self.findChild(QLabel, 'HP_LABEL')
        self.mp_label = self.findChild(QLabel, 'MP_LABEL')
        self.str_label = self.findChild(QLabel, 'STR_LABEL')
        self.agi_label = self.findChild(QLabel, 'AGI_LABEL')
        self.int_label = self.findChild(QLabel, 'INT_LABEL')
        self.luck_label = self.findChild(QLabel, 'LUCK_LABEL')
        self.money_label = self.findChild(QLabel, 'MONEY_LABEL')
        self.avoid_label = self.findChild(QLabel, 'AVOID_LABEL')
        self.attack_label = self.findChild(QLabel, 'ATTACK_LABEL')
        self.defense_label = self.findChild(QLabel, 'DEFENSE_LABEL')
        self.backpack_label = self.findChild(QLabel, 'BACKPACK_LABEL')
        
        # 캐릭터 장비 정보 넣기
        self.helmat_label = self.findChild(QLabel, 'HELMAT_LABEL')
        self.neck_label = self.findChild(QLabel, 'NECK_LABEL')
        self.armor_label = self.findChild(QLabel, 'ARMOR_LABEL')
        self.leggings_label = self.findChild(QLabel, 'LEGGINGS_LABEL')
        self.shose_label = self.findChild(QLabel, 'SHOSE_LABEL')
        self.ring1_label = self.findChild(QLabel, 'RING1_LABEL')
        self.ring2_label = self.findChild(QLabel, 'RING2_LABEL')
        self.weapon_right_label = self.findChild(QLabel, 'WEAPON_RIGHT_LABEL')
        self.weapon_left_label = self.findChild(QLabel, 'WEAPON_LEFT_LABEL')
        self.backpack_label_2 = self.findChild(QLabel, 'BACKPACK_LABEL_2')

        self.name = None
        self.player_inventory = None
        
        # 인벤토리 탭 연결하기
        # 탭 변경 시그널 연결
        self.InventoryTab.currentChanged.connect(self.on_tab_changed)

        # 초기화: 첫 번째 탭 활성화 및 데이터 설정
        self.InventoryTab.setCurrentIndex(0)
        
        # 테이블 위젯 연결하기
        self.inventory_table_widget = self.findChild(QTableWidget, 'InventoryTable')
        self.armor_inventory_table_widget = self.findChild(QTableWidget, 'ArmorTable')
        
        # 우클릭 이벤트 연결
        self.inventory_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.inventory_table_widget.customContextMenuRequested.connect(self.WearArmor)
        
    def on_tab_changed(self, index):
        """
        탭 변경됨
        """    
        
        # 전체 인벤토리
        if index == 0:
            self.LoadInventory()
        elif index == 1:
            self.LoadInventoryArmor()
    
    # 플레이어 정보에 대한 내용을 새로고침(업데이트) 합니다.
    def refresh_widget(self):
        self.load_player_data(self.name)
        self.LoadInventory()
        self.LoadArmor()
        pass
    
    def ViewInventory(self):
        if not self.load_ui:  # 창이 이미 열려 있는지 확인
            self.load_ui = InventoryWindow(self, self.player_inventory)  # 부모로 현재 창을 전달
        self.load_ui.show()  # 새 창 표시
    
    # 메인 창에서 캐릭터 데이터 입력하기
    def load_player_data(self, name):
        self.name = name   
        
        svld = SAVE_LOADS()
        self.player_data = svld.player_load(name)
        
        # print(self.player_data)
        
        self.lv_label.setText(str(self.player_data['LV']))
        self.name_label.setText(str(self.player_data['name']))
        self.class_label.setText(str(self.player_data['CLASS']))
        self.hp_label.setText(str(self.player_data['hp']))
        self.mp_label.setText(str(self.player_data['mp']))
        self.str_label.setText(str(self.player_data['STR']))
        self.agi_label.setText(str(self.player_data['AGI']))
        self.int_label.setText(str(self.player_data['INT']))
        self.luck_label.setText(str(self.player_data['LUCK']))
        self.money_label.setText(str(self.player_data['money']))
        self.avoid_label.setText(str(self.player_data['AVOID']))
        self.attack_label.setText(str(self.player_data['attack_score']))
        self.defense_label.setText(str(self.player_data['defense_score']))
        self.backpack_label.setText(self.player_data['wear_armor']['가방'])
        # self.backpack_label.setText(str(player_data))
        
        self.player_inventory = self.player_data['inventory']
        
        # 테이블 데이터 넣기
        # self.LoadInventory()
        self.LoadArmor()
    
    # 테이블 데이터 선택 못하게 하기
    def CantEdit(self, data):
        # Name
        item = QTableWidgetItem(data)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 수정 불가능
        return item
    
    # 아이템 데이터 만들기(테이블)
    def LoadInventory(self):
        item = Item()
        
        self.inventory_table_widget.setColumnCount(5)  # 필요한 열 수
        self.inventory_table_widget.setHorizontalHeaderLabels([
            "아이템 이름", "아이템 설명", "공격력", "방어력", "부위"
        ])
        
        # 행 수 설정
        self.inventory_table_widget.setRowCount(len(self.player_inventory))
        self.inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 열의 크기 조절
        self.inventory_table_widget.setColumnWidth(0, 250)  # 첫 번째 열의 너비를 150px로 설정
        self.inventory_table_widget.setColumnWidth(1, 300)   # 두 번째 열의 너비를 50px로 설정
        self.inventory_table_widget.setColumnWidth(2, 40)  # 네 번째 열의 너비를 100px로 설정
        self.inventory_table_widget.setColumnWidth(3, 40)  # 네 번째 열의 너비를 100px로 설정
        self.inventory_table_widget.setColumnWidth(4, 40)  # 다섯 번째 열의 너비를 100px로 설정
        
        item_data = []
        for row_index, item_1 in enumerate(self.player_inventory):
            item_data = item.SearchItem(item_1)
            
            # 아이템 넣기
            if item_data:
                # Name
                self.inventory_table_widget.setItem(row_index, 0, self.CantEdit(item_data['name']))
                # Description
                self.inventory_table_widget.setItem(row_index, 1, self.CantEdit(item_data['description']))
                # Attack
                self.inventory_table_widget.setItem(row_index, 2, self.CantEdit(str(item_data['attack'])))
                # Defense
                self.inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(item_data['defense'])))
                # Type
                self.inventory_table_widget.setItem(row_index, 4, self.CantEdit(item_data['type']))
    
    def LoadArmor(self):
        # 플레이어 착용 장비 가져오기
        player_armor = self.player_data['wear_armor']
        
        # 현재 착용하고 있는 데이터 넣기
        
        self.helmat_label.setText(player_armor['투구'])
        self.neck_label.setText(player_armor['목걸이'])
        self.armor_label.setText(player_armor['갑옷'])
        self.leggings_label.setText(player_armor['바지'])
        self.shose_label.setText(player_armor['신발'])
        ring1, ring2 = player_armor['반지']
        self.ring1_label.setText(ring1)
        self.ring2_label.setText(ring2)
        self.weapon_right_label.setText(player_armor['무기'])
        self.weapon_left_label.setText(player_armor['무기'])
        self.backpack_label_2.setText(player_armor['가방'])
        
    def WearArmor(self, pos):
        # 마우스 위치에 따라 메뉴 생성
        menu = QMenu(self)
        action1 = menu.addAction("착용하기")
        action2 = menu.addAction("아이템 상세보기")

        # 선택된 메뉴 항목 처리
        action = menu.exec_(self.inventory_table_widget.viewport().mapToGlobal(pos))
        
        if action == action1:
            print("Action 1 selected")
        elif action == action2:
            print("Action 2 selected")
    
    def LoadInventoryArmor(self):
        item = Item()
        
        self.armor_inventory_table_widget.setColumnCount(5)  # 필요한 열 수
        self.armor_inventory_table_widget.setHorizontalHeaderLabels([
            "아이템 이름", "아이템 설명", "공격력", "방어력", "부위"
        ])
        
        # 현재 인벤토리에서 장비 아이템만 가져오기
        print(self.player_inventory)