from data.item_data import Item_SAVELOAD

class Item(Item_SAVELOAD):
    def __init__(self,
                name = None,                # 아이템 이름
                description = None,         # 아이템 설명
                attack = None,              # 아이템 사용시 공격력
                defense = None,             # 아이템 사용시 수비력
                hp = None,                  # 아이템 사용시 체력 
                mp = None,                  # 아이템 사용시 마력
                stat = None,                # 아이템 사용시 스텟
                drop = None,                # 아이템 드랍률
                type = None                 # 아이템 분류
                ):
        super().__init__()

        self.item_name = name
        self.item_description = description
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.mp = mp
        self.stat = stat
        self.drop = drop
        self.type = type
        
        # self.item_name = None
        # self.item_description = None
        # self.attack = None
        # self.defense = None
        # self.hp = None
        # self.mp = None
        # self.stat = None
        # self.drop = None
        # self.type = None
        
        self.ItemSave()
        
    # 아이템 추가하기
    def ItemSave(self):
        self.AddItem({
            'name': self.item_name,
            'item_name': self.item_name,
            'item_description': self.item_description,
            'attack': self.attack,
            'defense': self.defense,
            'hp': self.hp,
            'mp': self.mp,
            'stat': self.stat,
            'drop': self.drop,
            'type': self.type
        })