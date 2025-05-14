from unit.item import Item

class Armor:
    def __init__(self):
        self.inventory = None
        self.item_name = None
        
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
    def CanWearItem(self):
        iteM = Item()
        data_list = {}
        for item in self.inventory:
            data = iteM.SearchItem(item)
            if data:
                if data['type'] in ['weapon', 'helmat', 'top_clothes', 'bottom_clothes', 'ring', 'necklace', 'shose']:
                    data_list[data['name']] = data
                
        print(data_list)
        return data_list