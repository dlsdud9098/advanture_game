#!/bin/bash

# AI2 시스템 Git 커밋 스크립트

echo "=== AI2 시스템 Git 커밋 시작 ==="

# 프로젝트 루트로 이동
cd /home/apic/python/advanture_game

# Git 상태 확인
echo "현재 Git 상태:"
git status

# AI2 폴더의 모든 파일 추가
echo "AI2 시스템 파일들을 Git에 추가..."
git add ai2/

# 변경사항이 있는지 확인
if git diff --cached --quiet; then
    echo "추가할 변경사항이 없습니다."
    exit 0
fi

# 커밋 메시지 작성 및 커밋
echo "AI2 시스템 커밋 중..."
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

# 커밋 결과 확인
if [ $? -eq 0 ]; then
    echo "✅ AI2 시스템이 성공적으로 커밋되었습니다!"
    echo ""
    echo "최근 커밋 정보:"
    git log --oneline -1
    echo ""
    echo "원격 저장소에 푸시하려면 다음 명령어를 실행하세요:"
    echo "git push origin main"
else
    echo "❌ 커밋 중 오류가 발생했습니다."
    exit 1
fi

echo "=== AI2 시스템 Git 커밋 완료 ==="
