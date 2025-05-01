class Warrior:
    def __init__(self):
        self.STR = 10
        self.AGI = 3
        self.INT = 5
        self.LUCK = 2
        
        self.attack_score = 0
        self.defense_score = 0
        
        self.hp = 0
        self.mp = 0
        
        self.weapons = []
        
        self.skills = []
        self.skill_tree = [{"skill_name": 'asdf',"skill_level": 0,"required_stat": [],"skill_description": ''}]
        
    def get_status(self):
        self.hp = self.STR * 100
        self.mp = self.INT * 50
        self.attack_score = self.STR * 5
        self.defense_score = round(self.STR * 0.5)
        
        self.weapons = []
        
        return {
            "hp": self.hp,
            "mp": self.mp,
            "STR": self.STR,
            "AGI": self.AGI,
            "INT": self.INT,
            "LUCK": self.LUCK,
            "attack_score": self.attack_score,
            "defense_score": self.defense_score
        }
        
    # 스킬 트리
    def class_skill_tree(self):
        self.skill_tree = [
            {
                "skill_name": '내려치기',
                "skill_level": 1,
                "required_stat": [
                    {
                        "STR":  15,
                    }],
                "skill_description": '강하게 내려친다.',
                "skill_damage": 20,
                "use_mana": 50
            }
            ]
        return self.skill_tree