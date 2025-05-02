import pandas as pd
from tabulate import tabulate
import os
import json

class Item():
    def __init__(self, name = None, description = None, \
                required_class = None, required_stat = None, \
                attack = None, defense = None, stat = None, drop = None):
        
        self.name = name
        self.description = description
        
        self.stat = stat                        # 올려주는 스텟
        self.required_class = required_class    # 착용 가능 직업
        self.required_stat = required_stat      # 착용 가능 레벨, 스텟
        
        self.attack_score = attack
        self.defense_score = defense
        
        self.drop = drop
        
    
    def UseItem(self):
        
        return self.stat, self.attack_score, self.defense_score
    
    # 전체 아이템 목록 불러오기
    def LoadItemDataBase(self):
        save_file_path = 'saves/datas/item_data.json'
        # 데이터 비어있거나 파일이 없음
        if not os.path.exists(save_file_path) or os.path.getsize(save_file_path) == 0:
            with open(save_file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
            
            ItemDataBase = {}
        else:
            with open('saves/datas/item_data.json', 'r', encoding='utf-8') as f:
                ItemDataBase = json.load(f)
            
        return ItemDataBase

    # 현재 아이템 이름을 전체 아이템 목록과 대조해서 정보 가져오기
    def LoadItem(self, item_name):
        ItemDataBase = self.LoadItemDataBase()
        
        # 빠른 검색
        if item_name in ItemDataBase:
            item = ItemDataBase[item_name]
            
            ItemData = {}
            for key, value in item.items():
                ItemData[key] = value
            
        else:
            print(f"Item '{item_name}' not found.")
            return 0
        
        return ItemData
    
    def ItemDisplay(self):
        ItemDataBase = self.LoadItemDataBase()
        pass
    
    # 아이템 출력하기 (1개)
    def ItemDisplayOne(self, name):
        item_data = self.LoadItem(name)
        
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
            ["부위", item_data.get('type', 0)]
        ]
        
        
        # 출력
        print(tabulate(table_data, tablefmt="plain", colalign=("left", "left")))
    
    # 아이템 추가하기
    def AddItem(self, data):
        ItemData = self.LoadItemDataBase()
        
        # 중복 확인
        if data['name'] in ItemData:
            print(f"Item '{data['name']}' already exists.")
            return  # 중복된 아이템은 추가하지 않음
        
        # 새로운 데이터
        ItemData[data['name']] = {}
        for key, value in data.items():
            ItemData[data['name']][key] = value
        
        with open('saves/datas/item_data.json', 'w', encoding='utf-8') as f:
            json.dump(ItemData, f, indent=4)
