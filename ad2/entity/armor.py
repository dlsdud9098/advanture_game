from data.item_data import Item_SAVELOAD

class Armor(Item_SAVELOAD):
    def __init__(self,
                name,
                description,
                required_stat,
                required_class,
                up_stat,
                attack,
                defense,
                hp,
                mp,
                drop,
                type
                ):
        
        self.name = name
        self.description = description
        self.required_stat = required_stat
        self.required_class = required_class
        self.up_stat = up_stat
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.mp = mp
        self.drop = drop
        self.type = type
        

    def AddItem(self):
        self.SaveData({
            'name': self.name,
            'description': self.description,
            'required_stat': self.required_stat,
            'required_class': self.required_class,
            'up_stat': self.up_stat,
            'attack': self.attack,
            'defense': self.defense,
            'hp': self.hp,
            'mp': self.mp,
            'drop': self.drop,
            'type': self.type
        })