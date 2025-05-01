class Monster():
    def __init__(self):
        self.mp = 0               # 개체의 마력
        self.hp = 0               # 개체의 체력
        self.attack_score = 0     # 개체의 공격력
        self.defense_score = 0    # 개체의 방어력
        self.skills = []          # 개체의 스킬
        self.items = []           # 개체가 드랍하는 아이템
        self.unit_type = ''       # 개체 타입(몬스터, 유닛, npc 등)
        self.money = 0            # 개체가 드랍하는 골드
        self.STR = 0              # 개체의 힘 (공격력, 체력)
        self.AGI = 0              # 개체의 민첩 (회피, 방어력)
        self.INT = 0              # 개체의 지능 (마력, 스킬 데미지)
        self.LUCK = 0             # 개체의 운 (드랍 확률, 크리티컬 확률)
        self.AVOID = 0.0          # 회피 확률
        self.experience = 0       # 사냥시 주는 경험치
        self.LV = 0               # 개체의 레벨
        
    # 공격하기
    def attack_damage(self):
        self.attack_damage
    
    # 스킬 사용하기
    def use_skill(self):
        pass
    
    # 무기 교체하기
    def change_weapon(self):
        pass
    
    