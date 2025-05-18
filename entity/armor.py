from data.item_data import Item_SAVELOAD
import pandas as pd

class Armor(Item_SAVELOAD):
    def __init__(self):
        super().__init__()
        self.armor_tags = ['무기', '갑옷', '바지', '신발', '목걸이', '반지', '투구', '한 손 무기', '양 손 무기']

    # 장비 아이템만 추출
    def OnlyLoadArmor(self, inventory):
        results = []
        for items in inventory:
            if items['type'] in self.armor_tags:
                results.append(items)
        print(results)
        return results
    
    # 장비 장착하기 함수
    def WearArmor(self, item_data, item_type, player_data, item_labels, hands=''):
        self.player_data = player_data
        
        # print(item_data)
        
        self.AddStatArmor(item_data)
        self.SetWearArmor(item_type, item_data, hands)
        item_labels[item_type+hands].setText(item_data['name'])
        
        return self.player_data
        
    # 장비 장착 해제하기 함수
    def UnWearArmor(self, item_data, item_type, player_data, item_labels, hands=''):
        self.player_data = player_data
        
        
    # 장비 스텟 더하기(장착)
    def AddStatArmor(self, item_data):
        self.player_data['STR'] += item_data['up_stat'].get('STR', 0)
        self.player_data['AGI'] += item_data['up_stat'].get('AGI', 0)
        self.player_data['INT'] += item_data['up_stat'].get('INT', 0)
        self.player_data['LUCK'] += item_data['up_stat'].get('LUCK', 0)
        self.player_data['attack_score'] += item_data.get('attack', 0)
        self.player_data['defense_score'] += item_data.get('defense', 0)
        self.player_data['hp'] += item_data.get('hp', 0)
        self.player_data['mp'] += item_data.get('mp', 0)

    # 장비 착용하기
    def SetWearArmor(self, item_type, item, hands = None):
        # item = self.SearchItem(item_data['name'])
        # print(item, item_type)
        if item_type == '반지' or item_type == '한 손 무기':
            hands_key = '왼손' if hands == 'left' else '오른손'
            item_type = '무기' if item_type == '한 손 무기' else '반지'
            if self.player_data['wear_armor'][item_type][hands_key] == '비어있음':
                self.player_data['inventory'].remove(item['name'])
            else:
                self.player_data['inventory'].append(self.player_data['wear_armor'][item_type][hands_key])
                
            self.player_data['wear_armor'][item_type][hands_key] = item['name']
                
                
        else:
            if self.player_data['wear_armor'].get(item_type) == '비어있음':                
                # print(f"before: {self.player_data['inventory']}")
                self.player_data['inventory'].remove(item['name'])
                # print(f"after: {self.player_data['inventory']}")
            else:
                self.player_data['inventory'].append(self.player_data['wear_armor'][item_type])
            self.player_data['wear_armor'][item_type] = item['name']
            # print(self.player_data)
            
    # 장비 스텟 빼기(장착 해제)
    def SubStatArmor(self, item_data):
        self.player_data['STR'] -= item_data['up_stat'].get('STR', 0),
        self.player_data['AGI'] -= item_data['up_stat'].get('AGI', 0),
        self.player_data['INT'] -= item_data['up_stat'].get('INT', 0),
        self.player_data['LUCK'] -= item_data['up_stat'].get('LUCK', 0),
        self.player_data['attack_score'] -= item_data.get('attack', 0),
        self.player_data['defense_score'] -= item_data.get('defense', 0),
        self.player_data['hp'] -= item_data.get('hp', 0),
        self.player_data['mp'] -= item_data.get('mp', 0)
    
    # 장비 장착 해제
    def SetUnWearArmor(self, item_type, item_data, hands = None):
        if item_type == '반지' or item_type == '한 손 무기':
            hands_key = '왼손' if hands == 'left' else '오른손'
            self.player_data['wear_armor'][item_type][hands_key] = '비어있음'
        else:
            self.player_data['wear_armor']['item_type'] = '비어있음'
        