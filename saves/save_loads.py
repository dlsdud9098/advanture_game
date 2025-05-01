import json
import os

from unit.player import Player

import pandas as pd
from tabulate import tabulate

class SAVE_LOADS:
    def __init__(self):
        try:
            with open('saves/datas/saves.json', 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
    # 데이터 저장하기
    def data_save(self, player_datas):
        with open('saves/datas/saves.json', 'w', encoding='utf-8') as f:
            json.dump(player_datas, f, indent=4)
        
    # 데이터 가져오기
    def data_load(self):
        with open('saves/datas/saves.json', 'r', encoding='utf-8') as f:
            player_datas = json.load(f)
            
        print(player_datas)
        print()
        print(os.getcwd())
        print()

        # 데이터가 없으면
        if not bool(player_datas):
            player_datas = []
            print('데이터가 비어있습니다.')

        return player_datas

    # 새로운 플레이어 데이터 추가하기
    def data_update(self, data):
        player_datas = self.data_load()
        
        # 데이터 비어있음
        if not bool(player_datas):
            player_datas.append(data)
        else:
            if player_datas['name'] == data['name']:
                print('중복된 이름입니다.')
                return 1
        player_datas.append(data)
        self.data_save(player_datas)
    
    # 플레이어 로드하기
    def player_load(self, data):
        player = Player()
        player.set_status(
            {
            "mp" : data['mp'],
            "hp" : data['hp'],
            "attack_score" : data['attack_score'],
            "defense_score" : data['defense_score'],
            "skills" : data['skills'],
            "inventory" : data['inventory'],
            "use_items" : data['use_items'],
            "unit_type" : data['unit_type'],
            "money" : data['money'],
            "STR" : data['STR'],
            "AGI" : data['AGI'],
            "INT" : data['INT'],
            "LUCK" : data['LUCK'],
            "AVOID" : data['AVOID'],
            "experience" : data['experience'],
            "skillpoint" : data['skillpoint'],
            "LV" : data['LV'],
            "honor" : data['honor'],
            "CLASS" : data['CLASS'],
            "name" : data['name']
            }
        )