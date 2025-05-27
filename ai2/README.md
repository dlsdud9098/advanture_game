# AI2 - NPC AI 시스템

게임 내 NPC와의 지능적인 대화를 위한 AI 시스템입니다. Bllossom-3B 모델을 기반으로 하여 각 NPC별 개성과 설정에 맞는 대화를 생성합니다.

## 🚀 주요 기능

- **NPC별 개별 세션 관리**: 각 NPC마다 독립적인 대화 세션
- **설정 기반 학습**: NPC 설정 파일을 바탕으로 자동 학습 데이터 생성
- **효율적인 파인튜닝**: LoRA를 활용한 메모리 효율적인 학습
- **GUI 통합**: PySide6 GUI와 완전 통합
- **실시간 대화**: 플레이어와 NPC 간 자연스러운 실시간 대화

## 📁 폴더 구조

```
ai2/
├── __init__.py              # 모듈 초기화 및 편의 함수
├── data_processor.py        # 데이터 전처리 및 학습 데이터 생성
├── fine_tuner.py           # 파인튜닝 트레이너
├── session_manager.py      # NPC 세션 관리자
├── ai_bridge.py           # GUI-AI 연결 브릿지
├── updated_start_main_ui.py # 업데이트된 GUI 파일
├── main.py                # 메인 실행 스크립트
├── requirements.txt       # 필요 라이브러리
├── README.md             # 이 파일
└── data/                 # 생성되는 데이터 폴더
    ├── training_dataset.json
    └── formatted_dataset.txt
```

## 🛠️ 설치 및 설정

### 1. 필요 라이브러리 설치

```bash
cd /home/apic/python/advanture_game/ai2
pip install -r requirements.txt
```

### 2. 빠른 설정 (권장)

```bash
# 모든 단계를 자동으로 실행
python main.py --action setup
```

### 3. 단계별 설정

```bash
# 1단계: 학습 데이터 생성
python main.py --action data

# 2단계: 모델 학습 (3 에포크)
python main.py --action train --epochs 3

# 3단계: AI 시스템 테스트
python main.py --action test
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

# 메시지 전송
response = controller.send_player_message("안녕하세요!")
print(f"신: {response}")

# 정리
controller.cleanup()
```

### GUI에서 사용

기존 `UI/start_main_ui.py` 파일을 `ai2/updated_start_main_ui.py`로 교체하면 자동으로 AI 시스템이 통합됩니다.

```python
# UI/start_main_ui.py 파일을 백업하고 새 파일로 교체
cp UI/start_main_ui.py UI/start_main_ui.py.backup
cp ai2/updated_start_main_ui.py UI/start_main_ui.py
```

## ⚙️ 설정 파일

### NPC 설정 추가

새로운 NPC를 추가하려면 `data/data_files/npc_instruction/` 폴더에 새 텍스트 파일을 생성하세요.

예시: `data/data_files/npc_instruction/npc_merchant.txt`

```
<NPC: merchant
이름: 상인 김
직업: 상인
성별: 남성
성격: 친근함, 장사꾼
역할: 아이템 판매, 정보 제공
설명: 다양한 아이템을 판매하는 상인입니다. 항상 밝은 표정으로 손님을 맞이합니다.
>
```

### 상황 설정 추가

게임 상황을 추가하려면 `data/data_files/other_instruction/` 폴더에 텍스트 파일을 추가하세요.

## 🔧 고급 설정

### 학습 파라미터 조정

`fine_tuner.py`에서 학습 파라미터를 조정할 수 있습니다:

```python
# LoRA 설정
r=8,                    # LoRA rank
lora_alpha=32,         # LoRA alpha
lora_dropout=0.1,      # LoRA dropout

# 학습 설정
num_epochs=3,          # 에포크 수
batch_size=1,          # 배치 크기
learning_rate=2e-4,    # 학습률
```

### 메모리 최적화

GPU 메모리가 부족한 경우:

1. `batch_size`를 1로 설정 (이미 기본값)
2. `gradient_accumulation_steps`를 늘려서 효과적인 배치 크기 증가
3. 8-bit 양자화 사용 (이미 활성화됨)

## 🐛 문제 해결

### 1. CUDA 메모리 부족

```bash
# GPU 메모리 정리
python -c "import torch; torch.cuda.empty_cache()"
```

### 2. 모델 로드 실패

모델 경로와 파일이 올바른지 확인:

```bash
ls -la workspace/npc_model/
```

### 3. 학습 데이터 문제

데이터 파일 형식 확인:

```bash
python -c "
from ai2.data_processor import NPCDataProcessor
processor = NPCDataProcessor()
data = processor.read_npc_files()
print(data.keys())
"
```

### 4. AI 응답이 이상한 경우

- 학습 데이터를 다시 생성하고 재학습
- 더 많은 에포크로 학습
- NPC 설정 파일의 내용 검토

## 📊 성능 모니터링

학습 진행 상황을 모니터링하려면:

```python
# 학습 로그 확인
tail -f ai2/ai_system.log

# GPU 사용량 모니터링
nvidia-smi -l 1
```

## 🔄 업데이트 및 유지보수

### 새 NPC 추가 후 재학습

1. 새 NPC 설정 파일 추가
2. 학습 데이터 재생성: `python main.py --action data`
3. 모델 재학습: `python main.py --action train`

### 모델 성능 개선

1. 더 많은 대화 예시 추가
2. 에포크 수 증가
3. 학습률 조정

## 📞 지원

문제가 발생하면 다음을 확인하세요:

1. 로그 파일: `ai2/ai_system.log`
2. GPU 메모리 상태: `nvidia-smi`
3. Python 환경: 필요 라이브러리 설치 상태

## 🚀 향후 개선 사항

- [ ] 더 많은 NPC 타입 지원
- [ ] 음성 인식/합성 연동
- [ ] 감정 상태 시스템
- [ ] 멀티턴 퀘스트 대화
- [ ] 플레이어 행동 기반 NPC 반응 변화

---

**참고**: 이 시스템은 Bllossom-3B 모델을 기반으로 하며, 적절한 GPU 환경에서 최적의 성능을 발휘합니다.
