from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QTableWidgetItem,
    QTableWidget,
    QMenu,
    QSizePolicy,
    QTabWidget,
    QPushButton, 
    QLineEdit,
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QApplication
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import json
import uuid

from data.save_load import Player_SAVELOAD
from data.item_data import Item_SAVELOAD

from .item_view_ui import ItemViewWindow
from entity.item import Item
from entity.armor import Armor
from entity.consum import Consum

from functions.show_inventory_items import ShowInventoryItems
# from ai.brain_chat import Chat
from ai.god_brain import God



# form_class = ...  # PySide6에서는 uic.loadUiType가 없으므로, .ui를 py파일로 변환해 사용하거나 QUiLoader 사용 권장

# class StartMainWindow(QMainWindow, form_class, ShowInventoryItems, Armor, Item_SAVELOAD):
class StartMainWindow(QMainWindow, ShowInventoryItems, Armor, Item_SAVELOAD, God):
    def __init__(self, parent, name):
        super().__init__()
        Item_SAVELOAD.__init__(self)
        God.__init__(self)
        
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
        
        self.session1 = self.create_session()
        
        self.player_data = Player_SAVELOAD().LoadPlayer(name)
    
        self.ConnectWidget()
        self.ConnectInventoryTab()
        self.ConnectPlayerData()
        
        
    # 위젯 연결하기
    def ConnectWidget(self):
        self.SAVE_BTN = self.ui.findChild(QPushButton, 'SAVE_BTN')
        self.SAVE_BTN.clicked.connect(self.CharacterSave)

        self.Chat_Spend_BTN = self.ui.findChild(QPushButton, 'Chat_Spend_BTN')
        self.Chat_Spend_BTN.clicked.connect(self.Chatting)
        
        self.chat_text = self.ui.findChild(QLineEdit, 'Chat_Text')
        # 엔터 키로 입력받을 수 있도록 설정
        self.chat_text.returnPressed.connect(self.Chatting)

        self.main_content = self.ui.findChild(QScrollArea, 'MAIN_CONTENT')
        self.scroll_content = self.ui.findChild(QWidget, 'scroll_content')

        # scroll_content에 레이아웃 설정
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)  # 전체 내용을 상단에 정렬
        self.scroll_layout.setSpacing(2)  # 라벨 간의 간격 축소
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)  # 레이아웃 여백 제거

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

        # 타이핑 효과 관련 변수 초기화
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.display_next_character)
        self.current_label = None
        self.full_text = ""
        self.current_index = 0
        
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
        
        
        self.add_typing_label('당신은 ')
        self.add_typing_label('이세계로 소환되었습니다.')
        
        
        
    # 인벤토리 탭 불러오기
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
        
        self.consum_inventory_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.consum_inventory_table_widget.customContextMenuRequested.connect(self.ShowRightClick)
        
    # 캐릭터 불러오기
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
        
    # 뒤로가기 & 현재 캐릭터 저장하기
    def CharacterSave(self):
        self.parent.switch_to_main_menu()
    
    # 탭에서 인벤토리 변경하기
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
    
    # 소모품 인벤토리
    def ConsumInventory(self):
        inventory_items = self.SearchItemList(self.player_data['inventory'])
        self.consum_inventory_table_widget = self.ConsumInventoryItems(self.consum_inventory_table_widget, inventory_items)
    
    # 우클릭 함수
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
        wearLeft = None
        wearRight = None
        useItem = None

        if type_ in ['반지', '한 손 무기']:
            wearLeft = menu.addAction('왼손에 착용하기')
            wearRight = menu.addAction('오른손에 착용하기')
        elif type_ in ['갑옷', '바지', '신발', '반지', '목걸이', '투구', '한 손 무기', '양손 무기']:
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
        elif action == view_item:
            self.show_item_detail(item_data)
        
        self.SyncData()
            
    # 아이템 상세보기 창 띄우기
    def show_item_detail(self, item_data):
        # 아이템 상세보기 다이얼로그 생성
        detail_dialog = ItemViewWindow(item_data, self)
        detail_dialog.exec_()    # 모달 창으로 실행

    # 데이터 리로드
    def SyncData(self):
        self.ConnectPlayerData()
        self.AllInventory()
        self.ArmorInventory()
        self.ConsumInventory()

    # 대화하기
    def Chatting(self):
        # QLineEdit에서 텍스트 가져오기
        text = self.chat_text.text().strip()
        
        from data.data_files.npc_instruction import god_npc
        system_instruction = god_npc.system_instruction
        system_instruction += json.dumps(self.player_data, ensure_ascii=False)
        system_instruction += '\n\n'
        
        with open('data/data_files/class_question.txt', 'r', encoding='utf-8') as f:
            class_question = ''.join(f.readlines())
        system_instruction += class_question
        
        if not text or self.typing_timer.isActive():
            return  # 빈 입력이거나 타이머가 이미 실행 중이면 무시
        
        # 입력 필드 초기화
        self.chat_text.clear()

        # QLineEdit로 포커스를 다시 옮김
        self.chat_text.setFocus()

        self.add_typing_label(text)
        
        # self.check_session()
        response = self.Chat(session_id=self.session1, instruction=system_instruction, input_text=text)
        self.add_typing_label(response)

    # 다음 글자를 한 글자씩 표시
    def display_next_character(self):
        if self.current_index < len(self.full_text):
            current_text = self.current_label.text()
            self.current_label.setText(current_text + self.full_text[self.current_index])
            self.current_index += 1

            # 글자 추가될 때마다 스크롤 맨 아래로 이동
            QApplication.processEvents()  # UI 이벤트 처리
            self.main_content.verticalScrollBar().setValue(self.main_content.verticalScrollBar().maximum())
        else:
            self.typing_timer.stop()  # 모든 글자를 표시했으면 타이머 정지

    # 실제 라벨 생성 및 타이핑 효과 시작 (시스템 문장 등은 이 함수 사용)
    def add_typing_label(self, text):
        self.current_label = QLabel("")
        self.current_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.current_label.setWordWrap(True)
        self.current_label.setStyleSheet("font-size: 20px; margin: 0px; padding: 0px;")
        self.current_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.current_label.setMaximumWidth(self.scroll_content.width())  # 적절한 최대 너비 지정 (스크롤 영역 폭에 맞게 조절)
        self.current_label.setMaximumHeight(self.scroll_content.height())  # 적절한 최대 너비 지정 (스크롤 영역 폭에 맞게 조절)
        
        self.scroll_layout.addWidget(self.current_label)

        self.full_text = text
        self.current_index = 0
        self.typing_timer.start(10)

        self.scroll_content.adjustSize()
        QApplication.processEvents()
        self.main_content.verticalScrollBar().setValue(self.main_content.verticalScrollBar().maximum())

    # 시스템 메시지 출력용 함수
    def system_message(self, text):
        if self.typing_timer.isActive():
            # 필요하면 타이머 종료하거나 큐에 넣는 로직 구현 가능
            return
        
    # def chat(self, session_id, instruction, input_text):
    #     if session_id not in self.sessions:
    #         print("Session not found. Please create a session first.")
    #         return None

    #     # 이전 대화 기록 누적
    #     history = self.sessions[session_id]
    #     history_text = ""
    #     for turn in history:
    #         history_text += f"User: {turn['user']}\nBot: {turn['bot']}\n"        
        
    #     # 최종 프롬프트 구성
    #     prompt = f"{instruction}\n\n{history_text}User: {input_text}\nBot:"

    #     inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    #     inputs = {k: v.to('cuda') for k, v in inputs.items()}

    #     outputs = self.model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.7)
    #     bot_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    #     # self.add_message_to_session(session_id, input_text, bot_response)

    #     self.add_typing_label(bot_response)
        
    # def check_session(self):
    #     print("Session ID:", self.session1)
    #     print("Sessions keys:", list(self.god.sessions.keys()))
        