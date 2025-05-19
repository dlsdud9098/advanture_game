from unit.character_class.warrior import Warrior
from unit.unit import Unit
from entity.money import Money

class Player(Unit, Warrior, Money):
    def __init__(self, name, unit_type, class_):
        # Unit 초기화
        Unit.__init__(self, name, unit_type)
        # Warrior 초기화
        Warrior.__init__(self)
        # Money 초기화
        Money.__init__(self)
        
        self.inventory = ['철 검', '철 갑옷', '하급 회복 물약', '철 반지', '철 반지', '미스릴 검', '철 대검']
        # self.inventory = []
        self.max_inventory_size = 0    # 최대 인벤토리 용량
        
        self.skills = []
        self.wear_armor ={                 # 착용하고 있는 아이템
                '투구': '비어있음',
                '목걸이': '비어있음',
                '반지': {
                        '왼손': '비어있음',
                        '오른손': '비어있음'
                        },
                '갑옷': '비어있음',
                '바지': '비어있음',
                '신발': '비어있음',
                '무기': {
                        '왼손': '비어있음',
                        '오른손': '비어있음'
                        },
                '가방': '비어있음'
            }                
        self.class_ = class_            # 캐릭터의 클래스(직업)
        self.experience = 0     # 경험치
        self.skillpoint = 0    # 스킬 포인트
        
        # 기본 스텟
        self.STR = 10
        self.AGI = 10
        self.INT = 10
        self.LUCK = 5
        
        self.hp = 0
        self.mp = 0
        self.money = 1000
        
        self.lv = 1
    
        
        self.SettingClass()
        self.ClacStat()
    
    # 직업 선택 후 스텟, 아이템, 스킬 등 기본 받기
    def SettingClass(self):
        if self.class_ == '전사':
            stats = self.GetStatusWarrior()
            
        self.STR += stats.get('STR', 0)
        self.AGI += stats.get('AGI', 0)
        self.INT += stats.get('INT', 0)
        self.LUCK += stats.get('LUCK', 0)
        self.hp += stats.get('hp', 0)
        self.mp += stats.get('mp', 0)
            
    # 스텟 및 공격력, 수비력 계산
    def ClacStat(self):
        hp = self.STR * 100
        self.hp += hp
        
        mp = self.INT * 50
        self.mp += mp
        
        self.attack_score = self.STR * 5
        self.defense_score = round(self.STR * 0.5)
        
        self.max_inventory_size = int(self.STR * 0.5)    # 인벤토리는 힘 스텟의 절반
        
    def displaystatus(self):
        print(f'name: {self.name}')
        print(f'lv: {self.lv}')
        print(f'class: {self.class_}')
        print()
        print(f'STR: {self.STR}')
        print(f'AGI: {self.AGI}')
        print(f'INT: {self.INT}')
        print(f'LUCK: {self.LUCK}')
        print()
        print(f'hp: {self.hp}')
        print(f'mp: {self.mp}')
        print()
        print(f'attack: {self.attack_score}')
        print(f'defense: {self.defense_score}')
        
    # 현재 캐릭터 정보 내보내기
    def GetStatus(self):
        stat = {
            'name':self.name,
            'lv':self.lv,
            'class':self.class_,
            
            'STR':self.STR,
            'AGI':self.AGI,
            'INT':self.INT,
            'LUCK':self.LUCK,
            
            'experience':self.experience,
            'skillpoint':self.skillpoint,
            
            'attack_score':self.attack_score,
            'defense_score':self.defense_score,
            
            'inventory':self.inventory,
            'max_inventory_size':self.max_inventory_size,
            
            'hp': self.hp,
            'mp': self.mp,
            
            'money': self.money,
            'wear_armor': self.wear_armor
        }
        
        return stat
    
    def NowCharaterDatas(self):
        datas = {
            'name':self.name,
            'lv':self.lv,
            'class':self.class_,
            
            'STR':self.STR,
            'AGI':self.AGI,
            'INT':self.INT,
            'LUCK':self.LUCK,
            
            'experience':self.experience,
            'skillpoint':self.skillpoint,
            
            'attack_score':self.attack_score,
            'defense_score':self.defense_score,
            
            'inventory':self.inventory,
            'max_inventory_size':self.max_inventory_size,
            
            "wear_armor": self.wear_armor,
            "skill_point": self.skillpoint,
            "money": self.money,
            "unit_type": self.unit_type
        }
        
        return datas