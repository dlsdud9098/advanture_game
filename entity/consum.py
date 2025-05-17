from data.item_data import Item_SAVELOAD

class Consum(Item_SAVELOAD):
    def __init__(self):
        super().__init__()
        
    # 소모품만 추출하기
    def OnlyConsumInventory(self, inventory):
        datas = self.LoadData()
        
        df = df[datas['name'].isin(inventory)]
        datas = df.to_dict(orient='records')
        return datas
    