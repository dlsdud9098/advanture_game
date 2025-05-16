from unit.item import Item

class Armor:
    def __init__(self):
        self.inventory = None
        self.item_name = None
        
        self.item_types = ['갑옷', '바지', '신발', '반지','목걸이', '투구', '무기']
        
    # 무기, 갑옷 착용하기
    def WearArmor(self):
        # 현재 인벤토리에서 장비와 관련된 아이템 목록 추출
        items = self.CanWearItem()
    
    # 착용 해제
    def UnWearArmor(self):
        pass
    
    # 현재 착용하고 있는 아이템
    def ViewArmor(self):
        pass
    
    # 착용할 수 있는 아이템 목록
    def CanWearItem(self, inventory):
        iteM = Item()
        data_list = []
        for item in inventory:
            data = iteM.SearchItem(item)
            if data:
                if data['type'] in self.item_types:
                    data_list.append(data)
                
        # print(data_list)
        return data_list