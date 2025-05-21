from unit.player import Player
class NPC(Player):
    def __init__(self, name, unit_type, class_):
        super().__init__(name, unit_type, class_)
        
        