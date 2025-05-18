import pickle
import os
import pandas as pd


class Item_SAVELOAD:
    def __init__(self):
        self.item_data_path = "./data/data_files/item_datas.item"

        if (not os.path.exists(self.item_data_path)) or (
            os.path.getsize(self.item_data_path) == 0
        ):
            self.SaveData([])

    #  데이터 불러오기(전체)
    def LoadData(self):
        df = pd.read_pickle(self.item_data_path)
        df = df.dropna()
        return df

    # 데이터 저장하기(전체)
    def SaveData(self, datas):
        df = pd.DataFrame(datas)
        
        df.to_pickle(self.item_data_path)

    # 아이템 추가하기(관리자)
    def AddItem(self, data):
        datas = self.LoadData()
        datas = datas.to_dict(orient='records')
        datas.append(data)
        
        self.SaveData(datas)

    # 아이템 삭제하기
    def DeleteItem(self, name):
        df = self.LoadData()
        df = df[df['name'] != name]
        
        df = df.to_dict(orient='records')
        self.SaveData(df)

    # 아이템 검색하기
    def SearchItem(self, name):
        df = self.LoadData()
        
        df = df[df['name'] == name]
        if not df.empty:
            df = df.to_dict(orient='records')[0]
            return df
        else:
            print('아이템이 목록에 없습니다.')
    
    # 아이템 검색(여러개)
    def SearchItemList(self, item_list):
        df = self.LoadData()
        result = []
        for item_name in item_list:
            match = df[df["name"] == item_name]  # 데이터프레임에서 아이템 검색
            if not match.empty:
                result.append(match.iloc[0].to_dict())  # 딕셔너리 형태로 데이터 가져오기
                
        return result
