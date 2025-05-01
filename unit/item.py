class Item():
    def __init__(self):
        self.name = ''
        self.description = ''
        
        self.stat = []              # 올려주는 스텟
        self.required_class = []    # 착용 가능 직업
        self.required_stat = []     # 착용 가능 레벨, 스텟
        
        self.attack_score = 0
        self.defense_score = 0