# 🎮 Adventure Game - AI-Powered Text RPG

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg)](https://pyside.org)
[![AI](https://img.shields.io/badge/AI-Bllossom--3B-orange.svg)](https://huggingface.co/Bllossom/llama-3.2-Korean-Bllossom-3B)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AI 기반 텍스트 RPG 게임**으로, 지능형 NPC와의 대화를 통해 모험을 즐길 수 있는 게임입니다. Bllossom-3B 모델을 활용하여 각 NPC가 개성 있는 대화를 제공합니다.

## ✨ 주요 기능

### 🎯 게임 핵심 기능
- **캐릭터 생성 및 관리**: 플레이어 생성, 저장, 로드 시스템
- **인벤토리 시스템**: 아이템 관리, 장비 착용/해제
- **스텟 시스템**: STR, AGI, INT, LUCK 기반 캐릭터 성장
- **장비 시스템**: 투구, 갑옷, 무기, 반지 등 다양한 장비
- **퀘스트 시스템**: CSV 기반 퀘스트 관리

### 🤖 AI 시스템 (AI2)
- **지능형 NPC**: 각 NPC별 개성 있는 대화
- **실시간 대화**: 플레이어와 NPC 간 자연스러운 상호작용
- **학습 기반**: NPC 설정 파일을 바탕으로 자동 학습
- **메모리 효율**: LoRA + 8-bit 양자화로 최적화
- **세션 관리**: NPC별 독립적인 대화 세션

## 🏗️ 프로젝트 구조

```
advanture_game/
├── 📁 UI/                          # 사용자 인터페이스
│   ├── main_menu_ui.py            # 메인 메뉴
│   ├── new_game_ui.py             # 새 게임 생성
│   ├── load_game_ui.py            # 게임 로드
│   ├── start_main_ui.py           # 게임 메인 화면
│   ├── inventory_ui.py            # 인벤토리 관리
│   ├── item_view_ui.py            # 아이템 상세보기
│   └── ui_files/                  # UI 디자인 파일들
│
├── 📁 entity/                      # 게임 엔티티
│   ├── item.py                    # 아이템 클래스
│   ├── armor.py                   # 장비 시스템
│   ├── consum.py                  # 소모품 시스템
│   ├── inventory.py               # 인벤토리 관리
│   └── money.py                   # 화폐 시스템
│
├── 📁 data/                        # 데이터 관리
│   ├── save_load.py               # 저장/로드 시스템
│   ├── item_data.py               # 아이템 데이터 관리
│   ├── quest.py                   # 퀘스트 시스템
│   └── data_files/                # 게임 데이터 파일
│       ├── npc_instruction/       # NPC 설정 파일
│       ├── other_instruction/     # 기타 설정 파일
│       ├── item_datas.item        # 아이템 데이터
│       ├── player_datas.player    # 플레이어 데이터
│       └── quest.csv              # 퀘스트 데이터
│
├── 📁 ai2/                         # AI 시스템 (신규)
│   ├── __init__.py                # 모듈 초기화
│   ├── data_processor.py          # 학습 데이터 생성
│   ├── fine_tuner.py              # AI 모델 파인튜닝
│   ├── session_manager.py         # NPC 세션 관리
│   ├── ai_bridge.py               # GUI-AI 연결
│   ├── main.py                    # AI 시스템 실행
│   ├── updated_start_main_ui.py   # AI 통합 GUI
│   ├── README.md                  # AI 시스템 가이드
│   └── requirements.txt           # AI 의존성
│
├── 📁 functions/                   # 유틸리티 함수
│   └── show_inventory_items.py    # 인벤토리 표시
│
├── 📁 ai/                          # 기존 AI 시스템
│   ├── brain_chat.py              # 채팅 기능
│   ├── god_brain.py               # 신 NPC AI
│   ├── fine_tune.py               # 파인튜닝
│   └── ...                        # 기타 AI 파일들
│
├── 📁 workspace/                   # AI 작업 공간
├── 📁 develop_logs/                # 개발 로그
├── 📁 unit/                        # 단위 테스트
├── main.py                        # 게임 메인 실행 파일
├── pyproject.toml                 # 프로젝트 설정
└── README.md                      # 이 파일
```

## 🚀 설치 및 실행

### 1. 기본 요구사항
- Python 3.11+
- CUDA GPU (AI 기능 사용 시)
- 8GB+ RAM (AI 기능 사용 시)

### 2. 의존성 설치

```bash
# 기본 게임 의존성
pip install pyside6 pandas

# AI 기능 사용 시 추가 설치
cd ai2
pip install -r requirements.txt
```

### 3. 게임 실행

```bash
# 기본 게임 실행
python main.py

# AI 시스템 설정 (처음 실행 시)
cd ai2
python main.py --action setup
```

## 🎮 게임 플레이 가이드

### 캐릭터 생성
1. **새 게임** 선택
2. 캐릭터 이름 입력
3. 초기 스텟 설정

### 게임 시스템
- **인벤토리**: 아이템 관리 및 장비 착용/해제
- **스탯**: STR(힘), AGI(민첩), INT(지능), LUCK(운)
- **장비**: 투구, 갑옷, 바지, 신발, 목걸이, 반지, 무기
- **NPC 대화**: AI 기반 지능형 대화 시스템

### AI NPC와의 대화
- **신 NPC**: 캐릭터 직업 및 스킬 부여
- **상황별 대화**: 게임 진행에 따른 동적 대화
- **개성 있는 응답**: 각 NPC의 설정에 맞는 일관된 성격

## 🔧 AI 시스템 설정

### 빠른 설정
```bash
cd ai2
python main.py --action setup
```

### 단계별 설정
```bash
# 1. 학습 데이터 생성
python main.py --action data

# 2. 모델 학습
python main.py --action train --epochs 3

# 3. 시스템 테스트
python main.py --action test
```

### GUI에 AI 통합
```bash
# 기존 UI 백업
cp UI/start_main_ui.py UI/start_main_ui.py.backup

# AI 통합 UI로 교체
cp ai2/updated_start_main_ui.py UI/start_main_ui.py
```

## 📝 NPC 추가 방법

### 새로운 NPC 설정 파일 생성
`data/data_files/npc_instruction/npc_새캐릭터.txt`:

```
<NPC: 새캐릭터
이름: 새캐릭터 이름
직업: 직업
성별: 성별
성격: 성격 특성
역할: 게임 내 역할
설명: 상세한 캐릭터 설명
>
```

### 학습 데이터 재생성
```bash
cd ai2
python main.py --action data
python main.py --action train
```

## 🔍 주요 클래스 및 모듈

### UI 시스템
- `MainWindow`: 메인 애플리케이션 창
- `StartMainWindow`: 게임 메인 화면
- `NewGameWindow`: 새 게임 생성
- `LoadGameWindow`: 게임 로드

### 게임 시스템
- `Item`: 아이템 관리
- `Armor`: 장비 착용/해제 시스템
- `Player_SAVELOAD`: 플레이어 데이터 저장/로드

### AI 시스템
- `NPCSessionManager`: NPC 세션 관리
- `GameAIController`: GUI-AI 통합 컨트롤러
- `NPCDataProcessor`: 학습 데이터 자동 생성

## 🛠️ 개발 환경

### 권장 개발 도구
- **IDE**: VSCode, PyCharm
- **Python**: 3.11+
- **Qt Designer**: UI 디자인 (선택사항)

### 디버깅 및 테스트
```bash
# 게임 기본 기능 테스트
python main.py

# AI 시스템 테스트
cd ai2
python main.py --action test

# 특정 NPC 대화 테스트
python -c "from ai2 import GameAIController; ..."
```

## 🔮 향후 개발 계획

### 게임 기능 확장
- [ ] 전투 시스템 구현
- [ ] 퀘스트 시스템 확장
- [ ] 다양한 던전 및 맵
- [ ] 멀티플레이어 지원

### AI 시스템 개선
- [ ] 더 많은 NPC 타입 추가
- [ ] 감정 상태 시스템
- [ ] 음성 인식/합성 연동
- [ ] 플레이어 행동 학습 시스템

### 기술적 개선
- [ ] 성능 최적화
- [ ] 모바일 지원
- [ ] 클라우드 저장
- [ ] 실시간 업데이트

## 📊 성능 및 시스템 요구사항

### 최소 요구사항 (기본 게임)
- **OS**: Windows 10, macOS 10.15, Ubuntu 18.04+
- **RAM**: 4GB
- **Storage**: 1GB

### 권장 요구사항 (AI 기능 포함)
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **RAM**: 16GB+
- **GPU**: NVIDIA GTX 1060 6GB+ (CUDA 지원)
- **Storage**: 10GB+

## 🤝 기여하기

프로젝트에 기여하고 싶으시다면:

1. 이 저장소를 Fork
2. 새로운 브랜치 생성 (`git checkout -b feature/새기능`)
3. 변경사항 커밋 (`git commit -am '새기능 추가'`)
4. 브랜치에 Push (`git push origin feature/새기능`)
5. Pull Request 생성

## 📜 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원 및 문의

- **이슈 리포트**: GitHub Issues 탭 활용
- **기능 제안**: GitHub Discussions 활용
- **문서**: 각 모듈의 README 파일 참조

---

**Made with ❤️ by Adventure Game Team**

*"AI와 함께하는 새로운 모험의 시작"*
