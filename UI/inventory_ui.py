from PySide6.QtWidgets import (
    QMainWindow, 
    QLabel, 
    QVBoxLayout, 
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QTableView
)
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from unit.item import Item

# from UI.ui_files.inventory_ui_pyside6 import Ui_Form

# class InventoryWindow(QMainWindow, Ui_Form):
class InventoryWindow(QMainWindow):
    def __init__(self, parent=None, inventory=None):
        super().__init__(parent)
        
        # UI 로드 (pyside6-uic로 변환한 파일이 없을 때 사용법)
        ui_file = QFile("./UI/ui_files/inventory_ui.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        self.setCentralWidget(self.ui)
        
        # 인벤토리 불러오기
        self.inventory = inventory if inventory else []
        
        # 테이블 위젯 연결하기
        self.inventory_table_widget = self.ui.findChild(QTableView, 'InventoryTable')
        if not self.inventory_table_widget:
            raise ValueError("TableWidget 'InventoryTable' not found in UI file.")
        
        # 테이블 데이터 넣기
        self.LoadInventory()
    
    def CantEdit(self, data):
        item = QTableWidgetItem(data)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 수정 불가능
        return item
    
    def LoadInventory(self):
        item = Item()
        
        self.inventory_table_widget.setColumnCount(5)  # 필요한 열 수
        self.inventory_table_widget.setHorizontalHeaderLabels([
            "아이템 이름", "아이템 설명", "공격력", "방어력", "부위"
        ])
        # 행 수 설정
        self.inventory_table_widget.setRowCount(len(self.inventory))
        # 테이블 열 크기 자동 조정
        self.inventory_table_widget.resizeColumnsToContents()
        
        for row_index, item_1 in enumerate(self.inventory):
            item_data = item.SearchItem(item_1)
            if item_data:
                self.inventory_table_widget.setItem(row_index, 0, self.CantEdit(item_data['name']))
                self.inventory_table_widget.setItem(row_index, 1, self.CantEdit(item_data['description']))
                self.inventory_table_widget.setItem(row_index, 2, self.CantEdit(str(item_data['attack'])))
                self.inventory_table_widget.setItem(row_index, 3, self.CantEdit(str(item_data['defense'])))
                self.inventory_table_widget.setItem(row_index, 4, self.CantEdit(item_data['type']))
