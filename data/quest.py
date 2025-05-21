import pandas as pd
import os

"""
퀘스트 식별 번호
    quest_id
        NPC제공 - NPC000
        사냥 퀘스트 - HNT000
        시나리오 퀘스트 - SNR000
        시스템 퀘스트 - SYS000
퀘스트 타입
    quest_type
        Hunt    사냥
        Collect 수집
        Escort  호위
        Deliver 전달

퀘스트 난이도
    quest_dificult
        F ~ SSS
퀘스트 상황
    quest_status
        Not Started
        In Progress
        Completed
퀘스트 이름
    quest name
퀘스트를 받기 위한 조건(트리거)
    quest_trigger
        required_level  필요 레벨
        required_items  필요 아이템
        required_class  직업
퀘스트 제공자(NCP 등)
    quest_order         퀘스트 제공자(NPC, SYSTEM 등)
퀘스트 클리어 조건
    quest_completion_conditions
        target      퀘스트 목표
        count       수량(몬스터 수, 아이템 수)
퀘스트 실패 조건
    quest_fail_trigger
        time
        dead
퀘스트 클리어 보상
    quest_reward
다음 퀘스트(연계일시)
    next_quest
"""

class Quest:
    def __init__(self):
        self.data_path = './data/data_files/quest.csv'

        if (not os.path.exists(self.data_path)) or (os.path.getsize(self.data_path) == 0):
            columns = [
                "quest_id", "quest_type", "quest_difficult", "quest_status",
                "quest_name", "quest_description", "quest_trigger", 
                "quest_order", "quest_completion_contitions", 
                "quest_fail_trigger", "quest_reward", "next_quest"
            ]
            self.SaveQuest(pd.DataFrame(columns=columns))

    # 퀘스트 목록 불러오기
    def LoadQuest(self):
        df = pd.read_csv(self.data_path, encoding='utf-8')
        df = df.dropna(axis=1)
        return df
    
    # 퀘스트 저장하기
    def SaveQuest(self, df):
        df.to_csv(self.data_path, encoding='utf-8', index=False)

    # 퀘스트 추가하기
    def AddQuest(self, data):
        df_old = self.LoadQuest()
        
        df = pd.DataFrame([data])
        df = pd.concat([df_old, df], ignore_index=True)
        self.SaveQuest(df)