import pickle
import os

class Player_SAVELOAD:
    def __init__(self):
        self.player_data_path = './data/data_files/player_datas.player'
        
        if (not os.path.exists(self.player_data_path)) or (os.path.getsize(self.player_data_path) == 0):
            self.SaveData({})
    
    # 데이터 불러오기
    def LoadData(self):
        with open(self.player_data_path, 'rb') as f:
            datas = pickle.load(f)
        return datas
    
    # 데이터 저장하기
    def SaveData(self, data):
        with open(self.player_data_path, 'wb') as f:
            pickle.dump(data, f)

    # 새로운 플레이어 데이터 추가하기
    def AddData(self, data):
        datas = self.LoadData()
        if data['name'] in datas.keys():    # 새로 만든 캐릭터의 닉네임이 이미 존재함
            print('이미 존재하는 닉네임입니다.')
            return 1
        elif len(datas) > 5:
            print('생성 개수를 초과하였습니다.')
            return 2
        else:
            datas[data['name']] = data
            
            self.SaveData(datas)
            return data
            
    # 플레이어 데이터 삭제하기
    def DeleteData(self, name):
        datas = self.LoadData()
        
        del datas[name]
        
        self.SaveData(datas)
        
    # 플레이어 불러오기
    def LoadPlayer(self, name):
        datas = self.LoadData()
        # print(datas)
        self.player_data = datas[name]
        # print(self.player_data)
        
        return self.player_data