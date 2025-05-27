"""
AI2 모듈 초기화 및 유틸리티 함수들
"""

import os
import logging
from pathlib import Path

# 로깅 설정
def setup_logging(log_level=logging.INFO):
    """로깅 설정"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('/home/apic/python/advanture_game/ai2/ai_system.log')
        ]
    )

# 모듈 버전
__version__ = "1.0.0"

# 기본 경로 설정
BASE_PATH = Path("/home/apic/python/advanture_game")
AI2_PATH = BASE_PATH / "ai2"
DATA_PATH = AI2_PATH / "data"
WORKSPACE_PATH = BASE_PATH / "workspace"

# 필요한 디렉토리 생성
def ensure_directories():
    """필요한 디렉토리들이 존재하는지 확인하고 생성"""
    directories = [
        DATA_PATH,
        WORKSPACE_PATH,
        WORKSPACE_PATH / "cache",
        WORKSPACE_PATH / "models"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# 초기화 함수
def initialize():
    """AI2 시스템 초기화"""
    setup_logging()
    ensure_directories()
    
# 모듈 임포트
from .data_processor import NPCDataProcessor
from .fine_tuner import NPCFineTuner
from .session_manager import NPCSessionManager, get_session_manager
from .ai_bridge import NPCAIBridge, get_ai_bridge, GameAIController

# 편의 함수들
def create_training_data():
    """학습 데이터 생성"""
    processor = NPCDataProcessor()
    dataset = processor.create_fine_tuning_dataset()
    
    # 데이터 저장
    dataset_path = DATA_PATH / "training_dataset.json"
    processor.save_dataset(dataset, str(dataset_path))
    
    return str(dataset_path)

def train_model(dataset_path: str = None, epochs: int = 3):
    """모델 학습"""
    if dataset_path is None:
        dataset_path = create_training_data()
    
    trainer = NPCFineTuner()
    model_path = trainer.train(
        dataset_path=dataset_path,
        num_epochs=epochs,
        batch_size=1,
        gradient_accumulation_steps=4
    )
    
    return model_path

def quick_setup():
    """빠른 설정 - 데이터 생성부터 모델 학습까지"""
    initialize()
    
    print("1. 학습 데이터 생성 중...")
    dataset_path = create_training_data()
    print(f"학습 데이터 저장: {dataset_path}")
    
    print("2. 모델 학습 시작...")
    model_path = train_model(dataset_path)
    print(f"모델 학습 완료: {model_path}")
    
    print("3. AI 시스템 준비 완료!")
    return model_path

# 사용법 출력
def print_usage():
    """사용법 출력"""
    print("""
=== AI2 시스템 사용법 ===

1. 기본 설정:
   from ai2 import initialize
   initialize()

2. 학습 데이터 생성:
   from ai2 import create_training_data
   dataset_path = create_training_data()

3. 모델 학습:
   from ai2 import train_model
   model_path = train_model()

4. GUI에서 AI 사용:
   from ai2 import GameAIController
   controller = GameAIController()
   response = controller.initialize_god_conversation(player_data)

5. 빠른 설정 (모든 단계 자동):
   from ai2 import quick_setup
   model_path = quick_setup()

자세한 사용법은 각 모듈의 문서를 참고하세요.
    """)

if __name__ == "__main__":
    print_usage()
