import random
import importlib

from tabulate import tabulate
import pandas as pd

# from character_class import Warrior

class Player():
    def __init__(self, **kwargs):
        self.mp = 100                       # 개체의 마력
        self.hp = 100                       # 개체의 체력
        self.attack_score = 10              # 개체의 공격력
        self.defense_score = 5              # 개체의 방어력
        self.skills = []                    # 개체의 스킬
        self.inventory = []                     # 개체가 소지하고 있는 아이템
        self.use_items = []                 # 착용하고 있는 아이템
        self.unit_type = ''                 # 개체 타입(몬스터, 유닛, npc 등)
        self.money = 1000                   # 개체가 소지하고 있는 골드(또는 드랍하는 골드)
        self.STR = 10                       # 개체의 힘 (공격력, 체력)
        self.AGI = 10                       # 개체의 민첩 (회피, 방어력)
        self.INT = 10                       # 개체의 지능 (마력, 스킬 데미지)
        self.LUCK = 5                       # 개체의 운 (드랍 확률)
        self.AVOID = 0.5                    # 회피 확률
        self.experience = 0                 # 개체의 경험치(사냥시 주는 경험치)
        self.skillpoint = 0                 # 개체가 가지고 있는 스킬 포인트
        self.LV = 1                         # 개체의 레벨
        self.honor = 0                      # 명성치
        self.CLASS = kwargs['CLASS']        # 직업
        self.name = kwargs['name']          # 개체 이름
        
        self.init_status()                  # 캐릭터 만들기
        
    def init_status(self):
        if self.CLASS == '전사':
            ch_class = 'warrior'
            # 동적으로 character_class 모듈 불러오기
            class_module = f"unit.character_class.{ch_class}"
            module = importlib.import_module(class_module)
        
        
        if hasattr(module, 'Warrior'):
            warrior_class = getattr(module, 'Warrior')  # Warrior 클래스를 가져옴
            warrior_instance = warrior_class()  # Warrior 인스턴스를 생성
            stats = warrior_instance.get_status()  # get_status 호출
            
            self.hp += stats.get('hp', 0)
            self.mp += stats.get('mp', 0)
            
            self.STR += stats.get('STR', 0)
            self.AGI += stats.get('AGI', 0)
            self.INT += stats.get('INT', 0)
            
            self.attack_score += stats.get('attack_score', 0)
            self.defense_score += stats.get('defense_score', 0)
        
        # elif self.CLASS == '마법사':
        #     pass
        # elif self.CLASS == '궁수':
        #     pass
        # elif self.CLASS == '성직자':
        #     pass
        # elif self.CLASS == '상인':
        #     pass
        # elif self.CLASS == '도적':
        #     pass
        
    # 공격하기
    def attack_damage(self):
        if random.random() < self.LUCK * 0.01:
            damage = self.attack_damage * 2
        else:
            damage = self.attack_damage
    
    # 스킬 사용하기
    def use_skill(self):
        pass
    
    # 무기 교체하기
    def change_weapon(self):
        pass
    
    
    # 소지하고 있는 골드
    def how_money(self):
        print(f"Gold: {self.money}")
        pass
    
    # 소지품
    def bag(self):
        pass
    
    # 행동
    def behavior(self):
        pass
    
    # 클래스 선택
    def select_class(self):
        pass
    
    # 경험치 바
    def experience_bar(self, length=20):
        max_xp = self.LV ** 10
        ratio = self.experience / max_xp
        filled_length = int(ratio * length)  # 채워진 부분 길이
        bar = "#" * filled_length + "-" * (length - filled_length)  # #로 채우고, -로 빈 공간 채우기
        return bar
    
    # 현제 스테이터스 보기
    def status(self):
        MAX_LENGTH = 50
        
        # 빈 DataFrame 생성: 4열로 생성
        display_status = pd.DataFrame(index=range(7), columns=range(4))

        # 데이터 추가
        display_status.iloc[0, 0] = "Level"
        display_status.iloc[0, 1] = self.LV
        display_status.iloc[1, 0] = "Name"
        display_status.iloc[1, 1] = self.name
        display_status.iloc[1, 2] = "CLASS"
        display_status.iloc[1, 3] = self.CLASS
        display_status.iloc[2, 0] = "HP"
        display_status.iloc[2, 1] = self.hp
        display_status.iloc[3, 0] = "MP"
        display_status.iloc[3, 1] = self.mp
        display_status.iloc[3, 2] = "소지 골드"
        display_status.iloc[3, 3] = self.money
        display_status.iloc[4, 0] = "STR"
        display_status.iloc[4, 1] = self.STR
        display_status.iloc[5, 0] = "AGI"
        display_status.iloc[5, 1] = self.AGI
        display_status.iloc[6, 0] = "INT"
        display_status.iloc[6, 1] = self.INT
        
        display_status.fillna('', inplace=True)
        

        print(tabulate(display_status, tablefmt='plain', showindex=False, headers=[]))
        
        return {
            "LV": self.LV,
            "name": self.name,
            "CLASS": self.CLASS,
            "hp": self.hp,
            "mp": self.mp,
            "STR": self.STR,
            "AGI": self.AGI,
            "INT": self.INT,
            "money": self.money,
            "attack_score": self.attack_score,
            "defense_score": self.defense_score,
            "honor": self.honor,
            "experience": self.experience,
            "skillpoint": self.skillpoint,
            "skills": self.skills,
            "use_items": self.inventory,
        }