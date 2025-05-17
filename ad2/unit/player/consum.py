from unit.item import Item

class Consum:
    def __init__(self):
        self.inventory = None
        self.item_name = None
        
        self.item_types = None
    
    # 소모품 아이템 목록
    def ConsumItem(self, inventory):
        iteM = Item()
        data_list = []
        for item in inventory:
            data = iteM.SearchItem(item)
            if data:
                if data['type'] in '소모품':
                    data_list.append(data)
                
        # print(data_list)
        return data_list