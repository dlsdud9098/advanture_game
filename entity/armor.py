from data.item_data import Item_SAVELOAD
import pandas as pd

class Armor(Item_SAVELOAD):
    def __init__(self):
        super().__init__()
        
        self.armor_tags = ['무기', '갑옷', '바지', '신발', '목걸이', '반지', '투구']

    # 장비 아이템만 추출
    def OnlyLoadArmor(self):
        df = self.LoadData()
        df = df[df['type'].isin(self.armor_tags)]
        datas = df.to_dict(orient='records')
        return datas
        
        