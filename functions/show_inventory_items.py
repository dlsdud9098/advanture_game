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
from PyQt5.QtCore import Qt

from entity.armor import Armor
from entity.consum import Consum

class ShowInventoryItems:
    
    # 모든 아이템 목록
    def AllInventoryItems(self, inventory_table_widget, inventory):
        inventory_table_widget.setColumnCount(5)  # 필요한 열 수
        inventory_table_widget.setHorizontalHeaderLabels([
            "아이템 이름", "아이템 설명", "공격력", "방어력", "타입"
        ])
        
        # 행 수 설정
        inventory_table_widget.setRowCount(len(inventory))
        inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 열의 크기 조절
        inventory_table_widget.setColumnWidth(0, 250)  # 첫 번째 열의 너비를 150px로 설정
        inventory_table_widget.setColumnWidth(1, 300)   # 두 번째 열의 너비를 50px로 설정
        inventory_table_widget.setColumnWidth(2, 40)  # 네 번째 열의 너비를 100px로 설정
        inventory_table_widget.setColumnWidth(3, 40)  # 네 번째 열의 너비를 100px로 설정
        inventory_table_widget.setColumnWidth(4, 70)  # 다섯 번째 열의 너비를 100px로 설정
        
        for row_index, item_data in enumerate(inventory):
            # Name
            inventory_table_widget.setItem(row_index, 0, self.CantEdit(item_data['name']))
            # Description
            inventory_table_widget.setItem(row_index, 1, self.CantEdit(item_data['description']))
            # Attack
            inventory_table_widget.setItem(row_index, 2, self.CantEdit(str(item_data['attack'])))
            # Defense
            inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(item_data['defense'])))
            # Type
            inventory_table_widget.setItem(row_index, 4, self.CantEdit(item_data['type']))
            
        
        
        return inventory_table_widget
    
    # 장비 아이템 목록
    def ArmorInventoryItems(self, armor_inventory_table_widget, inventory):
        armor_inventory_table_widget.setColumnCount(6)  # 필요한 열 수
        armor_inventory_table_widget.setHorizontalHeaderLabels([
            "상태", "아이템 이름", "아이템 설명", "공격력", "방어력", "타입"
        ])
        
        # 현재 인벤토리에서 장비 아이템만 가져오기        
        armor_ = Armor()
        wear_items = armor_.OnlyLoadArmor(inventory)
        
        # 행 수 설정
        armor_inventory_table_widget.setRowCount(len(wear_items))
        armor_inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        for row_index, wear_item in enumerate(wear_items):
            # Name
            armor_inventory_table_widget.setItem(row_index, 0, self.CantEdit('*'))
            # Name
            armor_inventory_table_widget.setItem(row_index, 1, self.CantEdit(wear_item['name']))
            # Description
            armor_inventory_table_widget.setItem(row_index, 2, self.CantEdit(wear_item['description']))
            # Attack
            armor_inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(wear_item['attack'])))
            # Defense
            armor_inventory_table_widget.setItem(row_index, 4, self.CantEdit(str(wear_item['defense'])))
            # Type
            armor_inventory_table_widget.setItem(row_index, 5, self.CantEdit(wear_item['type']))
        
        self.set_column_weights(armor_inventory_table_widget, [1, 2, 10, 1, 1, 1])    
        
        return armor_inventory_table_widget
    
    # 소모품 아이템 목록
    def ConsumInventoryItems(self, consum_inventory_table_widget, inventory):
        consum_inventory_table_widget.setColumnCount(5)  # 필요한 열 수
        consum_inventory_table_widget.setHorizontalHeaderLabels([
            "아이템 이름", "아이템 설명", "공격력", "방어력", "타입"
        ])

        cnosum = Consum()
        consum_items = cnosum.OnlyConsumInventory(inventory)
        print(consum_items)
        
        # 행 수 설정
        consum_inventory_table_widget.setRowCount(len(consum_items))
        consum_inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 열의 크기 조절
        consum_inventory_table_widget.setColumnWidth(0, 250)  # 첫 번째 열의 너비를 150px로 설정
        consum_inventory_table_widget.setColumnWidth(1, 300)   # 두 번째 열의 너비를 50px로 설정
        consum_inventory_table_widget.setColumnWidth(2, 40)  # 네 번째 열의 너비를 100px로 설정
        consum_inventory_table_widget.setColumnWidth(3, 40)  # 네 번째 열의 너비를 100px로 설정
        consum_inventory_table_widget.setColumnWidth(4, 70)  # 다섯 번째 열의 너비를 100px로 설정
        
        for row_index, wear_item in enumerate(consum_items):
            # Name
                consum_inventory_table_widget.setItem(row_index, 0, self.CantEdit(wear_item['name']))
                # Description
                consum_inventory_table_widget.setItem(row_index, 1, self.CantEdit(wear_item['description']))
                # Attack
                consum_inventory_table_widget.setItem(row_index, 2, self.CantEdit(str(wear_item['attack'])))
                # Defense
                consum_inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(wear_item['defense'])))
                # Type
                consum_inventory_table_widget.setItem(row_index, 4, self.CantEdit(wear_item['type']))
                
        return consum_inventory_table_widget
    
    # 열 크기
    def set_column_weights(self, table_widget, weights):
        temp = 0
        # 각 열의 비율에 따라 크기 설정
        for i, weight in enumerate(weights):
            a = int(table_widget.width()*(weight/sum(weights)))-3
            temp += a
            table_widget.setColumnWidth(i, a)
            
    # 테이블 데이터 선택 못하게 하기
    def CantEdit(self, data):
        # Name
        item = QTableWidgetItem(data)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 수정 불가능
        return item