# from unit.player.player import Player

class Inventory():
    def __init__(self):
        pass
        self.inventory = None
        self.max_inventory = None
        
    # 인벤토리에 아이템 넣기
    def AddInventory(self):
        pass
    
    # 인벤토리에서 아이템 빼기
    def DeleteInventory(self):
        pass
    
    # 인벤토리 목록 출력하기
    def ViewInventory(self):
        print(f"{len(self.inventory)}/{self.max_inventory}")
        print(self.inventory)