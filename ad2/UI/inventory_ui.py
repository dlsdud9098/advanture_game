from PyQt5.QtWidgets import (
    QMainWindow, 
    QLabel, 
    QVBoxLayout, 
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QTableView
    )
from PyQt5 import uic
from unit.item import Item
from PyQt5.QtCore import Qt


form_class = uic.loadUiType("./UI/ui_files/inventory_ui.ui")[0]

class InventoryWindow(QMainWindow, form_class):
    def __init__(self, parent=None, inventory = None):
        super().__init__(parent)  # 부모 창을 전달받아 처리
        self.setupUi(self)  # UI 초기화
        
        # 인벤토리 불러오기
        self.inventory = inventory if inventory else []
        
        # 테이블 위젯 연결하기
        self.inventory_table_widget = self.findChild(QTableView, 'InventoryTable')
        if not self.inventory_table_widget:
            raise ValueError("TableWidget 'InventoryTable' not found in UI file.")
        
        # 테이블 데이터 넣기
        self.LoadInventory()
    
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
        self.inventory_table_widget.setRowCount(len(self.inventory))
        # 테이블 열 크기 자동
        self.inventory_table_widget.resizeColumnsToContents()
        
        item_data = []
        for row_index, item_1 in enumerate(self.inventory):
            item_data = item.SearchItem(item_1)
            
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
            
            