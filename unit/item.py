import pandas as pd
from tabulate import tabulate
import os
import json

class Item():
    def __init__(self, name = None, description = None, \
                required_class = None, required_stat = None, \
                attack = None, defense = None, stat = None):
        
        self.name = name
        self.description = description
        
        self.stat = stat                        # 올려주는 스텟
        self.required_class = required_class    # 착용 가능 직업
        self.required_stat = required_stat      # 착용 가능 레벨, 스텟
        
        self.attack_score = attack
        self.defense_score = defense
        
    
    def UseItem(self):
        
        return self.stat, self.attack_score, self.defense_score
    
    # 전체 아이템 목록 불러오기
    def LoadItemDataBase(self):
        save_file_path = 'saves/datas/item_data.json'
        # 데이터 비어있거나 파일이 없음
        if not os.path.exists(save_file_path) or os.path.getsize(save_file_path) == 0:
            with open('saves/datas/item_data.json', 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)
            
            ItemDataBase = []
        else:
            with open('saves/datas/item_data.json', 'r', encoding='utf-8') as f:
                ItemDataBase = json.load(f)
            
        return ItemDataBase

    # 현재 아이템 이름을 전체 아이템 목록과 대조해서 정보 가져오기
    def LoadItem(self, item_name):
        ItemDataBase = self.LoadItemDataBase()
        
        # 딕셔너리로 변환
        item_dict = {item["name"]: item for item in ItemDataBase}
        
        # 빠른 검색
        if item_name in item_dict:
            item = item_dict[item_name]
            
            ItemData = {
                "name": item['name'],
                "description": item['description'],
                "stat": item['stat'],
                "required_class": item['required_class'],
                "required_stat": item['required_stat'],
                "attack_score": item['attack_score'],
                "defense_score": item['defense_score']
            }
            
        else:
            print(f"Item '{item_name}' not found.")
        
            
        return ItemData
    
    def ItemDisplay(self):
        ItemDataBase = self.LoadItemDataBase()
        pass
    
    # 아이템 출력하기 (1개)
    def ItemDisplayOne(self, name):
        item = self.LoadItem(name)
        item_df = pd.DataFrame(index=range(16), columns=range(1))
        
        data = {
            "아이템 이름": item['name'],
            "설명": item['description'],
            "스텟": item['stat'],
            "착용 가능 클래스": item['required_class'],
            "요구 스텟": item['required_stat'],
            "공격력": item['attack_score'],
            "방어력": item['defense_score'],
        }
        
        # for idx, (key, value) in enumerate(data.items()):
        #     row = 1
        #     item_df.iloc[idx, 0] = key
        #     item_df.iloc[idx, 0] = value
        #     row += 1
        
        # item_df.fillna('', inplace=True)
        # print(tabulate(item_df, tablefmt='plain', showindex=False, headers=[]), '\n')
        
        for key, value in data.items():
            print(f"{key}\t{value}")
    
    # 아이템 추가하기
    def AddItem(self, data):
        ItemData = self.LoadItemDataBase()
        
        data = {
            "name": data['name'],
            "description": data['description'],
            
            "stat": data['stat'],
            "required_class": data['required_class'],
            "required_stat": data['required_stat'],
            
            "attack_score": data['attack_score'],
            "defense_score": data['defense_score']
        }
        
        ItemData.append(data)
        with open('saves/datas/item_data.json', 'w', encoding='utf-8') as f:
            json.dump(ItemData, f, indent=4)
