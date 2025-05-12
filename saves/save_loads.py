import os
import pickle

class SAVE_LOADS:
    def __init__(self):
        save_file_path = 'saves/datas/saves.bin'
        # 데이터 비어있거나 파일이 없음
        if not os.path.exists(save_file_path) or os.path.getsize(save_file_path) == 0:
            with open(save_file_path, 'wb') as f:
                pickle.dump({}, f)
    
    # 데이터 저장하기
    def data_save(self, player_datas):
        with open('saves/datas/saves.bin', 'wb') as file:
            pickle.dump(player_datas, file)

        
    # 데이터 가져오기
    def data_load(self):
        with open('saves/datas/saves.bin', 'rb') as f:
            player_datas = pickle.load(f)
        
        return player_datas

    # 새로운 플레이어 데이터 추가하기
    def data_update(self, data):
        player_datas = self.data_load()
        
        if data['name'] in player_datas.keys():
            os.system('clear')
            print('중복된 이름입니다.')
            return 1
        
        else:
            player_datas[data['name']] = data
            
        self.data_save(player_datas)
        return 0
    
    # 플레이어 로드하기
    def player_load(self, data):
        data