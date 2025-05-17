import pickle
import os

class Item_SAVELOAD:
    def __init__(self):
        self.item_data_path = './data/data_files/item_datas.item'
        
        if (not os.path.exists(self.item_data_path)) or (os.path.getsize(self.item_data_path) == 0):
            self.SaveData({})
            
    
    #  데이터 불러오기(전체)
    def LoadData(self):
        with open(self.item_data_path, 'rb') as f:
            datas =pickle.load(f)
        return datas
    
    # 데이터 저장하기(전체)
    def SaveData(self, data):
        with open(self.item_data_path, 'wb') as f:
            pickle.dump(data, f)

    # 아이템 추가하기(관리자)
    def AddItem(self, data):
        datas = self.LoadData()
        datas[data['name']] = data
        
        self.SaveData(datas)
        
    # 아이템 삭제하기
    def DeleteItem(self, name):
        datas = self.LoadData()
        del datas[name]
        self.SaveData(datas)
        
    # 아이템 검색하기
    def SearchItem(self, name):
        datas = self.LoadData()
        if name in datas.keys():
            data = datas[name]
            return data
        else:
            print('아이템이 목록에 없습니다.')