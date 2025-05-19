from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QTableWidgetItem,
    QTableWidget,
    QMenu,
    QSizePolicy,
    QTabWidget
    )
from data.save_load import Player_SAVELOAD
from data.item_data import Item_SAVELOAD
from PyQt5.QtCore import Qt

from .item_view_ui import ItemViewWindow

from entity.item import Item
from entity.armor import Armor
from entity.consum import Consum

from functions.show_inventory_items import ShowInventoryItems

form_class = uic.loadUiType("./UI/ui_files/start_game_main_ui.ui")[0]

class StartMainWindow(QMainWindow, form_class, ShowInventoryItems, Armor, Item_SAVELOAD):
    def __init__(self, parent, name):
        super().__init__()
        Item_SAVELOAD.__init__(self)
        
        self.setupUi(self)
        self.load_ui = None
        
        self.parent = parent
        
        self.player_data = Player_SAVELOAD().LoadPlayer(name)
    
        self.ConnectWidget()
        self.ConnectInventoryTab()
        self.ConnectPlayerData()
        
        
    # UI 위젯 연결하기
    def ConnectWidget(self):
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
        self.attack_label = self.findChild(QLabel, 'ATTACK_LABEL')
        self.defense_label = self.findChild(QLabel, 'DEFENSE_LABEL')
        self.backpack_label = self.findChild(QLabel, 'BACKPACK_LABEL')
        self.backpacksize_label = self.findChild(QLabel, 'BACKPACKSIZE_LABEL')
        
        # 캐릭터 장비 정보 넣기
        self.helmat_label = self.findChild(QLabel, 'HELMAT_LABEL')
        self.helmat_label.setText('비어있음')
        self.neck_label = self.findChild(QLabel, 'NECK_LABEL')
        self.neck_label.setText('비어있음')
        self.armor_label = self.findChild(QLabel, 'ARMOR_LABEL')
        self.armor_label.setText('비어있음')
        self.leggings_label = self.findChild(QLabel, 'LEGGINGS_LABEL')
        self.leggings_label.setText('비어있음')
        self.shose_label = self.findChild(QLabel, 'SHOSE_LABEL')
        self.shose_label.setText('비어있음')
        self.ring1_label = self.findChild(QLabel, 'RING1_LABEL')
        self.ring1_label.setText('비어있음')
        self.ring2_label = self.findChild(QLabel, 'RING2_LABEL')
        self.ring2_label.setText('비어있음')
        self.weapon_right_label = self.findChild(QLabel, 'WEAPON_RIGHT_LABEL')
        self.weapon_right_label.setText('비어있음')
        self.weapon_left_label = self.findChild(QLabel, 'WEAPON_LEFT_LABEL')
        self.weapon_left_label.setText('비어있음')
        self.backpack_label_2 = self.findChild(QLabel, 'BACKPACK_LABEL_2')
        self.backpack_label_2.setText('비어있음')
        
        self.item_labels = {
            '투구': self.helmat_label,
            '목걸이': self.neck_label,
            '갑옷': self.armor_label,
            '바지': self.leggings_label,
            '신발': self.shose_label,
            '반지left': self.ring1_label,
            '반지right': self.ring2_label,
            '무기left': self.weapon_left_label,
            '무기right': self.weapon_right_label,
            '가방': self.backpack_label_2,
            '양손 무기': [self.weapon_left_label, self.weapon_right_label]
        }
        
    # 인벤토리 위젯 연결하기
    def ConnectInventoryTab(self):
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
        
        self.armor_inventory_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.armor_inventory_table_widget.customContextMenuRequested.connect(self.ShowRightClick)
        
        # self.consum_inventory_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.consum_inventory_table_widget.customContextMenuRequested.connect(self.ShowRightClick)
        
    
    # 플레이어 정보 연결하기
    def ConnectPlayerData(self):
        self.lv_label.setText(str(self.player_data['lv']))
        self.name_label.setText(self.player_data['name'])
        self.class_label.setText(self.player_data['class'])
        self.hp_label.setText(str(self.player_data['hp']))
        self.mp_label.setText(str(self.player_data['mp']))
        self.str_label.setText(str(self.player_data['STR']))
        self.agi_label.setText(str(self.player_data['AGI']))
        self.int_label.setText(str(self.player_data['INT']))
        self.luck_label.setText(str(self.player_data['LUCK']))
        self.money_label.setText(str(self.player_data['money']))
        self.attack_label.setText(str(self.player_data['attack_score']))
        self.defense_label.setText(str(self.player_data['defense_score']))
        self.backpack_label.setText(self.player_data['wear_armor']['가방'])
        self.backpacksize_label.setText(str(self.player_data['max_inventory_size']))
        self.player_inventory = self.player_data['inventory']
        
    
    # 캐릭터 저장하기(뒤로가기)
    def CharacterSave(self):
        self.parent.switch_to_main_menu()
    
    # 탭 변경 됨
    def on_tab_changed(self, index):
        # 전체 인벤토리
        if index == 0:
            self.AllInventory()
        elif index == 1:
            self.ArmorInventory()
        elif index == 2:
            self.ConsumInventory()
        
    # 테이블 데이터 선택 못하게 하기
    def CantEdit(self, data):
        # Name
        item = QTableWidgetItem(data)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 수정 불가능
        return item
    
    # 인벤토리 전체
    def AllInventory(self):
        inventory_items = self.SearchItemList(self.player_data['inventory'])
        self.inventory_table_widget = self.AllInventoryItems(self.inventory_table_widget, inventory_items)
    
    # 인벤토리 장비만
    def ArmorInventory(self):
        inventory_items = self.SearchItemList(self.player_data['inventory'])
        self.armor_inventory_table_widget = self.ArmorInventoryItems(self.armor_inventory_table_widget, inventory_items)
        
    # 인벤토리 소모품만
    def ConsumInventory(self):
        inventory_items = self.SearchItemList(self.player_data['inventory'])
        self.consum_inventory_table_widget = self.ConsumInventoryItems(self.consum_inventory_table_widget, inventory_items)
    
    # 인벤토리에서 우클릭 시
    def ShowRightClick(self, pos):
        # 마우스 위치에 따라 메뉴 생성
        item = self.inventory_table_widget.itemAt(pos)
        if not item:
            return  # 빈 공간을 클릭한 경우 무시
        
        # 우클릭한 아이템 좌표
        row = item.row()
        item_name = self.inventory_table_widget.item(row, 0).text()  # 클릭한 아이템의 이름 가져오기
        item_data = self.SearchItem(item_name)
        type = item_data['type']
        
        # 메뉴 생성
        menu = QMenu(self)
        wearArmor = None
        useItem = None
        if type in ['갑옷', '바지', '신발', '반지','목걸이', '투구', '한 손 무기', '양손 무기']:
            if type == '반지' or type == '한 손 무기':
                wearLeft = menu.addAction('왼손에 착용하기')
                wearRight = menu.addAction('오른손에 착용하기')
            else:
                # 장비 아이템
                wearArmor = menu.addAction("착용하기")
        elif type == '소모품':
            useItem = menu.addAction("사용하기")
            
        view_item = menu.addAction("아이템 상세보기")
        
        # 선택된 메뉴 항목 처리
        action = menu.exec_(self.inventory_table_widget.viewport().mapToGlobal(pos))
        
        if action == None: # 선택 안함
            pass
        elif action == wearArmor:   # 장비 착용
            self.player_data = self.WearArmor(item_data, item_data['type'], self.player_data, self.item_labels)
        elif action == wearLeft:
            self.player_data = self.WearArmor(item_data, item_data['type'], self.player_data, self.item_labels, hands='left')
        elif action == wearRight:
            # 아이템 제거
            self.player_data = self.WearArmor(item_data, item_data['type'], self.player_data, self.item_labels, hands='right')
        elif action == useItem:
            pass
        
        self.SyncData()
            
    def SyncData(self):
        self.ConnectPlayerData()
        self.AllInventory()
        self.ArmorInventory()
        self.ConsumInventory()