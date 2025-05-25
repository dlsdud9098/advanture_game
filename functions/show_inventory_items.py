from PySide6.QtWidgets import (
    QTableWidgetItem,
    QSizePolicy,
    QHeaderView
)
from PySide6.QtCore import Qt

from entity.armor import Armor
from entity.consum import Consum
from data.item_data import Item_SAVELOAD

class ShowInventoryItems(Item_SAVELOAD):
    
    
    # 모든 아이템 목록 표시
    def AllInventoryItems(self, inventory_table_widget, inventory):
        inventory_table_widget.setColumnCount(5)
        inventory_table_widget.setHorizontalHeaderLabels([
            "아이템 이름", "아이템 설명", "공격력", "방어력", "타입"
        ])
        inventory_table_widget.setRowCount(len(inventory))
        inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        for row_index, item_data in enumerate(inventory):
            inventory_table_widget.setItem(row_index, 0, self.CantEdit(item_data['name']))
            inventory_table_widget.setItem(row_index, 1, self.CantEdit(item_data['description']))
            inventory_table_widget.setItem(row_index, 2, self.CantEdit(str(item_data['attack_score'])))
            inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(item_data['defense_score'])))
            inventory_table_widget.setItem(row_index, 4, self.CantEdit(item_data['type']))


        # 열 크기 조정 모드를 Interactive로 설정
        inventory_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.set_column_weights(inventory_table_widget, [2, 8, 1, 1, 2]) 

        return inventory_table_widget
    
    # 장비 아이템 목록 표시
    def ArmorInventoryItems(self, armor_inventory_table_widget, inventory):
        armor_inventory_table_widget.setColumnCount(6)
        armor_inventory_table_widget.setHorizontalHeaderLabels([
            "상태", "아이템 이름", "아이템 설명", "공격력", "방어력", "타입"
        ])
        
        armor_ = Armor()
        wear_items = armor_.OnlyLoadArmor(inventory)
        
        armor_inventory_table_widget.setRowCount(len(wear_items))
        armor_inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        for row_index, wear_item in enumerate(wear_items):
            armor_inventory_table_widget.setItem(row_index, 0, self.CantEdit('*'))
            armor_inventory_table_widget.setItem(row_index, 1, self.CantEdit(wear_item['name']))
            armor_inventory_table_widget.setItem(row_index, 2, self.CantEdit(wear_item['description']))
            armor_inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(wear_item['attack_score'])))
            armor_inventory_table_widget.setItem(row_index, 4, self.CantEdit(str(wear_item['defense_score'])))
            armor_inventory_table_widget.setItem(row_index, 5, self.CantEdit(wear_item['type']))
        
        self.set_column_weights(armor_inventory_table_widget, [1, 2, 10, 1, 1, 1])    
        
        return armor_inventory_table_widget
    
    # 소모품 아이템 목록 표시
    def ConsumInventoryItems(self, consum_inventory_table_widget, inventory):
        consum_inventory_table_widget.setColumnCount(5)
        consum_inventory_table_widget.setHorizontalHeaderLabels([
            "아이템 이름", "아이템 설명", "공격력", "방어력", "타입"
        ])

        consum = Consum()
        consum_items = consum.OnlyConsumInventory(inventory)
        
        consum_inventory_table_widget.setRowCount(len(consum_items))
        consum_inventory_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        consum_inventory_table_widget.setColumnWidth(0, 250)
        consum_inventory_table_widget.setColumnWidth(1, 300)
        consum_inventory_table_widget.setColumnWidth(2, 40)
        consum_inventory_table_widget.setColumnWidth(3, 40)
        consum_inventory_table_widget.setColumnWidth(4, 70)
        
        for row_index, wear_item in enumerate(consum_items):
            consum_inventory_table_widget.setItem(row_index, 0, self.CantEdit(wear_item['name']))
            consum_inventory_table_widget.setItem(row_index, 1, self.CantEdit(wear_item['description']))
            consum_inventory_table_widget.setItem(row_index, 2, self.CantEdit(str(wear_item['attack_score'])))
            consum_inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(wear_item['defense_score'])))
            consum_inventory_table_widget.setItem(row_index, 4, self.CantEdit(wear_item['type']))
                
        self.set_column_weights(consum_inventory_table_widget, [2, 8, 1, 1, 2]) 
        return consum_inventory_table_widget
    
    def set_column_weights(self, table_widget, weights):
        total_weight = sum(weights)

        # 가용 너비 계산
        available_width = table_widget.viewport().width()  # 테이블의 가용 영역 너비 (테두리와 스크롤바 제외)

        for index, weight in enumerate(weights):
            column_width = int((weight / total_weight) * available_width)
            table_widget.setColumnWidth(index, column_width)
            
    # 셀을 수정 불가능하게 만드는 아이템 생성 함수
    def CantEdit(self, data):
        item = QTableWidgetItem(data)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item