from data.item_data import Item_SAVELOAD

class Consum(Item_SAVELOAD):
    def __init__(self):
        super().__init__()
        
    # 소모품만 추출하기
    def OnlyConsumInventory(self, inventory):
        df = self.LoadData()
        
        df = df[df['type'] == '소모품']
        
        datas = df.to_dict(orient='records')
        return datas
    