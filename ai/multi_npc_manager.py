import json
import os
from pathlib import Path
import logging
from typing import List, Dict, Optional
from npc_training import NPCTrainer

logger = logging.getLogger(__name__)

class MultiNPCManager:
    """
    여러 NPC를 관리하고 학습시키는 매니저 클래스
    """
    
    def __init__(self, npc_data_dir="./data/data_files/npc_instruction", models_dir="./npc_models"):
        """
        초기화
        
        Args:
            npc_data_dir (str): NPC JSON 파일들이 있는 디렉토리
            models_dir (str): 학습된 모델들을 저장할 디렉토리
        """
        self.npc_data_dir = Path(npc_data_dir)
        self.models_dir = Path(models_dir)
        self.npc_configs = {}
        
        # 디렉토리 생성
        self.npc_data_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        
    def scan_npc_files(self) -> List[str]:
        """
        NPC 데이터 디렉토리에서 JSON 파일들을 스캔
        
        Returns:
            List[str]: 발견된 NPC JSON 파일 경로 리스트
        """
        npc_files = []
        for file_path in self.npc_data_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'npc_id' in data and 'name' in data:
                        npc_files.append(str(file_path))
                        self.npc_configs[data['npc_id']] = {
                            'file_path': str(file_path),
                            'name': data['name'],
                            'description': data.get('description', ''),
                            'personality': data.get('personality', {}),
                            'last_trained': self._get_last_trained_time(data['npc_id'])
                        }
                        logger.info(f"NPC 발견: {data['name']} ({data['npc_id']})")
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"올바르지 않은 NPC 파일: {file_path} - {e}")
                
        return npc_files
    
    def _get_last_trained_time(self, npc_id: str) -> Optional[str]:
        """
        NPC의 마지막 학습 시간 조회
        """
        config_path = self.models_dir / npc_id / "training_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('training_timestamp')
            except:
                pass
        return None
    
    def list_npcs(self) -> Dict:
        """
        발견된 모든 NPC 정보 반환
        """
        self.scan_npc_files()
        return self.npc_configs
    
    def train_single_npc(self, npc_id: str, **training_kwargs) -> bool:
        """
        특정 NPC 학습
        
        Args:
            npc_id (str): 학습할 NPC ID
            **training_kwargs: 학습 파라미터
        """
        if npc_id not in self.npc_configs:
            logger.error(f"NPC '{npc_id}'를 찾을 수 없습니다.")
            return False
        
        npc_file = self.npc_configs[npc_id]['file_path']
        
        try:
            trainer = NPCTrainer()
            
            # NPC 데이터 로드
            if not trainer.load_npc_data(npc_file):
                return False
            
            # 모델 로드
            if not trainer.load_model_and_tokenizer():
                return False
            
            # LoRA 설정
            if not trainer.setup_lora():
                return False
            
            # 기본 학습 파라미터
            default_params = {
                'output_dir': str(self.models_dir),
                'num_train_epochs': 3,
                'per_device_train_batch_size': 1,
                'gradient_accumulation_steps': 8,
                'learning_rate': 2e-4
            }
            default_params.update(training_kwargs)
            
            # 학습 실행
            success = trainer.train(**default_params)
            
            if success:
                trainer.save_training_config(str(self.models_dir))
                logger.info(f"NPC '{npc_id}' 학습 완료")
                
                # 설정 업데이트
                self.npc_configs[npc_id]['last_trained'] = self._get_last_trained_time(npc_id)
            
            return success
            
        except Exception as e:
            logger.error(f"NPC '{npc_id}' 학습 중 오류: {e}")
            return False
    
    def train_all_npcs(self, **training_kwargs) -> Dict[str, bool]:
        """
        모든 NPC 학습
        
        Returns:
            Dict[str, bool]: NPC ID별 학습 성공 여부
        """
        self.scan_npc_files()
        results = {}
        
        for npc_id in self.npc_configs:
            logger.info(f"NPC '{npc_id}' 학습 시작...")
            results[npc_id] = self.train_single_npc(npc_id, **training_kwargs)
        
        # 결과 출력
        successful = sum(results.values())
        total = len(results)
        logger.info(f"학습 완료: {successful}/{total} 성공")
        
        return results
    
    def get_trained_models(self) -> List[str]:
        """
        학습된 모델 목록 조회
        """
        trained_models = []
        for npc_id in self.npc_configs:
            model_path = self.models_dir / npc_id / "final_model"
            if model_path.exists():
                trained_models.append(npc_id)
        
        return trained_models
    
    def create_training_report(self) -> Dict:
        """
        학습 리포트 생성
        """
        self.scan_npc_files()
        
        report = {
            'total_npcs': len(self.npc_configs),
            'trained_models': len(self.get_trained_models()),
            'npcs': {}
        }
        
        for npc_id, config in self.npc_configs.items():
            model_exists = (self.models_dir / npc_id / "final_model").exists()
            report['npcs'][npc_id] = {
                'name': config['name'],
                'description': config['description'],
                'trained': model_exists,
                'last_trained': config['last_trained']
            }
        
        return report
    
    def save_training_report(self, output_file="training_report.json"):
        """
        학습 리포트를 파일로 저장
        """
        report = self.create_training_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"학습 리포트 저장: {output_file}")
    
    def validate_npc_data(self, npc_file: str) -> Dict:
        """
        NPC 데이터 유효성 검사
        """
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            with open(npc_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 필수 필드 검사
            required_fields = ['npc_id', 'name', 'system_instruction', 'questions']
            for field in required_fields:
                if field not in data:
                    validation_result['errors'].append(f"필수 필드 누락: {field}")
                    validation_result['valid'] = False
            
            # 질문 데이터 검사
            if 'questions' in data:
                questions = data['questions']
                if len(questions) < 5:
                    validation_result['warnings'].append("질문이 5개 미만입니다.")
                
                for i, question in enumerate(questions):
                    if 'question' not in question:
                        validation_result['errors'].append(f"질문 {i+1}: 'question' 필드 누락")
                        validation_result['valid'] = False
                    
                    if 'stat_keywords' not in question:
                        validation_result['errors'].append(f"질문 {i+1}: 'stat_keywords' 필드 누락")
                        validation_result['valid'] = False
            
            # 대화 예시 검사
            if 'conversation_examples' in data:
                examples = data['conversation_examples']
                for i, example in enumerate(examples):
                    required_example_fields = ['user', 'assistant']
                    for field in required_example_fields:
                        if field not in example:
                            validation_result['errors'].append(f"대화 예시 {i+1}: '{field}' 필드 누락")
                            validation_result['valid'] = False
            
        except json.JSONDecodeError as e:
            validation_result['errors'].append(f"JSON 파싱 오류: {e}")
            validation_result['valid'] = False
        except Exception as e:
            validation_result['errors'].append(f"파일 읽기 오류: {e}")
            validation_result['valid'] = False
        
        return validation_result

def main():
    """
    사용 예시
    """
    # 매니저 초기화
    manager = MultiNPCManager()
    
    # NPC 목록 조회
    npcs = manager.list_npcs()
    print("발견된 NPC들:")
    for npc_id, config in npcs.items():
        print(f"  - {config['name']} ({npc_id})")
    
    # 특정 NPC 학습 (예: god NPC)
    if 'god' in npcs:
        print("\n김샐프 NPC 학습 시작...")
        success = manager.train_single_npc('god', num_train_epochs=2)
        if success:
            print("김샐프 NPC 학습 완료!")
        else:
            print("김샐프 NPC 학습 실패")
    
    # 모든 NPC 학습 (주석 처리)
    # print("\n모든 NPC 학습 시작...")
    # results = manager.train_all_npcs(num_train_epochs=2)
    
    # 학습 리포트 생성
    manager.save_training_report()
    
    # 학습된 모델 목록
    trained = manager.get_trained_models()
    print(f"\n학습된 모델: {trained}")

if __name__ == "__main__":
    main()