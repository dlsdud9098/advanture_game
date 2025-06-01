import os
import json
import re
from glob import glob

class GameDataPreprocessor:
    """게임 데이터를 instruction-following 형식으로 전처리하는 클래스"""
    
    def __init__(self, data_dir="data/data_files"):
        self.data_dir = data_dir
        self.system_prompt = "당신은 게임 '어드벤처 월드'의 AI입니다. 플레이어와 자연스럽게 대화하며 게임을 진행해주세요."
    
    def parse_npc_file(self, file_path):
        """NPC 파일을 파싱하여 정보 추출"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        npc_data = {
            'name': '',
            'job': '',
            'gender': '',
            'personality': '',
            'role': '',
            'description': '',
            'content': content
        }
        
        # 정규표현식으로 정보 추출
        patterns = {
            'name': r'이름:\s*(.+)',
            'job': r'직업:\s*(.+)',
            'gender': r'성별:\s*(.+)',
            'personality': r'성격:\s*(.+)',
            'role': r'역할:\s*(.+)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                npc_data[key] = match.group(1).strip()
        
        return npc_data
    
    def create_god_conversations(self):
        """신 김샐프와의 대화 생성"""
        questions = [
            "당신의 가장 두려운 것은 무엇인가요?",
            "당신이 가장 존경하는 사람은 누구인가요?",
            "스트레스를 받을 때는 주로 어떻게 해결하시나요?",
            "당신의 가장 소중한 기억은 무엇인가요?",
            "어려운 상황에서 가장 먼저 하는 행동은 무엇인가요?",
            "당신이 가장 좋아하는 활동은 무엇인가요?",
            "친구들과 함께 있을 때 주로 어떤 역할을 하나요?",
            "새로운 환경에 적응할 때 어떤 방식을 선호하나요?",
            "중요한 결정을 내릴 때 무엇을 가장 중요하게 생각하나요?",
            "당신의 꿈이나 목표는 무엇인가요?"
        ]
        
        responses = [
            ("어두운 곳을 무서워합니다.", "신중하고 침착한 성격", "민첩"),
            ("저를 키워준 부모님입니다.", "책임감과 동료애", "힘"),
            ("조용한 곳에서 책을 읽습니다.", "창의적이고 독립적", "지능"),
            ("친구와 함께한 모험입니다.", "모험심과 우정", "운"),
            ("상황을 차분히 분석합니다.", "분석적 사고", "지능"),
            ("새로운 것을 배우는 것입니다.", "학습 욕구", "지능"),
            ("팀을 이끄는 리더 역할을 합니다.", "리더십", "힘"),
            ("빠르게 적응하며 행동합니다.", "적응력과 순발력", "민첩"),
            ("모든 사람의 이익을 고려합니다.", "균형감과 판단력", "운"),
            ("세상을 더 나은 곳으로 만드는 것입니다.", "이타적 성향", "힘")
        ]
        
        conversations = []
        
        # 게임 시작 대화
        conversations.append({
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": "게임을 시작하고 싶습니다."},
                {"role": "assistant", "content": "안녕하세요, 용사님! 저는 이 세계의 신 김샐프입니다. 이 세계가 위험에 처해 있어 당신을 불러왔습니다. 먼저 당신에 대해 알아보고 적절한 능력을 부여해드리겠습니다. 첫 번째 질문입니다."}
            ]
        })
        
        # 질문-답변 대화들
        for i, (question, (user_answer, analysis, stat)) in enumerate(zip(questions[:5], responses[:5])):
            # 질문하는 대화
            conversations.append({
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": "네, 답변하겠습니다."},
                    {"role": "assistant", "content": f"{question}"}
                ]
            })
            
            # 답변에 대한 반응
            if i < 4:  # 마지막이 아닌 경우
                conversations.append({
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_answer},
                        {"role": "assistant", "content": f"{analysis}이 엿보이는군요. 좋습니다. 다음 질문입니다."}
                    ]
                })
            else:  # 마지막 질문의 경우
                conversations.append({
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_answer},
                        {"role": "assistant", "content": f"{analysis}이 보입니다. 모든 질문이 끝났습니다. 당신의 답변을 바탕으로 초기 능력을 부여해드리겠습니다.\n\n📊 초기 스탯:\n힘: 14\n민첩: 12\n지능: 16\n운: 13\n\n🎭 직업: 마법사\n\n이제 세계를 구하기 위한 모험을 시작하실 수 있습니다!"}
                    ]
                })
        
        return conversations
    
    def create_gameplay_conversations(self):
        """게임플레이 대화 생성"""
        conversations = [
            # 마을 탐험
            {
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": "마을에 도착했습니다."},
                    {"role": "assistant", "content": "🏘️ 평화로운 마을에 도착하셨습니다.\n\n주변을 둘러보니 다음과 같은 장소들이 보입니다:\n• 🏪 상점 - 장비와 아이템 구매\n• 🏨 여관 - 휴식 및 정보 수집\n• 📋 퀘스트 게시판 - 의뢰 확인\n• 👥 마을 광장 - 주민들과 대화\n\n어디로 가시겠습니까?"}
                ]
            },
            
            # 전투 시스템
            {
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": "고블린과 전투를 시작합니다."},
                    {"role": "assistant", "content": "⚔️ 전투 시작!\n\n🧌 야생 고블린이 나타났습니다!\n고블린 HP: 30/30\n당신의 HP: 50/50, MP: 25/25\n\n🎯 행동을 선택하세요:\n1. ⚔️ 기본 공격\n2. 🔥 파이어볼 (MP 8)\n3. ❄️ 아이스 볼트 (MP 6)\n4. 🛡️ 방어\n5. 🏃 도망"}
                ]
            },
            
            # 퀘스트 수행
            {
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": "퀘스트를 확인하고 싶습니다."},
                    {"role": "assistant", "content": "📋 현재 이용 가능한 퀘스트:\n\n🟢 [초급] 늑대 퇴치\n- 내용: 마을 근처의 늑대 5마리 처치\n- 보상: 금화 100, 경험치 50\n- 난이도: ★☆☆\n\n🟡 [중급] 잃어버린 보물\n- 내용: 숲 깊숙한 곳의 보물 상자 찾기\n- 보상: 금화 300, 마법 아이템\n- 난이도: ★★☆\n\n🔴 [고급] 드래곤 소굴 정화\n- 내용: 고대 드래곤 처치\n- 보상: 금화 1000, 전설 장비\n- 난이도: ★★★\n\n어떤 퀘스트를 선택하시겠습니까?"}
                ]
            },
            
            # 레벨업
            {
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": "레벨업을 했습니다!"},
                    {"role": "assistant", "content": "🎉 축하합니다! 레벨 업!\n\n✨ 레벨 2 → 레벨 3\n\n📈 스탯 증가:\n• HP: 50 → 60 (+10)\n• MP: 25 → 30 (+5)\n• 힘: 14 → 15 (+1)\n• 지능: 16 → 18 (+2)\n\n🆕 새로운 스킬 습득:\n🔥 파이어스톰 - 광범위 화염 공격 (MP 15)\n\n현재 능력치를 확인하시겠습니까?"}
                ]
            }
        ]
        
        return conversations
    
    def process_all_data(self):
        """모든 데이터를 처리하여 훈련용 데이터셋 생성"""
        all_conversations = []
        
        # 신과의 대화 추가
        god_conversations = self.create_god_conversations()
        all_conversations.extend(god_conversations)
        
        # 게임플레이 대화 추가
        gameplay_conversations = self.create_gameplay_conversations()
        all_conversations.extend(gameplay_conversations)
        
        # 기존 파일들 처리 (있다면)
        npc_files = glob(os.path.join(self.data_dir, 'npc_instruction/*.txt'))
        for file_path in npc_files:
            if os.path.exists(file_path):
                npc_data = self.parse_npc_file(file_path)
                # NPC별 특화 대화 생성 로직 추가