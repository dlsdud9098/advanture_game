from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QTableWidget,
    QSizePolicy,
    QPushButton,
    QDialog,
    QHeaderView
    )
from data.item_data import Item_SAVELOAD
from PyQt5.QtCore import Qt

# from unit.item import Item
from entity.item import Item

form_class = uic.loadUiType("./UI/ui_files/item_view_ui.ui")[0]

class ItemViewWindow(QDialog, form_class):
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.setup_table(item_data)
    def setup_table(self, item_data):
        # 테이블 위젯 참조 (Designer에서 설정한 이름 사용)
        table_widget = self.findChild(QTableWidget, "itemtableWidget")
        
        # 데이터 설정
        table_widget.setRowCount(4)  # 행 개수 설정
        table_widget.setColumnCount(2)  # 열 개수 설정
        table_widget.setHorizontalHeaderLabels(["속성", "값"])
        
        # 데이터 설정
        details = [
            ("아이템 이름", item_data['name']),
            ("아이템 타입", item_data['type']),
            ("아이템 요구 스탯", ""),  # 요구 스탯 구분선
            ("STR", item_data['required_stat'].get('STR', 0)),
            ("AGI", item_data['required_stat'].get('AGI', 0)),
            ("INT", item_data['required_stat'].get('INT', 0)),
            ("LUCK", item_data['required_stat'].get('LUCK', 0)),
        ]
        
        # 테이블 행 및 열 설정
        table_widget.setRowCount(len(details))
        table_widget.setColumnCount(2)
        table_widget.setHorizontalHeaderLabels(["속성", "값"])
        table_widget.verticalHeader().setVisible(False)  # 행 번호 숨기기

        # 데이터 추가
        for row, (attribute, value) in enumerate(details):
            table_widget.setItem(row, 0, self.CantEdit(attribute))
            table_widget.setItem(row, 1, self.CantEdit(str(value)))

        # 열 크기 조정
        table_widget.resizeColumnsToContents()
        # table_widget.setColumnWidth(0, 150)  # 첫 번째 열 너비 고정
        
        # 열 비율 설정
        self.set_column_weights(table_widget, [1,2])  # 첫 번째 열: 1, 두 번째 열: 2
        
        # 테이블 데이터 선택 못하게 하기
    def CantEdit(self, data):
        # Name
        item = QTableWidgetItem(data)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 수정 불가능
        return item
    
    def set_column_weights(self, table_widget, weights):
        """
        테이블의 열 너비를 비율(weight)에 따라 설정합니다.

        :param table_widget: QTableWidget 인스턴스
        :param weights: 각 열의 비율을 리스트로 전달 (예: [1, 2, 1])
        """
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # 전체 너비를 비율로 설정
        total_weight = sum(weights)

        # 각 열의 비율에 따라 크기 설정
        for i, weight in enumerate(weights):
            table_widget.setColumnWidth(i, int(weight / total_weight * table_widget.width()))