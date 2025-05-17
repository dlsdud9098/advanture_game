class Warrior:
    def __init__(self):
        self.warrior_STR = 10
        self.warrior_AGI = 3
        self.warrior_INT = 5
        self.warrior_LUCK = 2
        
        self.warrior_hp = 500
        self.warrior_mp = 100
        
        self.weapons = []
        
        self.skills = []
        self.skill_tree = [{"skill_name": 'asdf',"skill_level": 0,"required_stat": [],"skill_description": ''}]
        
    def GetStatusWarrior(self):
        return {
            "hp": self.warrior_hp,
            "mp": self.warrior_mp,
            "STR": self.warrior_STR,
            "AGI": self.warrior_AGI,
            "INT": self.warrior_INT,
            "LUCK": self.warrior_LUCK
        }
        
    # 스킬 트리
    def class_skill_tree(self):
        self.skill_tree = [
            {
                "skill_name": '내려치기',                   # 스킬 이름
                "skill_level": 1,                         # 스킬 레벨
                "required_level": 1,
                "required_stat": [                        # 스킬을 사용하는데 필요 조건
                    {
                        "STR":  15,
                    }],
                "skill_description": '강하게 내려친다.',     # 스킬 설명
                "skill_damage": 20,                       # 스킬 데미지
                "required_mana": 50                            # 필요 마나
            }
            ]
        return self.skill_tree