import json

class SAVE_LOADS:
    def __init__(self):
        with open('saves/datas/saves.json', 'r') as f:
            self.datas = json.load(f)
    
    # 세이브된 데이터 목록 보기
    def save_loads(self):
        with open('saves/datas/saves.json', 'r') as f:
            self.datas = json.load(f)
        
        
        (f"{self.datas['LV']}, {self.datas['name']}")
    
    # 데이터 새로 저장하기
    def save(self, data):
        print(data)
        with open('saves/datas/saves.json', 'w', encoding='utf-8') as f:
            
            for player in data:
                json.dump(player, indent=4)
    
    def update_player_data(self, data):
        player_data = self.load_player_data()

        for player in player_data:
            if data['name'] == player['name']:
                print('이름이 이미 존재함')
            else:
                player_data.append(data)
                
                self.save(player_data)
                return 0
        
        
    def load_player_data(self):
        player_data = []
        with open('saves/datas/saves.json', 'r') as f:
            data = json.load(f)
        
        player_data.append(data)

        return player_data

    # 데이터 불러오기
    def load(self):
        pass
    
    def display_save_data(self):
        pass