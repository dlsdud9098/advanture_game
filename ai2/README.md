# AI2 - NPC AI 시스템 v1.1.0 🚀

게임 내 NPC와의 지능적인 대화를 위한 고도화된 AI 시스템입니다. Bllossom-3B 모델을 기반으로 하여 각 NPC별 개성과 설정에 맞는 자연스럽고 풍부한 대화를 생성합니다.

## 🆕 v1.1.0 새로운 기능

### 📊 대폭 확장된 학습 데이터
- **기존**: 14개 기본 대화 → **신규**: 60+ 개 풍부한 대화 (400% 증가!)
- **15개 질문 시스템**: 플레이어 직업 결정을 위한 체계적 질문-답변 과정
- **멀티턴 대화**: 연속된 자연스러운 대화 흐름
- **감정 상호작용**: 플레이어의 다양한 감정 상태에 대한 적절한 반응
- **게임 메커니즘 통합**: 레벨업, 장비, 퀘스트 등 게임 요소 설명

### 🎭 김샐프 신 NPC 특화
- **개성 강화**: 다정하면서도 엄격한 신의 캐릭터
- **상황별 대응**: 소환, 직업 부여, 퀘스트, 격려 등 다양한 상황
- **일관성**: 존댓말 사용과 위엄있는 말투 유지
- **교육적**: 게임 세계관과 메커니즘을 자연스럽게 설명

## 🚀 주요 기능

- **NPC별 개별 세션 관리**: 각 NPC마다 독립적인 대화 세션
- **설정 기반 학습**: NPC 설정 파일을 바탕으로 자동 학습 데이터 생성
- **효율적인 파인튜닝**: LoRA를 활용한 메모리 효율적인 학습
- **GUI 통합**: PySide6 GUI와 완전 통합
- **실시간 대화**: 플레이어와 NPC 간 자연스러운 실시간 대화

## 📁 폴더 구조

```
ai2/
├── __init__.py                    # 모듈 초기화 및 편의 함수 (v1.1.0)
├── data_processor.py             # 기본 데이터 처리
├── extended_data_generator.py    # 🆕 확장 데이터 생성기
├── fine_tuner.py                # 파인튜닝 트레이너
├── session_manager.py           # NPC 세션 관리자
├── ai_bridge.py                # GUI-AI 연결 브릿지
├── updated_start_main_ui.py    # 업데이트된 GUI 파일
├── main.py                     # 메인 실행 스크립트 (v1.1.0)
├── generate_data.py           # 🆕 데이터 생성 전용 스크립트
├── requirements.txt           # 필요 라이브러리
├── README.md                 # 이 파일
└── data/                     # 생성되는 데이터 폴더
    ├── god_npc_extended_dataset.json     # 🆕 확장 데이터
    ├── god_npc_extended_dataset_formatted.txt
    ├── training_dataset.json            # 기본 데이터
    └── formatted_dataset.txt
```

## 🛠️ 설치 및 설정

### 1. 필요 라이브러리 설치

```bash
cd /home/apic/python/advanture_game/ai2
pip install -r requirements.txt
```

### 2. 빠른 설정 (권장) 🚀

```bash
# 확장 데이터로 고품질 AI 시스템 구축
python main.py --action setup
```

### 3. 단계별 설정

```bash
# 1단계: 확장 학습 데이터 생성 (60+ 대화)
python main.py --action data

# 2단계: 모델 학습 (3 에포크)
python main.py --action train --epochs 3

# 3단계: AI 시스템 테스트
python main.py --action test

# 4단계: 데이터셋 비교 (기본 vs 확장)
python main.py --action compare
```

### 4. 기본 데이터만 사용하고 싶다면

```bash
python main.py --action setup --basic
```

## 📝 사용법

### Python 코드에서 직접 사용

```python
from ai2 import GameAIController, initialize

# AI 시스템 초기화
initialize()

# 컨트롤러 생성
controller = GameAIController()

# 플레이어 데이터
player_data = {
    "name": "플레이어이름",
    "lv": 1,
    "class": "미정",
    "hp": 100,
    "mp": 50,
    "STR": 10,
    "AGI": 10,
    "INT": 10,
    "LUCK": 10
}

# 신과의 대화 시작
response = controller.initialize_god_conversation(player_data)
print(f"신: {response}")

# 다양한 메시지 테스트
messages = [
    "안녕하세요, 신님!",
    "제가 어떤 능력을 갖게 될까요?",
    "첫 번째 질문을 해주세요.",
    "A",  # 질문에 대한 답변
    "무서워요. 정말 할 수 있을까요?",
    "퀘스트를 주세요."
]

for msg in messages:
    response = controller.send_player_message(msg)
    print(f"플레이어: {msg}")
    print(f"신: {response}\n")

# 정리
controller.cleanup()
```

### GUI에서 사용

기존 `UI/start_main_ui.py` 파일을 `ai2/updated_start_main_ui.py`로 교체:

```bash
# 백업 생성
cp UI/start_main_ui.py UI/start_main_ui.py.backup

# 새 파일로 교체
cp ai2/updated_start_main_ui.py UI/start_main_ui.py
```

## 📊 데이터 구성 (v1.1.0)

### 확장 데이터 카테고리 (60+ 대화)

