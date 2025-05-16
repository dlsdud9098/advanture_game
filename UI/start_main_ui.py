from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QTableWidgetItem,
    QTableWidget,
    QMenu,
    QSizePolicy,
    QTabWidget,
    QPushButton
    )
from saves.save_loads import SAVE_LOADS
from PyQt5.QtCore import Qt

from unit.item import Item
from unit.player.armor import Armor
from unit.player.consum import Consum

form_class = uic.loadUiType("./UI/ui_files/start_game_main_ui.ui")[0]

class StartMainWindow(QMainWindow, form_class):
    def __init__(self, parent, name):
        super().__init__()
        self.setupUi(self)
        self.load_ui = None
        
        self.parent = parent
        self.name = name
        
        svld = SAVE_LOADS()
        self.player_data = svld.player_load(name)
        
        print(self.player_data)
        
        # 버튼 연결        
        self.SAVE_BTN.clicked.connect(self.CharacterSave)
        # self.Chat_Spend_BTN.clicked.connect(self.SpendChat)
        
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
        # print(self.player_data)
        self.player_inventory = self.player_data['inventory']
        
        # 인벤토리 탭 연결하기
        # 탭 변경 시그널 연결
        self.inventory_tab = self.findChild(QTabWidget, 'InventoryTab')
        self.inventory_tab.currentChanged.connect(self.on_tab_changed)

        # 테이블 위젯 연결하기
        self.inventory_table_widget = self.findChild(QTableWidget, 'InventoryTable')
        self.armor_inventory_table_widget = self.findChild(QTableWidget, 'ArmorTable')
        self.consum_inventory_table_widget = self.findChild(QTableWidget, 'ConsumableTable')
        
        # 초기화: 첫 번째 탭 활성화 및 데이터 설정
        self.inventory_tab.setCurrentIndex(0)
        
        # 우클릭 이벤트 연결
        self.inventory_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.inventory_table_widget.customContextMenuRequested.connect(self.ShowRightClick)
        
        
        self.load_player_data()
        
    def on_tab_changed(self, index):
        """
        탭 변경됨
        """    
        
        # 전체 인벤토리
        if index == 0:
            self.LoadInventory('all')
        elif index == 1:
            self.LoadInventory('armor')
        elif index == 2:
            self.LoadInventory('consum')
            
    # 플레이어 정보에 대한 내용을 새로고침(업데이트) 합니다.
    def refresh_widget(self):
        # self.load_player_data()
        self.LoadInventory('all')
        # self.LoadArmor()
        pass
    
    def CharacterSave(self):
        self.parent.switch_to_main_menu()
        pass
    
    # 메인 창에서 캐릭터 데이터 입력하기
    def load_player_data(self):
        
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
        
        # self.player_inventory = self.player_data['inventory']
        
        # 테이블 데이터 넣기
        # self.LoadAllInventory()
        self.LoadArmor()
        self.LoadAllInventory()
    
    # 테이블 데이터 선택 못하게 하기
    def CantEdit(self, data):
        # Name
        item = QTableWidgetItem(data)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 수정 불가능
        return item
    
    # 소모품 아이템 테이블
    def LoadConsumInventory(self):
        self.consum_inventory_table_widget.setColumnCount(5)  # 필요한 열 수
        self.consum_inventory_table_widget.setHorizontalHeaderLabels([
            "아이템 이름", "아이템 설명", "공격력", "방어력", "타입"
        ])
        
        # 현재 인벤토리에서 장비 아이템만 가져오기        
        armor_ = Consum()
        wear_items = armor_.ConsumItem(self.player_inventory)
        
        # 행 수 설정
        self.consum_inventory_table_widget.setRowCount(len(wear_items))
        self.consum_inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 열의 크기 조절
        self.consum_inventory_table_widget.setColumnWidth(0, 250)  # 첫 번째 열의 너비를 150px로 설정
        self.consum_inventory_table_widget.setColumnWidth(1, 300)   # 두 번째 열의 너비를 50px로 설정
        self.consum_inventory_table_widget.setColumnWidth(2, 40)  # 네 번째 열의 너비를 100px로 설정
        self.consum_inventory_table_widget.setColumnWidth(3, 40)  # 네 번째 열의 너비를 100px로 설정
        self.consum_inventory_table_widget.setColumnWidth(4, 70)  # 다섯 번째 열의 너비를 100px로 설정
        
        for row_index, wear_item in enumerate(wear_items):
            # Name
                self.consum_inventory_table_widget.setItem(row_index, 0, self.CantEdit(wear_item['name']))
                # Description
                self.consum_inventory_table_widget.setItem(row_index, 1, self.CantEdit(wear_item['description']))
                # Attack
                self.consum_inventory_table_widget.setItem(row_index, 2, self.CantEdit(str(wear_item['attack'])))
                # Defense
                self.consum_inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(wear_item['defense'])))
                # Type
                self.consum_inventory_table_widget.setItem(row_index, 4, self.CantEdit(wear_item['type']))
    
    # 전체 아이템 데이터 만들기(테이블)
    def LoadAllInventory(self):
        item = Item()
        
        self.inventory_table_widget.setColumnCount(5)  # 필요한 열 수
        self.inventory_table_widget.setHorizontalHeaderLabels([
            "아이템 이름", "아이템 설명", "공격력", "방어력", "타입"
        ])
        
        # 행 수 설정
        self.inventory_table_widget.setRowCount(len(self.player_inventory))
        self.inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 열의 크기 조절
        self.inventory_table_widget.setColumnWidth(0, 250)  # 첫 번째 열의 너비를 150px로 설정
        self.inventory_table_widget.setColumnWidth(1, 300)   # 두 번째 열의 너비를 50px로 설정
        self.inventory_table_widget.setColumnWidth(2, 40)  # 네 번째 열의 너비를 100px로 설정
        self.inventory_table_widget.setColumnWidth(3, 40)  # 네 번째 열의 너비를 100px로 설정
        self.inventory_table_widget.setColumnWidth(4, 70)  # 다섯 번째 열의 너비를 100px로 설정
        
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
        self.ring1_label.setText(player_armor['반지']['왼손'])
        self.ring2_label.setText(player_armor['반지']['오른손'])
        self.weapon_right_label.setText(player_armor['무기'])
        self.weapon_left_label.setText(player_armor['무기'])
        self.backpack_label_2.setText(player_armor['가방'])
        
    def ShowRightClick(self, pos):
        # 마우스 위치에 따라 메뉴 생성
        item = self.inventory_table_widget.itemAt(pos)
        if not item:
            return  # 빈 공간을 클릭한 경우 무시
        
        # 우클릭한 아이템 좌표
        row = item.row()
        column = item.column()
        item_name = self.inventory_table_widget.item(row, 0).text()  # 클릭한 아이템의 이름 가져오기
        
        item = Item()
        item_data = item.SearchItem(item_name)
        type = item_data['type']
        
        # 메뉴 생성
        menu = QMenu(self)
        wearArmor = None
        useItem = None
        if type in ['갑옷', '바지', '신발', '반지','목걸이', '투구', '무기']:
            if type == '반지':
                wearRing1 = menu.addAction('왼손에 착용하기')
                wearRing2 = menu.addAction('오른손에 착용하기')
            else:
                # 장비 아이템
                wearArmor = menu.addAction("착용하기")
        elif type == '소모품':
            useItem = menu.addAction("사용하기")
            
        view_item = menu.addAction("아이템 상세보기")

        # 선택된 메뉴 항목 처리
        action = menu.exec_(self.inventory_table_widget.viewport().mapToGlobal(pos))
        print(action)
        if action == None: # 선택 안함
            pass
        elif action == wearArmor:   # 장비 착용
            # 아이템 제거
            self.player_inventory.remove(item_data['name'])
            self.WearArmor(item_data, item_data['type'])
        elif action == useItem:
            print("UseItem selected")
        elif action == view_item:       # 아이템 상세보기
            print('Action 2 selected')
        elif action == wearRing1:       # 왼손에 반지 착용
            # 아이템 제거
            self.player_inventory.remove(item_data['name'])
            self.WearArmor(item_data, item_data['type'], 'left')
        elif action == wearRing2:       # 오른손에 반지 착용
            # 아이템 제거
            self.player_inventory.remove(item_data['name'])
            self.WearArmor(item_data, item_data['type'], 'right')
            
        self.refresh_widget()
    
    # 장비 착용
    def WearArmor(self, item_data, item_type, hands = None):
        item_name = item_data['name']
        armor_func = {
            '투구': [
                lambda: self.helmat_label.setText(item_name),    #  armor 상태에 넣기
                lambda: self.AddStatArmor(item_data),
                lambda: self.set_wear_armor(item_type, item_name) # wear_armor 업데이트
            ],
            '목걸이': [
                lambda: self.neck_label.setText(item_name),    #  armor 상태에 넣기
                lambda: self.AddStatArmor(item_data),
                lambda: self.set_wear_armor(item_type, item_name) # wear_armor 업데이트
            ],
            '갑옷': [
                lambda: self.armor_label.setText(item_name),    #  armor 상태에 넣기
                lambda: self.AddStatArmor(item_data),
                lambda: self.set_wear_armor(item_type, item_name) # wear_armor 업데이트
            ],
            '바지': [
                lambda: self.leggings_label.setText(item_name),    #  armor 상태에 넣기
                lambda: self.AddStatArmor(item_data),
                lambda: self.set_wear_armor(item_type, item_name) # wear_armor 업데이트
            ],
            '신발': [
                lambda: self.shose_label.setText(item_name),    #  armor 상태에 넣기
                lambda: self.AddStatArmor(item_data),
                lambda: self.set_wear_armor(item_type, item_name) # wear_armor 업데이트
            ],
            '반지': [
                lambda: self.wear_ring(item_name),
                lambda: self.AddStatArmor(item_data),
                lambda: self.set_wear_armor(item_type, item_name, hands) # wear_armor 업데이트
            ],
            '무기': [
                lambda: self.weapon_right_label.setText(item_name),    #  armor 상태에 넣기
                lambda: self.AddStatArmor(item_data),
                lambda: self.set_wear_armor(item_type, item_name) # wear_armor 업데이트
            ],
            
        }
        
        if item_type in armor_func:
            for func in armor_func[item_type]:
                func()  # 리스트의 모든 함수 실행
        else:
            print(f"Unsupported armor type: {item_type}")
        self.load_player_data()
        
    # 헬퍼 함수 추가
    def set_wear_armor(self, armor_type, item_name, hands = None):
        if armor_type == '반지':
            if hands == 'left':
                self.player_data['wear_armor']['ring'][0]
        else:
            self.player_data['wear_armor'][armor_type] = item_name
    
    # 반지 착용
    def wear_ring(self, item_name):
        if self.ring1_label.text() == '비어있음':  # ring1_label이 비어있으면
            self.ring1_label.setText(item_name)
        else:
            self.ring2_label.setText(item_name)
    
    # 착용한 장비에 대한 스텟 변화
    def AddStatArmor(self, item_data):
        print(item_data['required_stat'].get('STR', 0))
        self.player_data['STR'] += item_data['required_stat'].get('STR', 0)
        self.player_data['AGI'] += item_data['required_stat'].get('AGI', 0)
        self.player_data['INT'] += item_data['required_stat'].get('INT', 0)
        self.player_data['LUCK'] += item_data['required_stat'].get('LUCK', 0)
        self.player_data['attack_score'] += item_data.get('attack', 0)
        self.player_data['defense_score'] += item_data.get('defense', 0)
        self.player_data['hp'] += item_data.get('hp', 0)
        self.player_data['mp'] += item_data.get('mp', 0)
        
    def UpdatePlayerData(self):
        pass
    
    # 인벤토리에서 장비 탭
    def LoadInventoryArmor(self):        
        self.armor_inventory_table_widget.setColumnCount(5)  # 필요한 열 수
        self.armor_inventory_table_widget.setHorizontalHeaderLabels([
            "상태", "아이템 이름", "아이템 설명", "공격력", "방어력", "타입"
        ])
        
        # 현재 인벤토리에서 장비 아이템만 가져오기        
        armor_ = Armor()
        wear_items = armor_.CanWearItem(self.player_inventory)
        
        # 행 수 설정
        self.armor_inventory_table_widget.setRowCount(len(wear_items))
        self.armor_inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 열의 크기 조절
        self.armor_inventory_table_widget.setColumnWidth(0, 10)  # 첫 번째 열의 너비를 150px로 설정
        self.armor_inventory_table_widget.setColumnWidth(1, 250)  # 첫 번째 열의 너비를 150px로 설정
        self.armor_inventory_table_widget.setColumnWidth(2, 300)   # 두 번째 열의 너비를 50px로 설정
        self.armor_inventory_table_widget.setColumnWidth(3, 40)  # 네 번째 열의 너비를 100px로 설정
        self.armor_inventory_table_widget.setColumnWidth(4, 40)  # 네 번째 열의 너비를 100px로 설정
        self.armor_inventory_table_widget.setColumnWidth(5, 70)  # 다섯 번째 열의 너비를 100px로 설정
        
        for row_index, wear_item in enumerate(wear_items):
            
            # Name
            self.armor_inventory_table_widget.setItem(row_index, 0, self.CantEdit('*'))
            # Name
            self.armor_inventory_table_widget.setItem(row_index, 1, self.CantEdit(wear_item['name']))
            # Description
            self.armor_inventory_table_widget.setItem(row_index, 2, self.CantEdit(wear_item['description']))
            # Attack
            self.armor_inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(wear_item['attack'])))
            # Defense
            self.armor_inventory_table_widget.setItem(row_index, 4, self.CantEdit(str(wear_item['defense'])))
            # Type
            self.armor_inventory_table_widget.setItem(row_index, 5, self.CantEdit(wear_item['type']))
    
    def InsertItem(self, row_index, item_data):
        self.inventory_table_widget.setItem(row_index, 0, self.CantEdit("*"))
        self.inventory_table_widget.setItem(row_index, 1, self.CantEdit(item_data['name']))
        # Description
        self.inventory_table_widget.setItem(row_index, 2, self.CantEdit(item_data['description']))
        # Attack
        self.inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(item_data['attack'])))
        # Defense
        self.inventory_table_widget.setItem(row_index, 4, self.CantEdit(str(item_data['defense'])))
        # Type
        self.inventory_table_widget.setItem(row_index, 5, self.CantEdit(item_data['type']))
    
    def LoadInventory(self, type):
        if type == 'all':
            self.LoadAllInventory()
        elif type == 'armor':
            self.LoadInventoryArmor()
        elif type == 'consum':
            self.LoadConsumInventory()