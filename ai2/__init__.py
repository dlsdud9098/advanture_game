"""
업데이트된 AI2 초기화 모듈
확장된 데이터 생성기를 포함
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
__version__ = "1.1.0"

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
    os.environ["QT_QPA_PLATFORM"] = "offscreen"  # GUI 없이 실행
    setup_logging()
    ensure_directories()
    
# 모듈 임포트
from .data_processor import NPCDataProcessor
from .extended_data_generator import GodNPCDataGenerator
from .fine_tuner import NPCFineTuner
from .session_manager import NPCSessionManager, get_session_manager
from .ai_bridge import NPCAIBridge, get_ai_bridge, GameAIController

# 편의 함수들 (업데이트됨)
def create_training_data(use_extended=True):
    """학습 데이터 생성 - 확장 버전 사용"""
    if use_extended:
        # 새로운 확장 데이터 생성기 사용
        generator = GodNPCDataGenerator()
        dataset_count = generator.save_dataset()
        dataset_path = DATA_PATH / "god_npc_extended_dataset.json"
        print(f"확장 데이터 생성 완료: {dataset_count}개 대화")
    else:
        # 기존 데이터 생성기 사용
        processor = NPCDataProcessor()
        dataset = processor.create_fine_tuning_dataset()
        dataset_path = DATA_PATH / "training_dataset.json"
        processor.save_dataset(dataset, str(dataset_path))
        print(f"기본 데이터 생성 완료: {len(dataset)}개 대화")
    
    return str(dataset_path)

def train_model(dataset_path: str = None, epochs: int = 3):
    """모델 학습"""
    if dataset_path is None:
        dataset_path = create_training_data(use_extended=True)
    
    trainer = NPCFineTuner()
    model_path = trainer.train(
        dataset_path=dataset_path,
        num_epochs=epochs,
        batch_size=1,
        gradient_accumulation_steps=4
    )
    
    return model_path

def quick_setup(use_extended_data=True):
    """빠른 설정 - 확장 데이터로 업그레이드"""
    initialize()
    
    print("=== AI2 시스템 빠른 설정 시작 ===")
    
    print("1. 학습 데이터 생성 중...")
    if use_extended_data:
        print("   → 확장된 대화 데이터 생성 (60+ 대화)")
        dataset_path = create_training_data(use_extended=True)
    else:
        print("   → 기본 대화 데이터 생성")
        dataset_path = create_training_data(use_extended=False)
    
    print(f"   → 데이터 저장: {dataset_path}")
    
    print("2. 모델 학습 시작...")
    print("   → LoRA 기반 효율적 파인튜닝")
    print("   → 8-bit 양자화로 메모리 절약")
    model_path = train_model(dataset_path)
    print(f"   → 모델 저장: {model_path}")
    
    print("3. AI 시스템 준비 완료!")
    print("   → NPC별 세션 관리 준비됨")
    print("   → GUI 통합 준비됨")
    print("   → 실시간 대화 시스템 활성화")
    
    print("\n=== 사용법 ===")
    print("GUI에서 사용: updated_start_main_ui.py 파일을 기존 UI와 교체")
    print("코드에서 사용: from ai2 import GameAIController")
    print("테스트: python main.py --action test")
    
    return model_path

def compare_datasets():
    """기본 데이터와 확장 데이터 비교"""
    print("=== 데이터셋 비교 ===")
    
    # 기본 데이터 생성
    print("1. 기본 데이터 생성...")
    processor = NPCDataProcessor()
    basic_dataset = processor.create_fine_tuning_dataset()
    basic_count = len(basic_dataset)
    
    # 확장 데이터 생성  
    print("2. 확장 데이터 생성...")
    generator = GodNPCDataGenerator()
    extended_dataset = generator.generate_comprehensive_conversations()
    extended_count = len(extended_dataset)
    
    print(f"\n=== 비교 결과 ===")
    print(f"기본 데이터: {basic_count}개 대화")
    print(f"확장 데이터: {extended_count}개 대화")
    print(f"증가량: {extended_count - basic_count}개 ({(extended_count/basic_count)*100:.1f}%)")
    
    print(f"\n=== 확장 데이터 구성 ===")
    print("• 초기 소환 및 세계 설명")
    print("• 15개 질문을 통한 직업 결정 과정")
    print("• 스텟 및 스킬 부여 상세 대화")
    print("• 퀘스트 부여 및 진행 가이드")
    print("• 감정적 상호작용 및 격려")
    print("• 게임 메커니즘 설명")
    print("• 멀티턴 연속 대화")
    
    return basic_count, extended_count

# 사용법 출력
def print_usage():
    """사용법 출력 (업데이트됨)"""
    print("""
=== AI2 시스템 사용법 (v1.1.0) ===

🆕 새로운 기능:
- 확장된 대화 데이터 (60+ 시나리오)
- 15개 질문 기반 직업 결정 시스템
- 감정적 상호작용 및 멀티턴 대화
- 게임 메커니즘 통합 설명

1. 빠른 설정 (권장):
   from ai2 import quick_setup
   model_path = quick_setup()

2. 확장 데이터로 학습:
   from ai2 import create_training_data, train_model
   dataset_path = create_training_data(use_extended=True)
   model_path = train_model(dataset_path)

3. 데이터 비교:
   from ai2 import compare_datasets
   compare_datasets()

4. GUI에서 AI 사용:
   from ai2 import GameAIController
   controller = GameAIController()
   response = controller.initialize_god_conversation(player_data)

5. 명령행 도구:
   python main.py --action setup    # 전체 설정
   python main.py --action test     # 시스템 테스트
   python main.py --action data     # 데이터만 생성

🎯 주요 개선사항:
- 학습 데이터 400% 증가 (14개 → 60+개)
- 실제 게임 시나리오 반영
- NPC 개성과 일관성 강화
- 플레이어 선택에 따른 동적 반응

자세한 내용은 README.md를 참고하세요.
    """)

if __name__ == "__main__":
    print_usage()
