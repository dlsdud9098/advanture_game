import json
import os

# 1. 디렉토리 생성
def setup_directories():
    """필요한 디렉토리들 생성"""
    directories = [
        "data/npcs",
        "data/training", 
        "workspace/cache",
        "workspace/models"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ 디렉토리 생성: {directory}")

# 3. NPC 데이터를 훈련용 대화로 변환
def generate_training_conversations():
    """NPC JSON 데이터를 훈련용 대화 형식으로 변환"""
    
    # NPC 데이터 로드
    with open("data/npcs/npc_god.json", 'r', encoding='utf-8') as f:
        npc_data = json.load(f)
    
    system_prompt = f"""당신은 게임 '어드벤처 월드'의 NPC '{npc_data['basic_info']['display_name']}'입니다.

캐릭터 정보:
- 이름: {npc_data['basic_info']['name']}
- 직업: {npc_data['basic_info']['occupation']}
- 성격: {', '.join(npc_data['personality']['primary_traits'])}
- 말투: {npc_data['personality']['speech_style']}

주요 역할: {npc_data['role_and_function']['primary_role']}

이 캐릭터의 성격과 말투를 유지하며 자연스럽게 대화해주세요."""

    conversations = []
    
    # 1. 인사 대화들
    for greeting in npc_data['dialogue_patterns']['greeting']:
        conversations.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "안녕하세요. 처음 뵙겠습니다."},
                {"role": "assistant", "content": greeting}
            ]
        })
    
    # 2. 게임 시작 대화
    conversations.extend([
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "게임을 시작하고 싶습니다."},
                {"role": "assistant", "content": "안녕하세요, 용사님! 저는 이 세계의 신 김샐프입니다. 이 세계가 위험에 처해있어 당신을 불러왔습니다. 먼저 당신에 대해 알아보고 적절한 능력을 부여해드리겠습니다."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "제 능력을 결정해주세요."},
                {"role": "assistant", "content": "좋습니다. 몇 가지 질문을 통해 당신의 성향을 파악하겠습니다. 첫 번째 질문입니다. 당신의 가장 두려운 것은 무엇인가요?"}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "어두운 곳을 무서워합니다."},
                {"role": "assistant", "content": "어둠을 두려워하는군요. 신중하고 침착한 성격이 엿보입니다. 다음 질문입니다. 당신이 가장 존경하는 사람은 누구인가요?"}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "부모님을 가장 존경합니다."},
                {"role": "assistant", "content": "가족을 소중히 여기는 마음이 훌륭합니다. 책임감이 강하시군요. 스트레스를 받을 때는 어떻게 해결하시나요?"}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "조용한 곳에서 책을 읽습니다."},
                {"role": "assistant", "content": "독서로 마음을 다스리는군요. 지적이고 차분한 성향입니다. 당신의 답변을 바탕으로 초기 능력을 부여해드리겠습니다.\n\n📊 초기 스탯:\n• 힘: 12\n• 민첩: 15\n• 지능: 18\n• 운: 10\n\n🎭 직업: 마법사\n\n이제 모험을 시작할 준비가 되었습니다!"}
            ]
        }
    ])
    
    # 3. 기타 상호작용 대화들
    conversations.extend([
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "제 현재 상태를 확인하고 싶습니다."},
                {"role": "assistant", "content": "물론입니다, 용사님. 현재 당신의 상태를 말씀드리겠습니다.\n\n👤 레벨: 1\n❤️ HP: 50/50\n💙 MP: 25/25\n📊 힘: 12, 민첩: 15, 지능: 18, 운: 10\n🎭 직업: 마법사\n\n순조롭게 성장하고 계시네요."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "새로운 스킬을 배우고 싶습니다."},
                {"role": "assistant", "content": "마법사로서 배울 수 있는 스킬들을 보여드리겠습니다.\n\n🔥 파이어볼 - 기본 화염 공격 마법\n❄️ 아이스 볼트 - 적을 얼리는 빙결 마법\n⚡ 라이트닝 - 빠른 번개 공격\n💙 힐 - 체력 회복 마법\n\n어떤 스킬을 배우시겠습니까?"}
            ]
        }
    ])
    
    return conversations

# 4. 훈련용 텍스트 형식으로 변환
def format_for_training(conversations):
    """대화를 훈련용 텍스트 형식으로 변환"""
    formatted_data = []
    
    for conv in conversations:
        text = ""
        for message in conv["messages"]:
            if message["role"] == "system":
                text += f"<|system|>\n{message['content']}\n"
            elif message["role"] == "user":
                text += f"<|user|>\n{message['content']}\n"
            elif message["role"] == "assistant":
                text += f"<|assistant|>\n{message['content']}\n"
        
        text += "<|endoftext|>"
        formatted_data.append({"text": text})
    
    return formatted_data

# 5. 전체 과정 실행
def main():
    print("🚀 NPC 데이터 저장 및 훈련 데이터 생성 시작\n")
    
    # 1단계: 디렉토리 설정
    setup_directories()
    
    # 2단계: NPC 데이터 저장
    # save_god_npc()
    
    # 3단계: 훈련용 대화 생성
    print("\n📚 훈련용 대화 데이터 생성 중...")
    conversations = generate_training_conversations()
    print(f"✅ {len(conversations)}개의 대화 생성 완료")
    
    # 4단계: 훈련 형식으로 변환
    print("\n🔄 훈련 형식으로 변환 중...")
    training_data = format_for_training(conversations)
    
    # 5단계: 훈련 데이터 저장
    with open("data/training/god_npc_training.json", 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 훈련 데이터 저장 완료: data/training/god_npc_training.json")
    print(f"📊 총 {len(training_data)}개의 훈련 샘플")
    
    print("\n🎯 이제 파인튜닝을 시작할 수 있습니다!")
    print("다음 단계: python fine_tune_with_npc_data.py 실행")

if __name__ == "__main__":
    main()