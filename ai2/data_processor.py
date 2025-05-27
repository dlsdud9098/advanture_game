"""
데이터 처리 및 전처리 모듈
NPC 설정 파일과 기타 지침 파일들을 읽어서 학습용 데이터셋으로 변환
"""

import os
import re
import json
from typing import List, Dict, Tuple, Any
from pathlib import Path
import random


class NPCDataProcessor:
    def __init__(self, base_path: str = "/home/apic/python/advanture_game"):
        self.base_path = Path(base_path)
        self.npc_instruction_path = self.base_path / "data" / "data_files" / "npc_instruction"
        self.other_instruction_path = self.base_path / "data" / "data_files" / "other_instruction"
        
    def read_npc_files(self) -> Dict[str, str]:
        """NPC 설정 파일들을 읽어서 딕셔너리로 반환"""
        npc_data = {}
        
        if self.npc_instruction_path.exists():
            for file_path in self.npc_instruction_path.glob("*.txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    npc_name = file_path.stem
                    npc_data[npc_name] = content
                    
        return npc_data
    
    def read_other_files(self) -> Dict[str, str]:
        """기타 지침 파일들을 읽어서 딕셔너리로 반환"""
        other_data = {}
        
        if self.other_instruction_path.exists():
            for file_path in self.other_instruction_path.glob("*.txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    file_name = file_path.stem
                    other_data[file_name] = content
                    
        return other_data
    
    def parse_npc_setting(self, npc_content: str) -> Dict[str, Any]:
        """NPC 설정 텍스트를 파싱해서 구조화된 데이터로 변환"""
        setting = {}
        
        # NPC 기본 정보 추출
        name_match = re.search(r'이름:\s*(.+)', npc_content)
        if name_match:
            setting['name'] = name_match.group(1).strip()
            
        job_match = re.search(r'직업:\s*(.+)', npc_content)
        if job_match:
            setting['job'] = job_match.group(1).strip()
            
        gender_match = re.search(r'성별:\s*(.+)', npc_content)
        if gender_match:
            setting['gender'] = gender_match.group(1).strip()
            
        personality_match = re.search(r'성격:\s*(.+)', npc_content)
        if personality_match:
            setting['personality'] = personality_match.group(1).strip()
            
        role_match = re.search(r'역할:\s*(.+)', npc_content)
        if role_match:
            setting['role'] = role_match.group(1).strip()
            
        description_match = re.search(r'설명:\s*(.+?)(?=\n[가-힣]+:|$)', npc_content, re.DOTALL)
        if description_match:
            setting['description'] = description_match.group(1).strip()
            
        setting['full_content'] = npc_content
        return setting
    
    def create_training_conversations(self, npc_setting: Dict[str, Any], situation_data: str = None) -> List[Dict[str, str]]:
        """NPC 설정을 바탕으로 학습용 대화 데이터 생성"""
        conversations = []
        
        # 기본 시스템 프롬프트 생성
        system_prompt = self._create_system_prompt(npc_setting, situation_data)
        
        # 다양한 상황별 대화 예시 생성
        conversation_scenarios = self._generate_conversation_scenarios(npc_setting)
        
        for scenario in conversation_scenarios:
            conversation = {
                "system": system_prompt,
                "user": scenario["user"],
                "assistant": scenario["assistant"]
            }
            conversations.append(conversation)
            
        return conversations
    
    def _create_system_prompt(self, npc_setting: Dict[str, Any], situation_data: str = None) -> str:
        """NPC 설정을 바탕으로 시스템 프롬프트 생성"""
        prompt = f"""당신은 {npc_setting.get('name', 'NPC')}입니다.

기본 정보:
- 이름: {npc_setting.get('name', '미정')}
- 직업: {npc_setting.get('job', '미정')}
- 성별: {npc_setting.get('gender', '미정')}
- 성격: {npc_setting.get('personality', '미정')}
- 역할: {npc_setting.get('role', '미정')}

상세 설명:
{npc_setting.get('description', '')}

"""
        
        if situation_data:
            prompt += f"\n현재 상황:\n{situation_data}\n"
            
        prompt += f"""
지침:
1. 위의 캐릭터 설정에 맞게 일관되게 행동하세요.
2. 플레이어와 자연스럽고 몰입감 있는 대화를 나누세요.
3. 캐릭터의 성격과 역할에 맞는 말투와 행동을 보여주세요.
4. 게임 세계관에 맞는 응답을 제공하세요.

{npc_setting.get('full_content', '')}
"""
        return prompt
    
    def _generate_conversation_scenarios(self, npc_setting: Dict[str, Any]) -> List[Dict[str, str]]:
        """NPC 설정에 맞는 대화 시나리오 생성"""
        scenarios = []
        
        name = npc_setting.get('name', 'NPC')
        job = npc_setting.get('job', '')
        personality = npc_setting.get('personality', '')
        
        # 기본 인사 시나리오들
        greetings = [
            {"user": "안녕하세요.", "assistant": f"안녕하십니까. 저는 {name}입니다."},
            {"user": "처음 뵙겠습니다.", "assistant": f"반갑습니다. {name}이라고 합니다."},
            {"user": "누구세요?", "assistant": f"저는 이 세계의 {job}인 {name}입니다."}
        ]
        
        # 신 NPC 특화 시나리오
        if job == "신":
            god_scenarios = [
                {"user": "여기가 어디죠?", "assistant": "이곳은 제가 존재하는 신계입니다. 당신을 이 세계를 구하기 위해 소환했습니다."},
                {"user": "왜 저를 소환했나요?", "assistant": "이 세계에 큰 위기가 닥쳤습니다. 당신의 힘이 필요합니다."},
                {"user": "스킬을 주세요.", "assistant": "당신의 의지와 선택에 따라 적절한 능력을 부여하겠습니다. 먼저 몇 가지 질문에 답해주십시오."},
                {"user": "직업을 정해주세요.", "assistant": "당신에게 맞는 직업을 찾기 위해 질문을 드리겠습니다. 신중히 답변해 주십시오."}
            ]
            scenarios.extend(god_scenarios)
            
        scenarios.extend(greetings)
        return scenarios
    
    def create_fine_tuning_dataset(self) -> List[Dict[str, str]]:
        """파인튜닝용 데이터셋 생성"""
        dataset = []
        
        # NPC 데이터 읽기
        npc_data = self.read_npc_files()
        other_data = self.read_other_files()
        
        # 각 NPC별로 학습 데이터 생성
        for npc_name, npc_content in npc_data.items():
            npc_setting = self.parse_npc_setting(npc_content)
            
            # 상황 데이터 매칭
            situation_data = None
            if 'player_spawn' in other_data:
                situation_data = other_data['player_spawn']
            
            # 대화 데이터 생성
            conversations = self.create_training_conversations(npc_setting, situation_data)
            dataset.extend(conversations)
            
        return dataset
    
    def format_for_llama(self, conversations: List[Dict[str, str]]) -> List[str]:
        """LLaMA 형식으로 대화 데이터 포맷팅"""
        formatted_data = []
        
        for conv in conversations:
            # ChatML 형식으로 포맷팅
            formatted = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{conv['system']}<|eot_id|><|start_header_id|>user<|end_header_id|>
{conv['user']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{conv['assistant']}<|eot_id|><|end_of_text|>"""
            formatted_data.append(formatted)
            
        return formatted_data
    
    def save_dataset(self, dataset: List[Dict[str, str]], output_path: str):
        """데이터셋을 JSON 파일로 저장"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        print(f"데이터셋이 {output_path}에 저장되었습니다.")
        
    def save_formatted_dataset(self, formatted_data: List[str], output_path: str):
        """포맷팅된 데이터셋을 텍스트 파일로 저장"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in formatted_data:
                f.write(item + "\n\n")
        print(f"포맷팅된 데이터셋이 {output_path}에 저장되었습니다.")


if __name__ == "__main__":
    # 테스트 코드
    processor = NPCDataProcessor()
    
    # 데이터셋 생성
    dataset = processor.create_fine_tuning_dataset()
    print(f"생성된 대화 데이터 수: {len(dataset)}")
    
    # 샘플 출력
    if dataset:
        print("\n=== 샘플 데이터 ===")
        print(json.dumps(dataset[0], ensure_ascii=False, indent=2))
    
    # 데이터셋 저장
    processor.save_dataset(dataset, "/home/apic/python/advanture_game/ai2/data/training_dataset.json")
    
    # LLaMA 형식으로 포맷팅 및 저장
    formatted_data = processor.format_for_llama(dataset)
    processor.save_formatted_dataset(formatted_data, "/home/apic/python/advanture_game/ai2/data/formatted_dataset.txt")
