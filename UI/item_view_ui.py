from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from data.item_data import Item_SAVELOAD
from entity.item import Item

# from UI.ui_files.item_view_ui_pyside6 import Ui_Form

# class ItemViewWindow(QDialog, Ui_Form):
class ItemViewWindow(QDialog):
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        
        # UI 파일 로드
        ui_file = QFile("./UI/ui_files/item_view_ui.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        self.setLayout(self.ui.layout())  # QDialog에 로드한 UI 배치
        
        self.setup_table(item_data)
    
    def setup_table(self, item_data):
        table_widget = self.ui.findChild(QTableWidget, "itemtableWidget")
        
        details = [
            ("아이템 이름", item_data['name']),
            ("아이템 타입", item_data['type']),
            ("아이템 요구 스탯", ""),  # 요구 스탯 구분선
            ("STR", item_data['required_stat'].get('STR', 0)),
            ("AGI", item_data['required_stat'].get('AGI', 0)),
            ("INT", item_data['required_stat'].get('INT', 0)),
            ("LUCK", item_data['required_stat'].get('LUCK', 0)),
        ]
        
        table_widget.setRowCount(len(details))
        table_widget.setColumnCount(2)
        table_widget.setHorizontalHeaderLabels(["속성", "값"])
        table_widget.verticalHeader().setVisible(False)
        
        for row, (attribute, value) in enumerate(details):
            table_widget.setItem(row, 0, self.CantEdit(attribute))
            table_widget.setItem(row, 1, self.CantEdit(str(value)))
        
        table_widget.resizeColumnsToContents()
        self.set_column_weights(table_widget, [1, 2])
    
    def CantEdit(self, data):
        item = QTableWidgetItem(data)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item
    
    def set_column_weights(self, table_widget, weights):
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        total_weight = sum(weights)
        for i, weight in enumerate(weights):
            table_widget.setColumnWidth(i, int(weight / total_weight * table_widget.width()))
