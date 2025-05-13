import random
import importlib
import os

from tabulate import tabulate
import pandas as pd
import time

from unit.item import Item
from unit.player.inventory import Inventory
from unit.player.armor import Armor
from unit.player.money import Money

class Player(Inventory, Armor, Money):
    def __init__(self, **kwargs):
        self.mp = 100                       # 개체의 마력
        self.hp = 100                       # 개체의 체력
        self.attack_score = 10              # 개체의 공격력
        self.defense_score = 5              # 개체의 방어력
        self.AVOID = 0.5                    # 회피 확률
        
        self.skills = []                    # 개체의 스킬
        self.inventory = ['철 검', '튼튼한 갑옷']          # 개체가 소지하고 있는 아이템
        self.wear_armor = {                 # 착용하고 있는 아이템
                '투구': '',
                '목걸이': '',
                '반지': [],
                '갑옷': '',
                '바지': '',
                '신발': '',
                '무기': ''
            }                
        self.max_inventory = 10             # 최대 인벤토리 크기
        self.money = 1000                   # 개체가 소지하고 있는 골드(또는 드랍하는 골드)
        
        self.STR = 10                       # 개체의 힘 (공격력, 체력)
        self.AGI = 10                       # 개체의 민첩 (회피, 방어력)
        self.INT = 10                       # 개체의 지능 (마력, 스킬 데미지)
        self.LUCK = 5                       # 개체의 운 (드랍 확률)
        
        self.experience = 0                 # 개체의 경험치(사냥시 주는 경험치)
        self.skillpoint = 0                 # 개체가 가지고 있는 스킬 포인트
        self.honor = 0                      # 명성치
        
        self.name = kwargs['name']          # 개체 이름
        self.LV = 1                         # 개체의 레벨
        self.CLASS = kwargs['CLASS']        # 직업
        
        self.unit_type = 'Player'           # 개체 타입(몬스터, 유닛, npc 등)
        
        self.init_status()                  # 캐릭터 만들기
        self.init_inventory()               # 인벤토리 초기화하기
        
    # 직업별 초기 스텟 설정
    def init_status(self):
        if self.CLASS == '전사':
            from unit.character_class.warrior import Warrior
            warrior = Warrior()
            
            stats = warrior.get_status()
            self.hp += stats.get('hp', 0)
            self.mp += stats.get('mp', 0)
            
            self.STR += stats.get('STR', 0)
            self.AGI += stats.get('AGI', 0)
            self.INT += stats.get('INT', 0)
            
            self.attack_score += stats.get('attack_score', 0)
            self.defense_score += stats.get('defense_score', 0)
            
    # 인벤토리 초기화하기
    def init_inventory(self):
        # self.inventory = []
        self.max_inventory = 10

    # 캐릭터 정보 가져오기
    def get_status(self):
        stat = {
            "mp": self.mp,
            "hp": self.hp,
            "attack_score": self.attack_score,
            "defense_score": self.defense_score,
            "AVOID": self.AVOID,
            "skills": self.skills,
            "inventory": self.inventory,
            "user_armor": self.wear_armor,
            "max_inventory": self.max_inventory,
            "money": self.money,
            "STR": self.STR,
            "AGI": self.AGI,
            "INT": self.INT,
            "LUCK": self.LUCK,
            "experience": self.experience,
            "skillpoint": self.skillpoint,
            "honor": self.honor,
            "name": self.name,
            "LV": self.LV,
            "CLASS": self.CLASS,
            "unit_type": self.unit_type
        }
        
        return stat
        
    # 현재 스텟창 보기
    def ViewStatus(self):
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
        
        print(tabulate(display_status, tablefmt='plain', showindex=False, headers=[]), '\n')
        