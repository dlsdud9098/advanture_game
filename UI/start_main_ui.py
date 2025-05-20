from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QTableWidgetItem,
    QTableWidget,
    QMenu,
    QSizePolicy,
    QTabWidget,
    QPushButton, 
)
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from data.save_load import Player_SAVELOAD
from data.item_data import Item_SAVELOAD

from .item_view_ui import ItemViewWindow

from entity.item import Item
from entity.armor import Armor
from entity.consum import Consum

from functions.show_inventory_items import ShowInventoryItems


# form_class = ...  # PySide6에서는 uic.loadUiType가 없으므로, .ui를 py파일로 변환해 사용하거나 QUiLoader 사용 권장

# class StartMainWindow(QMainWindow, form_class, ShowInventoryItems, Armor, Item_SAVELOAD):
class StartMainWindow(QMainWindow, ShowInventoryItems, Armor, Item_SAVELOAD):
    def __init__(self, parent, name):
        super().__init__()
        Item_SAVELOAD.__init__(self)
        
        # self.setupUi(self)
        # .ui 파일 로드
        loader = QUiLoader()
        ui_file = QFile("./UI/ui_files/start_game_main_ui.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        self.setCentralWidget(self.ui)
        
        self.load_ui = None
        
        self.parent = parent
        
        self.player_data = Player_SAVELOAD().LoadPlayer(name)
    
        self.ConnectWidget()
        self.ConnectInventoryTab()
        self.ConnectPlayerData()
        
        
    def ConnectWidget(self):
        self.SAVE_BTN = self.ui.findChild(QPushButton, 'SAVE_BTN')
        self.SAVE_BTN.clicked.connect(self.CharacterSave)
        
        self.lv_label = self.ui.findChild(QLabel, 'LV_LABEL')
        self.name_label = self.ui.findChild(QLabel, 'NAME_LABEL')
        self.class_label = self.ui.findChild(QLabel, 'CLASS_LABEL')
        self.hp_label = self.ui.findChild(QLabel, 'HP_LABEL')
        self.mp_label = self.ui.findChild(QLabel, 'MP_LABEL')
        self.str_label = self.ui.findChild(QLabel, 'STR_LABEL')
        self.agi_label = self.ui.findChild(QLabel, 'AGI_LABEL')
        self.int_label = self.ui.findChild(QLabel, 'INT_LABEL')
        self.luck_label = self.ui.findChild(QLabel, 'LUCK_LABEL')
        self.money_label = self.ui.findChild(QLabel, 'MONEY_LABEL')
        self.attack_label = self.ui.findChild(QLabel, 'ATTACK_LABEL')
        self.defense_label = self.ui.findChild(QLabel, 'DEFENSE_LABEL')
        self.backpack_label = self.ui.findChild(QLabel, 'BACKPACK_LABEL')
        self.backpacksize_label = self.ui.findChild(QLabel, 'BACKPACKSIZE_LABEL')
        
        self.helmat_label = self.ui.findChild(QLabel, 'HELMAT_LABEL')
        self.helmat_label.setText('비어있음')
        self.neck_label = self.ui.findChild(QLabel, 'NECK_LABEL')
        self.neck_label.setText('비어있음')
        self.armor_label = self.ui.findChild(QLabel, 'ARMOR_LABEL')
        self.armor_label.setText('비어있음')
        self.leggings_label = self.ui.findChild(QLabel, 'LEGGINGS_LABEL')
        self.leggings_label.setText('비어있음')
        self.shose_label = self.ui.findChild(QLabel, 'SHOSE_LABEL')
        self.shose_label.setText('비어있음')
        self.ring1_label = self.ui.findChild(QLabel, 'RING1_LABEL')
        self.ring1_label.setText('비어있음')
        self.ring2_label = self.ui.findChild(QLabel, 'RING2_LABEL')
        self.ring2_label.setText('비어있음')
        self.weapon_right_label = self.ui.findChild(QLabel, 'WEAPON_RIGHT_LABEL')
        self.weapon_right_label.setText('비어있음')
        self.weapon_left_label = self.ui.findChild(QLabel, 'WEAPON_LEFT_LABEL')
        self.weapon_left_label.setText('비어있음')
        self.backpack_label_2 = self.ui.findChild(QLabel, 'BACKPACK_LABEL_2')
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
        
    def ConnectInventoryTab(self):
        self.inventory_tab = self.ui.findChild(QTabWidget, 'InventoryTab')
        self.inventory_tab.currentChanged.connect(self.on_tab_changed)
        
        self.inventory_table_widget = self.ui.findChild(QTableWidget, 'InventoryTable')
        self.armor_inventory_table_widget = self.ui.findChild(QTableWidget, 'ArmorTable')
        self.consum_inventory_table_widget = self.ui.findChild(QTableWidget, 'ConsumableTable')
        
        self.inventory_tab.setCurrentIndex(0)
        
        self.inventory_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.inventory_table_widget.customContextMenuRequested.connect(self.ShowRightClick)
        
        self.armor_inventory_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.armor_inventory_table_widget.customContextMenuRequested.connect(self.ShowRightClick)
        
        # self.consum_inventory_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.consum_inventory_table_widget.customContextMenuRequested.connect(self.ShowRightClick)
        
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
        
    def CharacterSave(self):
        self.parent.switch_to_main_menu()
    
    def on_tab_changed(self, index):
        if index == 0:
            self.AllInventory()
        elif index == 1:
            self.ArmorInventory()
        elif index == 2:
            self.ConsumInventory()
    
    # 수정 불가
    def CantEdit(self, data):
        item = QTableWidgetItem(data)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item
    
    # 인벤토리 전체 표시
    def AllInventory(self):
        inventory_items = self.SearchItemList(self.player_data['inventory'])
        self.inventory_table_widget = self.AllInventoryItems(self.inventory_table_widget, inventory_items)
    
    # 장비만 표시
    def ArmorInventory(self):
        inventory_items = self.SearchItemList(self.player_data['inventory'])
        self.armor_inventory_table_widget = self.ArmorInventoryItems(self.armor_inventory_table_widget, inventory_items)
    
    
    def ConsumInventory(self):
        inventory_items = self.SearchItemList(self.player_data['inventory'])
        self.consum_inventory_table_widget = self.ConsumInventoryItems(self.consum_inventory_table_widget, inventory_items)
    
    def ShowRightClick(self, pos):
        item = self.inventory_table_widget.itemAt(pos)
        if not item:
            return
        
        row = item.row()
        item_name = self.inventory_table_widget.item(row, 0).text()
        item_data = self.SearchItem(item_name)
        type_ = item_data['type']
        
        menu = QMenu(self)
        wearArmor = None
        useItem = None
        if type_ in ['갑옷', '바지', '신발', '반지', '목걸이', '투구', '한 손 무기', '양손 무기']:
            if type_ == '반지' or type_ == '한 손 무기':
                wearLeft = menu.addAction('왼손에 착용하기')
                wearRight = menu.addAction('오른손에 착용하기')
            else:
                wearArmor = menu.addAction("착용하기")
        elif type_ == '소모품':
            useItem = menu.addAction("사용하기")
            
        view_item = menu.addAction("아이템 상세보기")
        
        action = menu.exec(self.inventory_table_widget.viewport().mapToGlobal(pos))
        
        if action is None:
            pass
        elif action == wearArmor:
            self.player_data = self.WearArmor(item_data, item_data['type'], self.player_data, self.item_labels)
        elif action == wearLeft:
            self.player_data = self.WearArmor(item_data, item_data['type'], self.player_data, self.item_labels, hands='left')
        elif action == wearRight:
            self.player_data = self.WearArmor(item_data, item_data['type'], self.player_data, self.item_labels, hands='right')
        elif action == useItem:
            pass
        
        self.SyncData()
            
    def SyncData(self):
        self.ConnectPlayerData()
        self.AllInventory()
        self.ArmorInventory()
        self.ConsumInventory()
