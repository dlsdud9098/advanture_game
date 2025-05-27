# AI2 시스템을 Git에 커밋하는 방법

다음 명령어들을 터미널에서 순서대로 실행해주세요:

## 1. 프로젝트 폴더로 이동
```bash
cd /home/apic/python/advanture_game
```

## 2. Git 상태 확인
```bash
git status
```

## 3. AI2 시스템 파일들을 Git에 추가
```bash
git add ai2/
```

## 4. 변경사항 확인
```bash
git status
```

## 5. 커밋 실행
```bash
git commit -m "feat: Add AI2 NPC AI System

- Implemented comprehensive NPC AI system with Bllossom-3B model
- Added data processor for automatic training data generation  
- Created fine-tuner with LoRA for memory-efficient training
- Implemented session manager for individual NPC conversations
- Added AI bridge for GUI integration
- Created updated main UI with AI integration
- Added comprehensive documentation and usage guide

Features:
- NPC-specific conversation sessions
- Automatic training data generation from config files
- Memory-efficient fine-tuning with LoRA and 8-bit quantization
- Real-time conversation with intelligent NPCs
- Seamless GUI integration
- Comprehensive error handling and logging

Files added:
- ai2/__init__.py: Module initialization and utility functions
- ai2/data_processor.py: Data processing and dataset generation
- ai2/fine_tuner.py: Fine-tuning trainer with LoRA
- ai2/session_manager.py: NPC session management
- ai2/ai_bridge.py: GUI-AI integration bridge
- ai2/main.py: Main execution script
- ai2/updated_start_main_ui.py: Updated GUI with AI integration
- ai2/README.md: Comprehensive documentation
- ai2/requirements.txt: Required dependencies"
```

## 6. 원격 저장소에 푸시 (필요한 경우)
```bash
git push origin main
```

또는 원격 저장소의 기본 브랜치 이름이 다르다면:
```bash
git push origin master
```

## 📝 추가 정보

### 커밋된 파일 목록:
- `ai2/__init__.py` - 모듈 초기화 및 편의 함수
- `ai2/data_processor.py` - 데이터 처리 및 학습 데이터 생성
- `ai2/fine_tuner.py` - LoRA 기반 파인튜닝 트레이너
- `ai2/session_manager.py` - NPC 세션 관리자
- `ai2/ai_bridge.py` - GUI-AI 연결 브릿지
- `ai2/main.py` - 메인 실행 스크립트
- `ai2/updated_start_main_ui.py` - AI 통합 GUI
- `ai2/README.md` - 상세 사용법 가이드
- `ai2/requirements.txt` - 필요 라이브러리 목록
- `ai2/data/` - 데이터 저장 폴더

### 만약 오류가 발생한다면:
1. Git 설정 확인: `git config --list`
2. 원격 저장소 확인: `git remote -v`
3. 브랜치 확인: `git branch`