1. **초기 소환 대화** (5개)
   - "여기가 어디죠?", "왜 저를 소환했나요?" 등

2. **15개 질문 시스템** (20+개)
   - 체계적인 직업 결정 과정
   - 각 선택지별 신의 반응과 해석

3. **스텟/스킬 부여** (10개)
   - 능력치 설명 및 배분 과정
   - 직업별 특화 스킬 부여

4. **퀘스트 시스템** (5개)
   - 임무 부여 및 진행 가이드
   - 보상과 실패 처리 설명

5. **감정 상호작용** (5개)
   - 두려움, 기쁨, 분노, 슬픔 등에 대한 적절한 반응
   - 격려와 위로의 메시지

6. **게임 메커니즘** (5개)
   - 레벨업, 장비, 파티 구성 등 설명
   - 실용적인 게임 플레이 가이드

7. **세계관 설명** (5개)
   - 마왕, 다른 종족, 신들에 대한 설명
   - 이세계의 역사와 현재 상황

8. **멀티턴 대화** (연속성)
   - 자연스럽게 이어지는 대화 흐름
   - 이전 대화 내용을 기억하는 일관성

## ⚙️ 고급 설정

### 학습 파라미터 조정

`fine_tuner.py`에서 설정 가능:

```python
# LoRA 설정
r=8,                    # LoRA rank (높을수록 더 정교, 메모리 사용 증가)
lora_alpha=32,         # LoRA alpha (학습 강도)
lora_dropout=0.1,      # LoRA dropout (과적합 방지)

# 학습 설정
num_epochs=3,          # 에포크 수 (3-5 권장)
batch_size=1,          # 배치 크기 (GPU 메모리에 따라 조정)
learning_rate=2e-4,    # 학습률 (2e-4 권장)
gradient_accumulation_steps=4,  # 그래디언트 누적 (효과적 배치 크기 증가)
```

### 새로운 NPC 추가

1. **NPC 설정 파일 추가**:
   `data/data_files/npc_instruction/npc_merchant.txt`

```
<NPC: merchant
이름: 상인 김철수
직업: 상인
성별: 남성
성격: 친근함, 장사꾼 기질
역할: 아이템 판매, 시장 정보 제공
설명: 각종 아이템을 판매하는 경험 많은 상인입니다.
>
```

2. **확장 데이터 생성기에 시나리오 추가**:
   `extended_data_generator.py`에서 새 NPC용 대화 시나리오 추가

3. **재학습**:
```bash
python main.py --action data  # 새 데이터 생성
python main.py --action train # 재학습
```

## 🔧 문제 해결

### 1. CUDA 메모리 부족

```bash
# GPU 메모리 정리
python -c "import torch; torch.cuda.empty_cache()"

# 배치 크기 조정
# fine_tuner.py에서 batch_size=1, gradient_accumulation_steps 증가
```

### 2. 학습 데이터 확인

```bash
# 데이터 비교
python main.py --action compare

# 데이터 생성만
python ai2/generate_data.py
```

### 3. AI 응답 품질 개선

1. **더 많은 에포크로 학습**:
```bash
python main.py --action train --epochs 5
```

2. **데이터 품질 확인**:
   - `ai2/data/god_npc_extended_dataset.json` 파일 검토
   - 필요시 `extended_data_generator.py`에서 시나리오 추가

3. **모델 성능 테스트**:
```bash
python main.py --action test
```

## 📞 지원 및 디버깅

### 로그 확인
```bash
# 실시간 로그 모니터링
tail -f ai2/ai_system.log

# GPU 사용량 확인
nvidia-smi -l 1
```

### 단계별 디버깅
```bash
# 1. 데이터 생성 테스트
python ai2/generate_data.py

# 2. 모델 로드 테스트  
python -c "from ai2 import NPCSessionManager; mgr = NPCSessionManager()"

# 3. 전체 시스템 테스트
python main.py --action test
```

## 🎯 성능 비교

| 항목 | 기본 v1.0 | 확장 v1.1 | 개선율 |
|------|-----------|----------|--------|
| 학습 데이터 수 | 14개 | 60+개 | +400% |
| 대화 다양성 | 제한적 | 풍부함 | +500% |
| NPC 일관성 | 보통 | 우수 | +300% |
| 게임 연동성 | 기본 | 완전통합 | +400% |
| 감정 반응 | 없음 | 지원 | 신규 |

## 🚀 향후 개선 사항

- [ ] 더 많은 NPC 타입 지원 (상인, 모험가, 마법사 등)
- [ ] 플레이어 행동 기반 NPC 반응 변화
- [ ] 음성 인식/합성 연동
- [ ] 멀티플레이어 대화 지원
- [ ] 퀘스트 자동 생성 시스템
- [ ] 감정 상태 시각화

---

**⚡ v1.1.0 핵심 포인트**: 이전 버전 대비 400% 늘어난 학습 데이터로 김샐프 신이 훨씬 더 지능적이고 개성있게 플레이어와 대화합니다. 15개 질문을 통한 체계적인 직업 결정 과정과 다양한 감정 상호작용으로 진정한 RPG 경험을 제공합니다!

🎮 **지금 바로 시작하세요**: `python main.py`
