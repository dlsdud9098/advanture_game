import os
import pickle
from tabulate import tabulate

class Item():
    def __init__(self, 
                name = None,            
                description = None,     
                required_class = None,
                required_stat = None,
                attack = None, 
                defense = None, 
                hp = None,
                mp = None,
                stat = None, 
                drop = None,
                type = None,
                using = None    # 장비에 한해서 착용 여부
                ):
        
        self.name = name
        self.description = description
        
        self.stat = stat                        # 올려주는 스텟
        self.required_class = required_class    # 착용 가능 직업
        self.required_stat = required_stat      # 착용 가능 레벨, 스텟
        
        
        self.hp = hp,
        self.mp = mp,
        self.attack_score = attack
        self.defense_score = defense
        
        self.type= type
        self.drop = drop
        self.item_data_path = 'saves/datas/itemDB.item'
        
        self.LoadItemDataBase()
        
    # 아이템 목록 불러오기
    def LoadItemDataBase(self):
        # 데이터 파일이 없거나 비어있음
        if not os.path.exists(self.item_data_path) or os.path.getsize(self.item_data_path) == 0:
            with open(self.item_data_path, 'wb') as f:
                pickle.dump({}, f)
                self.itemDB = {}
        else:
            with open(self.item_data_path, 'rb') as f:
                self.itemDB = pickle.load(f)
    
    # DB 변경사항 저장하기
    def UpdateItemDataBase(self):
        with open(self.item_data_path, 'wb') as f:
            pickle.dump(self.itemDB, f)

    # 아이템 검색하기
    def SearchItem(self, item_name):
        if item_name in self.itemDB:
            item = self.itemDB[item_name]
            return item
        else:
            print('존재하지 않는 아이템 입니다.')
            return 0
        
    # 아이템 출력하기 (1개)
    def ItemDisplayOne(self, name):
        item_data = self.SearchItem(name)
        
        if item_data == 0:
            return 
        
        # 데이터를 변환하여 출력 형태를 조정
        stat_lines = [f"{key} {value}" for key, value in item_data["stat"][0].items()]
        stat_text = "\n".join(stat_lines)
        
        required_stat_lines = [f"{key} {value}" for key, value in item_data["required_stat"][0].items()]
        required_stat_text = "\n".join(required_stat_lines)
        
        # 착용 가능 클래스를 줄바꿈으로 변환
        required_class_text = "\n".join(item_data["required_class"])
        
        # 출력용 테이블 데이터
        table_data = [
            ["아이템 이름", item_data["name"]],
            ["설명", item_data["description"]],
            ["스텟", stat_text],
            ["착용 가능 클래스", required_class_text],
            ["요구 스텟", required_stat_text],
            ["공격력", item_data["attack_score"]],
            ["방어력", item_data["defense_score"]],
            ["드랍확률", item_data.get("drop_chance", 0)],
            ["타입", item_data.get('type', 0)]
        ]
        
        
        # 출력
        print(tabulate(table_data, tablefmt="plain", colalign=("left", "left")))
    
    # 아이템 추가하기
    def AddItem(self, new_item):
        # 아이템이 기존 DB에 존재하는지 확인
        if new_item['name'] in self.itemDB:
            print('중복된 아이템입니다.')
            return
        
        # 아이템 추가하기
        self.itemDB[new_item['name']] = {}
        for key, value in new_item.items():
            self.itemDB[new_item['name']][key] = value
    
        # 추가된 사항 저장하기
        self.UpdateItemDataBase()

    # 아이템 삭제하기
    def DeleteItem(self, item_name):
        if not item_name in self.itemDB:
            print('존재하지 않는 아이템입니다.')
        
        del self.itemDB[item_name]
        
        self.UpdateItemDataBase()