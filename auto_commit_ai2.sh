#!/bin/bash

# AI2 시스템 자동 커밋 스크립트
cd /home/apic/python/advanture_game

echo "=== AI2 시스템 Git 커밋 시작 ==="

# Git 상태 확인
echo "현재 Git 상태:"
git status

# AI2 폴더 추가
echo "AI2 시스템 파일들을 Git에 추가..."
git add ai2/

# 추가된 파일 확인  
echo "추가된 파일들:"
git diff --cached --name-only

# 커밋 실행
echo "커밋 실행 중..."
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

echo "✅ AI2 시스템 커밋 완료!"
echo "최근 커밋:"
git log --oneline -1

echo ""
echo "GitHub에 푸시하려면:"
echo "git push origin main"
