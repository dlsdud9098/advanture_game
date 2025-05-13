import os
import json

class Monster:
    def __init__(self, args):
        self.mp = args['mp']                        # 개체의 마력
        self.hp = args['hp']                        # 개체의 체력
        self.attack_score = args['attack_score']    # 개체의 공격력
        self.defense_score = args['defense_score']  # 개체의 방어력
        self.skills = args['skills']                # 개체의 스킬
        self.inventory = args['inventory']          # 개체가 드랍하는 아이템 목록
        self.unit_type = 'Monster'                  # 개체 타입(몬스터, 유닛, npc 등)
        self.money = args['money']                  # 개체가 드랍하는 골드
        self.STR = args['STR']                      # 개체의 힘 (공격력, 체력)
        self.AGI = args['AGI']                      # 개체의 민첩 (회피, 방어력)
        self.INT = args['INT']                      # 개체의 지능 (마력, 스킬 데미지)
        self.LUCK = args['LUCK']                    # 개체의 운 (드랍 확률)
        self.AVOID = args['AVOID']                  # 회피 확률
        self.experience = args['experience']        # 개체 사냥시 주는 경험치
        self.LV = args['LV']                        # 개체의 레벨
        self.name = args['name']                    # 개체 이름

        self.init_status()                          # 캐릭터 만들기
        
    # 공격하기
    def attack_damage(self):
        self.attack_damage
    
    # 스킬 사용하기
    def use_skill(self):
        pass
    
    # 몬스터 DB
    def MonsterDB(self):
        save_file_path = 'saves/datas/monster_data.json'
        # 데이터 비어있거나 파일이 없음
        if not os.path.exists(save_file_path) or os.path.getsize(save_file_path) == 0:
            with open(save_file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
        pass
    
    # 몬스터 추가
    def AddMonsterData(self):
        pass