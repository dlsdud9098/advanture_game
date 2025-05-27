"""
학습 및 테스트를 위한 메인 실행 스크립트
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
    parser = argparse.ArgumentParser(description='NPC AI 시스템 관리')
    parser.add_argument('--action', choices=['train', 'test', 'data', 'setup'], 
                       default='setup', help='수행할 작업')
    parser.add_argument('--epochs', type=int, default=3, help='학습 에포크 수')
    parser.add_argument('--model-path', type=str, help='모델 경로')
    
    args = parser.parse_args()
    
    if args.action == 'data':
        print("=== 학습 데이터 생성 ===")
        dataset_path = create_training_data()
        print(f"완료: {dataset_path}")
        
    elif args.action == 'train':
        print("=== 모델 학습 ===")
        model_path = train_model(epochs=args.epochs)
        print(f"완료: {model_path}")
        
    elif args.action == 'test':
        print("=== AI 시스템 테스트 ===")
        test_ai_system(args.model_path)
        
    elif args.action == 'setup':
        print("=== 전체 설정 ===")
        model_path = quick_setup()
        print(f"설정 완료: {model_path}")

def test_ai_system(model_path=None):
    """AI 시스템 테스트"""
    try:
        initialize()
        
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
        
        # 대화 테스트
        test_messages = [
            "안녕하세요, 신님!",
            "여기가 어디인가요?",
            "제가 왜 소환되었나요?",
            "저에게 힘을 주실 수 있나요?"
        ]
        
        for msg in test_messages:
            print(f"\n플레이어: {msg}")
            response = controller.send_player_message(msg)
            print(f"신: {response}")
        
        print("\n테스트 완료!")
        
        # 정리
        controller.cleanup()
        
    except Exception as e:
        print(f"테스트 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
