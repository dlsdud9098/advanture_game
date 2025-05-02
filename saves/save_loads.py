import json
import os

class SAVE_LOADS:
    def __init__(self):
        save_file_path = 'saves/datas/saves.json'
        # 데이터 비어있거나 파일이 없음
        if not os.path.exists(save_file_path) or os.path.getsize(save_file_path) == 0:
            with open('saves/datas/saves.json', 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
    
    # 데이터 저장하기
    def data_save(self, player_datas):
        with open('saves/datas/saves.json', 'w', encoding='utf-8') as file:
            json.dump(player_datas, file, indent=4)

        
    # 데이터 가져오기
    def data_load(self):
        with open('saves/datas/saves.json', 'r', encoding='utf-8') as f:
            player_datas = json.load(f)

        return player_datas

    # 새로운 플레이어 데이터 추가하기
    def data_update(self, data):
        player_datas = self.data_load()
        
        # 데이터 비어있음
        if not bool(player_datas):
            player_datas.append(data)
        else:
            names = [player['name'] for player in player_datas]
            if data['name'] in names:
                os.system('clear')
                print('중복된 이름입니다.')
                return 1
            player_datas.append(data)
        self.data_save(player_datas)
    
    # 플레이어 로드하기
    def player_load(self, data):
        data