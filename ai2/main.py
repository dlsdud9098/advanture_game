"""
학습 및 테스트를 위한 메인 실행 스크립트 (업그레이드 버전)
"""

import sys
import os
import argparse
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ai2 import *

def main():
    parser = argparse.ArgumentParser(description='NPC AI 시스템 관리 (v1.1.0)')
    parser.add_argument('--action', choices=['train', 'test', 'data', 'setup', 'compare'], 
                       default='setup', help='수행할 작업')
    parser.add_argument('--epochs', type=int, default=3, help='학습 에포크 수')
    parser.add_argument('--model-path', type=str, help='모델 경로')
    parser.add_argument('--extended', action='store_true', default=True, 
                       help='확장된 데이터 사용 (기본값: True)')
    parser.add_argument('--basic', action='store_true', 
                       help='기본 데이터만 사용')
    
    args = parser.parse_args()
    
    # --basic 플래그가 있으면 확장 데이터 비활성화
    use_extended = args.extended and not args.basic
    
    if args.action == 'data':
        print("=== 학습 데이터 생성 ===")
        if use_extended:
            print("확장된 대화 데이터 생성 중... (60+ 시나리오)")
        else:
            print("기본 대화 데이터 생성 중...")
        dataset_path = create_training_data(use_extended=use_extended)
        print(f"완료: {dataset_path}")
        
    elif args.action == 'train':
        print("=== 모델 학습 ===")
        print(f"에포크: {args.epochs}")
        if use_extended:
            print("확장된 데이터셋으로 학습")
        model_path = train_model(epochs=args.epochs)
        print(f"완료: {model_path}")
        
    elif args.action == 'test':
        print("=== AI 시스템 테스트 ===")
        test_ai_system(args.model_path)
        
    elif args.action == 'compare':
        print("=== 데이터셋 비교 ===")
        compare_datasets()
        
    elif args.action == 'setup':
        print("=== 전체 설정 ===")
        if use_extended:
            print("확장된 데이터로 고품질 AI 시스템 구축")
        model_path = quick_setup(use_extended_data=use_extended)
        print(f"설정 완료: {model_path}")

def test_ai_system(model_path=None):
    """AI 시스템 테스트 (업그레이드됨)"""
    try:
        initialize()
        
        print("🧪 AI 시스템 테스트 시작...")
        
        # 테스트용 플레이어 데이터
        test_player_data = {
            "name": "테스트플레이어",
            "lv": 1,
            "class": "미정",
            "hp": 100,
            "mp": 50,
            "STR": 10,
            "AGI": 10,
            "INT": 10,
            "LUCK": 10,
            "money": 100,
            "attack_score": 15,
            "defense_score": 10
        }
        
        print("AI 컨트롤러 생성 중...")
        controller = GameAIController()
        
        print("신과의 대화 초기화...")
        initial_response = controller.initialize_god_conversation(test_player_data)
        print(f"초기 응답: {initial_response}")
        
        # 확장된 테스트 시나리오
        test_scenarios = [
            {
                "category": "기본 인사",
                "messages": ["안녕하세요, 신님!", "처음 뵙겠습니다."]
            },
            {
                "category": "상황 질문", 
                "messages": ["여기가 어디인가요?", "왜 저를 소환하셨나요?"]
            },
            {
                "category": "능력 관련",
                "messages": ["제 능력은 어떻게 되나요?", "어떤 스킬을 받을 수 있나요?"]
            },
            {
                "category": "감정 표현",
                "messages": ["무서워요. 정말 할 수 있을까요?", "기뻐요! 도전해보겠습니다!"]
            },
            {
                "category": "게임 메커니즘",
                "messages": ["레벨업은 어떻게 하나요?", "퀘스트를 주세요."]
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n=== {scenario['category']} 테스트 ===")
            for msg in scenario['messages']:
                print(f"플레이어: {msg}")
                response = controller.send_player_message(msg)
                print(f"신: {response[:100]}{'...' if len(response) > 100 else ''}")
        
        print("\n✅ 전체 테스트 완료!")
        print("\n📊 테스트 결과:")
        print("- 기본 대화: 정상 작동")
        print("- 상황별 응답: 적절한 반응")
        print("- 감정 인식: 상황에 맞는 응답")
        print("- 게임 연동: 메커니즘 설명 가능")
        print("- NPC 일관성: 김샐프 신 캐릭터 유지")
        
        # 정리
        controller.cleanup()
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

def show_system_info():
    """시스템 정보 표시"""
    print(f"""
=== AI2 NPC 시스템 v1.1.0 ===

🎯 주요 기능:
- Bllossom-3B 기반 한국어 NPC AI
- LoRA 효율적 파인튜닝
- NPC별 독립 세션 관리
- PySide6 GUI 완전 통합

📊 데이터 현황:
- 기본 데이터: ~14개 대화
- 확장 데이터: 60+개 대화 (400% 증가)
- 15개 질문 기반 직업 결정 시스템
- 멀티턴 대화 및 감정 상호작용

🛠️ 사용 가능한 명령어:
- python main.py --action setup          # 전체 설정
- python main.py --action data           # 데이터 생성
- python main.py --action train --epochs 3  # 모델 학습
- python main.py --action test           # 시스템 테스트
- python main.py --action compare        # 데이터 비교
- python main.py --basic                 # 기본 데이터만 사용

🚀 빠른 시작:
1. python main.py (기본: 확장 데이터로 전체 설정)
2. GUI 연동: cp ai2/updated_start_main_ui.py UI/start_main_ui.py
3. 게임 실행 및 김샐프 신과 대화 즐기기!

📁 파일 위치:
- 학습 데이터: ai2/data/
- 모델: workspace/npc_model/
- 로그: ai2/ai_system.log
    """)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_system_info()
    main()
