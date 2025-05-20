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
        
        return results
    
    # 장비 장착하기 함수
    def WearArmor(self, item_data, item_type, player_data, item_labels, hands=''):
        self.player_data = player_data
        self.labels = item_labels

        if item_data['type'] in ['양손 무기', '한 손 무기']:
            self.UnWearWeapon(hands, item_data)
        elif item_data['type'] == '반지':
            self.UnWearRing(hands)
        else:
            self.UnWearArmor(self, item_data)
        
        self.AddStatArmor(item_data)
        self.UnWearArmor(item_data=item_data, hands=hands)
        
        if item_type == '반지':
            self.WearArmorRing(item_data, hands)
        elif item_type in ['양손 무기', '한 손 무기']:
            self.WearArmorWeapon(item_data, hands)
        else:
            self.SetWearArmor(item_data)
            
        return self.player_data

    # 장비(무기, 반지 제외) 장착 해제
    def UnWearArmor(self, item_data):
        self.player_data['wear_armor'][item_data['type']] = '비어있음'
        self.player_data['inventory'].append(item_data['type'])
        self.labels[item_data['type']].setText('비어있음')

    # 무기 장착 해제
    def UnWearWeapon(self, hands, item_data):
        hands_key = '왼손' if hands == 'left' else '오른손'
        left_weapon = self.player_data['wear_armor']['무기']['왼손']
        right_weapon = self.player_data['wear_armor']['무기']['오른손']

        """
        내가 장착하고자 하는 무기가 양손 무기다. => 현재 장착하고 있는 무기가 양손 무기일 때 => 양손의 무기를 모두 장착 해제한다.
                                                현재 장착하고 있는 무기가 한 손 무기일 때 => 양손의 무기를 모두 장착 해제한다.
        내가 장착하고자 하는 무기가 한 손 무기다. => 현재 장착하고 있는 무기가 양손 무기일 때 => 양손의 무기를 모두 장착 해제한다.
                                                현재 장착하고 있는 무기가 한 손 무기일 때 => 양손의 무기를 모두 장착 해제한다.
        """
        # 내가 장착하고자 하는 무기가 양손 무기일 때
        if item_data['type'] == '양손 무기':

            # 현재 장착하고 있는 무기가 양손 무기일 때
            if left_weapon == right_weapon:
                self.player_data['inventory'].append(left_weapon)
            # 현재 창착하고 있는 무기가 한 손 무기일 때
            else:
                self.player_data['inventory'].append(left_weapon)
                self.player_data['inventory'].append(right_weapon)
            
            self.player_data['wear_armor']['무기']['왼손'] = '비어있음'
            self.player_data['wear_armor']['무기']['오른손'] = '비어있음'
            self.labels['무기left'].setText('비어있음')
            self.labels['무기right'].setText('비어있음')
        
        # 내가 장착하고자 하는 무기가 한 손 무기일 때
        else:
            if left_weapon == right_weapon:
                print(item_data)
                self.player_data['inventory'].append(left_weapon)

                self.player_data['wear_armor']['무기']['왼손'] = '비어있음'
                self.player_data['wear_armor']['무기']['오른손'] = '비어있음'
                self.labels['무기left'].setText('비어있음')
                self.labels['무기right'].setText('비어있음')
            else:
                current_weapon = self.player_data['wear_armor']['무기'][hands_key]
                self.player_data['wear_armor']['무기'][hands_key] = '비어있음'
                self.player_data['inventory'].append(current_weapon)

                self.labels['무기'+hands].setText('비어있음')
        
    # 반지 장착 해제
    def UnWearRing(self, hands):
        pass

    # 장비 장착 해제하기 함수
    def UnWearArmor(self, item_data, hands = ''):
        if item_data['type'] in ['반지', '한 손 무기']:
            item_type = '무기' if item_data['type'] == '한 손 무기' else '반지'
            
            hands_key = '왼손' if hands == 'left' else '오른손'
            
            # 현재 착용하고 있는 무기가 양손 무기일 때
            if item_type == '무기':
                left_item = self.player_data['wear_armor'][item_type]['왼손']
                right_item = self.player_data['wear_armor'][item_type]['오른손']
                
                print(left_item, right_item)
                if left_item == right_item:
                    self.player_data['wear_armor'][item_type]['왼손'] = '비어있음'
                    self.player_data['wear_armor'][item_type]['오른손'] = '비어있음'
                    
                    self.labels[item_type+'left'].setText('비어있음')
                    self.labels[item_type+'right'].setText('비어있음')
                    return
                
            # 양손 무기가 아닌 한 손 무기, 반지일 때
            self.player_data['wear_armor'][item_type][hands_key] = '비어있음'
            self.player_data['inventory'].append(item_data['name'])    
            self.labels[item_type+hands].setText('비어있음')
        elif item_data['type'] == '양손 무기':
            item_type = '무기'
            for hand in ['왼손', '오른손']:
                self.player_data['wear_armor'][item_type][hand] = '비어있음'
                
            self.labels[item_type+'left'].setText('비어있음')
            self.labels[item_type+'right'].setText('비어있음')
        else:
            if self.player_data['wear_armor'][item_data['type']] != '비어있음':
                self.player_data['wear_armor'][item_data['type']] = '비어있음'
                self.player_data['inventory'].append(item_data['name'])
            self.labels[item_data['type']].setText('비어있음')
        
    # 장비 스텟 더하기(장착)
    def AddStatArmor(self, item_data):
        for stat in ['STR', 'AGI', 'INT', 'LUCK']:
            self.player_data[stat] += item_data.get('up_stat', {}).get(stat, 0)
            
        for stat in ['attack_score', 'defense_score', 'hp', 'mp']:
            self.player_data[stat] += item_data.get(stat, 0)

    # 반지 착용하기
    def WearArmorRing(self, item, hands):
        hands_key = '왼손' if hands == 'left' else '오른손'
        
        self.player_data['wear_armor'][item['type']][hands_key] = item['name']
        self.player_data['inventory'].remove(item['name'])
        self.labels[item['type']+hands].setText(item['name'])
        
    def WearArmorWeapon(self, item, hands = ''):
        if item['type'] == '양손 무기':
            item_type = '무기'
            
            self.player_data['wear_armor'][item_type]['왼손'] = item['name']
            self.player_data['wear_armor'][item_type]['오른손'] = item['name']
            
            self.labels[item_type+'left'].setText(item['name'])
            self.labels[item_type+'right'].setText(item['name'])
        else:
            item_type = '무기'
            hands_key = '왼손' if hands == 'left' else '오른손'
            
            self.player_data['wear_armor'][item_type][hands_key] = item['name']

            self.labels[item_type+hands].setText(item['name'])
        self.player_data['inventory'].remove(item['name'])
        
    # 장비 착용하기
    def SetWearArmor(self,item):
        self.player_data['wear_armor'][item['type']] = item['name']
        self.labels[item['type']].setText(item['name'])
        self.player_data['inventory'].remove(item['name'])
                
    # 장비 스텟 빼기(장착 해제)
    def SubStatArmor(self, item_data):
        for stat in ['STR', 'AGI', 'INT', 'LUCK']:
            self.player_data[stat] -= item_data.get('up_stat', {}).get(stat, 0)
            
        for stat in ['attack_score', 'defense_score', 'hp', 'mp']:
            self.player_data[stat] -= item_data.get(stat, 0)
    
    # 장비 장착 해제
    def SetUnWearArmor(self, item_type, item_data, hands = None):
        if item_type == '반지' or item_type == '한 손 무기':
            hands_key = '왼손' if hands == 'left' else '오른손'
            self.player_data['wear_armor'][item_type][hands_key] = '비어있음'
        else:
            self.player_data['wear_armor']['item_type'] = '비어있음'
        