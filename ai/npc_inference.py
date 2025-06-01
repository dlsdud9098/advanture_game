import json
import random
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NPCInference:
    """
    학습된 NPC 모델을 사용하여 대화 생성
    """
    
    def __init__(self, base_model_name="Bllossom/llama-3.2-Korean-Bllossom-3B"):
        """
        초기화
        
        Args:
            base_model_name (str): 기본 모델명
        """
        self.base_model_name = base_model_name
        self.tokenizer = None
        self.base_model = None
        self.loaded_npcs = {}  # npc_id: (model, npc_data)
        
    def load_base_model(self):
        """
        기본 모델과 토크나이저 로드
        """
        try:
            logger.info(f"기본 모델 로드 중: {self.base_model_name}")
            
            # 토크나이저 로드
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            
            # 기본 모델 로드
            self.base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
            
            logger.info("기본 모델 로드 완료")
            return True
            
        except Exception as e:
            logger.error(f"기본 모델 로드 실패: {e}")
            return False
    
    def load_npc_model(self, npc_id: str, model_path: str, npc_data_path: str):
        """
        특정 NPC 모델 로드
        
        Args:
            npc_id (str): NPC 식별자
            model_path (str): 학습된 모델 경로
            npc_data_path (str): NPC JSON 데이터 경로
        """
        try:
            logger.info(f"NPC '{npc_id}' 모델 로드 중...")
            
            # 기본 모델이 로드되지 않았다면 로드
            if self.base_model is None:
                if not self.load_base_model():
                    return False
            
            # LoRA 어댑터가 적용된 모델 로드
            npc_model = PeftModel.from_pretrained(
                self.base_model,
                model_path,
                torch_dtype=torch.float16
            )
            
            # NPC 데이터 로드
            with open(npc_data_path, 'r', encoding='utf-8') as f:
                npc_data = json.load(f)
            
            # 메모리에 저장
            self.loaded_npcs[npc_id] = (npc_model, npc_data)
            
            logger.info(f"NPC '{npc_id}' 로드 완료")
            return True
            
        except Exception as e:
            logger.error(f"NPC '{npc_id}' 로드 실패: {e}")
            return False
    
    def generate_response(self, npc_id: str, user_input: str, max_length: int = 256, temperature: float = 0.8) -> str:
        """
        NPC 응답 생성
        
        Args:
            npc_id (str): 사용할 NPC
            user_input (str): 사용자 입력
            max_length (int): 최대 생성 길이
            temperature (float): 생성 온도
            
        Returns:
            str: NPC 응답
        """
        if npc_id not in self.loaded_npcs:
            return f"NPC '{npc_id}'가 로드되지 않았습니다."
        
        try:
            model, npc_data = self.loaded_npcs[npc_id]
            
            # 더 간단하고 명확한 프롬프트 구성
            system_instruction = npc_data['system_instruction']
            prompt = f"{system_instruction}\n\n사용자 질문: {user_input}\n\n김샐프의 답변:"
            
            # 토크나이징
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=200  # 더 짧은 입력으로 응답 공간 확보
            )
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
            
            # 응답 생성 (더 엄격한 파라미터)
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=80,  # 새로 생성할 토큰 수 제한
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9,  # nucleus sampling 추가
                    top_k=50,   # top-k sampling 추가
                    repetition_penalty=1.3,  # 반복 억제 강화
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3  # 3-gram 반복 방지
                )
            
            # 응답 디코딩 및 정리
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # 프롬프트 부분 제거
            if "김샐프의 답변:" in response:
                response = response.split("김샐프의 답변:")[-1].strip()
            elif "어시스턴트:" in response:
                response = response.split("어시스턴트:")[-1].strip()
            
            # 응답 후처리
            response = self.clean_response(response)
            
            # 응답이 너무 짧거나 이상하면 기본 응답 사용
            if len(response.strip()) < 10 or self.is_repetitive(response):
                return self.get_fallback_response(user_input, npc_data)
            
            return response
            
        except Exception as e:
            logger.error(f"응답 생성 실패: {e}")
            return "죄송합니다. 응답을 생성할 수 없습니다."
    
    def clean_response(self, response: str) -> str:
        """
        응답 정리 및 후처리
        """
        # 줄바꿈 정리
        response = response.replace('\n', ' ').strip()
        
        # 반복되는 구문 제거
        words = response.split()
        cleaned_words = []
        prev_word = ""
        repeat_count = 0
        
        for word in words:
            if word == prev_word:
                repeat_count += 1
                if repeat_count < 2:  # 최대 1번까지만 반복 허용
                    cleaned_words.append(word)
            else:
                repeat_count = 0
                cleaned_words.append(word)
            prev_word = word
        
        response = ' '.join(cleaned_words)
        
        # 문장 부호 정리
        response = response.replace(' .', '.').replace(' ,', ',')
        response = response.replace('..', '.').strip()
        
        # 너무 긴 응답 자르기
        sentences = response.split('.')
        if len(sentences) > 3:
            response = '. '.join(sentences[:3]) + '.'
        
        return response
    
    def is_repetitive(self, text: str) -> bool:
        """
        텍스트가 반복적인지 확인
        """
        words = text.split()
        if len(words) < 4:
            return False
        
        # 같은 단어가 연속으로 3번 이상 나오는지 확인
        for i in range(len(words) - 2):
            if words[i] == words[i+1] == words[i+2]:
                return True
        
        return False
    
    def get_fallback_response(self, user_input: str, npc_data: dict) -> str:
        """
        기본 대체 응답 생성 (모델 응답이 이상할 때 사용)
        """
        fallback_responses = [
            "그렇군요. 당신의 마음이 잘 전해집니다.",
            "흥미로운 답변이군요. 당신의 성향을 이해했습니다.",
            "좋습니다. 이는 용사로서 중요한 자질입니다.",
            "깊이 있는 생각이 담긴 답변입니다.",
            "훌륭합니다. 당신의 의지가 느껴집니다."
        ]
        
        import random
        return random.choice(fallback_responses)
    
    def analyze_stat_keywords(self, npc_id: str, user_answer: str, question_id: int) -> Dict[str, int]:
        """
        사용자 답변에서 스탯 키워드 분석
        
        Args:
            npc_id (str): NPC ID
            user_answer (str): 사용자 답변
            question_id (int): 질문 ID
            
        Returns:
            Dict[str, int]: 스탯별 점수
        """
        if npc_id not in self.loaded_npcs:
            return {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
        _, npc_data = self.loaded_npcs[npc_id]
        
        # 해당 질문 찾기
        question_data = None
        for question in npc_data.get('questions', []):
            if question['id'] == question_id:
                question_data = question
                break
        
        if not question_data:
            return {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
        # 키워드 분석
        stat_points = {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
        for stat, keywords in question_data['stat_keywords'].items():
            for keyword in keywords:
                if keyword in user_answer:
                    stat_points[stat] += 2
        
        return stat_points
    
    def determine_class(self, npc_id: str, total_stats: Dict[str, int]) -> str:
        """
        총 스탯에 따른 직업 결정
        
        Args:
            npc_id (str): NPC ID
            total_stats (Dict[str, int]): 총합 스탯
            
        Returns:
            str: 결정된 직업
        """
        if npc_id not in self.loaded_npcs:
            return "전사"
        
        _, npc_data = self.loaded_npcs[npc_id]
        class_mapping = npc_data.get('class_mapping', {})
        
        # 가장 높은 스탯 찾기
        max_stat = max(total_stats, key=total_stats.get)
        
        # 각 직업의 주스탯 확인
        for class_name, class_info in class_mapping.items():
            if class_info['primary_stat'] == max_stat:
                # 최소 비율 조건 확인
                total_score = sum(total_stats.values())
                if total_score > 0:
                    stat_ratio = total_stats[max_stat] / total_score
                    if stat_ratio >= class_info.get('min_ratio', 0.3):
                        return class_name
        
        # 기본값으로 전사 반환
        return "전사"


class NPCManager:
    """
    여러 NPC를 관리하는 클래스
    """
    
    def __init__(self, models_dir="./npc_models", npc_data_dir="./data/data_files/npc_instruction"):
        """
        초기화
        
        Args:
            models_dir (str): 학습된 모델들이 있는 디렉토리
            npc_data_dir (str): NPC 데이터 파일들이 있는 디렉토리
        """
        self.models_dir = Path(models_dir)
        self.npc_data_dir = Path(npc_data_dir)
        self.inference = NPCInference()
        self.loaded_npcs = []
        
    def auto_load_npcs(self):
        """
        디렉토리에서 학습된 NPC들을 자동으로 찾아서 로드
        """
        logger.info("학습된 NPC 모델들을 검색 중...")
        
        for npc_dir in self.models_dir.iterdir():
            if npc_dir.is_dir():
                npc_id = npc_dir.name
                model_path = npc_dir / "final_model"
                npc_data_path = self.npc_data_dir / f"{npc_id}_npc_data.json"
                
                # god NPC의 경우 특별 처리
                if npc_id == "god" and not npc_data_path.exists():
                    npc_data_path = self.npc_data_dir / "god_npc_data.json"
                
                if model_path.exists() and npc_data_path.exists():
                    success = self.inference.load_npc_model(npc_id, str(model_path), str(npc_data_path))
                    if success:
                        self.loaded_npcs.append(npc_id)
                        logger.info(f"NPC '{npc_id}' 자동 로드 완료")
                else:
                    logger.warning(f"NPC '{npc_id}' 로드 실패: 모델 또는 데이터 파일 없음")
        
        logger.info(f"총 {len(self.loaded_npcs)}개 NPC 로드 완료: {self.loaded_npcs}")
    
    def chat_with_npc(self, npc_id: str, message: str) -> str:
        """
        특정 NPC와 대화
        
        Args:
            npc_id (str): NPC ID
            message (str): 메시지
            
        Returns:
            str: NPC 응답
        """
        if npc_id not in self.loaded_npcs:
            return f"NPC '{npc_id}'가 로드되지 않았습니다."
        
        return self.inference.generate_response(npc_id, message)
    
    def get_npc_info(self, npc_id: str) -> Dict:
        """
        NPC 정보 조회
        
        Args:
            npc_id (str): NPC ID
            
        Returns:
            Dict: NPC 정보
        """
        if npc_id not in self.inference.loaded_npcs:
            return {}
        
        _, npc_data = self.inference.loaded_npcs[npc_id]
        return {
            "name": npc_data.get("name"),
            "description": npc_data.get("description"),
            "personality": npc_data.get("personality", {}),
            "num_questions": len(npc_data.get("questions", []))
        }


class GodNPCQuestionnaire:
    """
    김샐프(신 NPC) 전용 질문-답변 시스템
    """
    
    def __init__(self, npc_manager: NPCManager):
        """
        초기화
        
        Args:
            npc_manager: NPC 매니저 인스턴스
        """
        self.npc_manager = npc_manager
        self.npc_id = "god"
        self.current_question_index = 0
        self.selected_questions = []
        self.user_answers = []
        self.total_stats = {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
    def start_questionnaire(self, num_questions: int = 15):
        """
        질문지 시작
        
        Args:
            num_questions (int): 질문 개수
        """
        if self.npc_id not in self.npc_manager.loaded_npcs:
            return "김샐프 NPC가 로드되지 않았습니다."
        
        # 질문 랜덤 선택
        _, npc_data = self.npc_manager.inference.loaded_npcs[self.npc_id]
        all_questions = npc_data.get('questions', [])
        
        self.selected_questions = random.sample(
            all_questions, 
            min(num_questions, len(all_questions))
        )
        
        self.current_question_index = 0
        self.user_answers = []
        self.total_stats = {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
        # 인사말
        greeting = npc_data.get('response_templates', {}).get('greeting', 
                                                             "용사여, 환영합니다.")
        return greeting
    
    def get_current_question(self) -> str:
        """
        현재 질문 반환
        """
        if self.current_question_index < len(self.selected_questions):
            question = self.selected_questions[self.current_question_index]
            return question['question']
        else:
            return self.finalize_questionnaire()
    
    def answer_question(self, user_answer: str) -> str:
        """
        질문에 답변하고 다음 질문으로 진행
        
        Args:
            user_answer (str): 사용자 답변
            
        Returns:
            str: NPC 응답
        """
        if self.current_question_index >= len(self.selected_questions):
            return "모든 질문이 완료되었습니다."
        
        current_question = self.selected_questions[self.current_question_index]
        
        # 답변 저장
        self.user_answers.append({
            'question_id': current_question['id'],
            'question': current_question['question'],
            'answer': user_answer
        })
        
        # 스탯 분석
        question_stats = self.npc_manager.inference.analyze_stat_keywords(
            self.npc_id, user_answer, current_question['id']
        )
        
        # 총 스탯에 추가
        for stat, points in question_stats.items():
            self.total_stats[stat] += points
        
        # NPC 응답 생성
        npc_response = self.npc_manager.chat_with_npc(
            self.npc_id, 
            f"질문: {current_question['question']}\n답변: {user_answer}"
        )
        
        # 다음 질문으로 진행
        self.current_question_index += 1
        
        return npc_response
    
    def finalize_questionnaire(self) -> Dict:
        """
        질문지 완료 및 최종 결과 반환
        
        Returns:
            Dict: 최종 결과 (스탯, 직업 등)
        """
        # 직업 결정
        final_class = self.npc_manager.inference.determine_class(self.npc_id, self.total_stats)
        
        # 최종 메시지
        _, npc_data = self.npc_manager.inference.loaded_npcs[self.npc_id]
        templates = npc_data.get('response_templates', {})
        
        result = {
            'completed': True,
            'final_stats': self.total_stats,
            'assigned_class': final_class,
            'class_description': npc_data.get('class_mapping', {}).get(final_class, {}).get('description', ''),
            'answers': self.user_answers,
            'final_message': templates.get('farewell', '이제 당신의 여정이 시작됩니다.')
        }
        
        return result
    
    def get_progress(self) -> Dict:
        """
        진행 상황 조회
        
        Returns:
            Dict: 진행 상황
        """
        return {
            'current_question': self.current_question_index + 1,
            'total_questions': len(self.selected_questions),
            'current_stats': self.total_stats,
            'completed': self.current_question_index >= len(self.selected_questions)
        }


def main():
    """
    사용 예시
    """
    # NPC 매니저 초기화 및 모델 로드
    manager = NPCManager()
    manager.auto_load_npcs()
    
    if not manager.loaded_npcs:
        print("로드된 NPC가 없습니다. 먼저 모델을 학습시켜주세요.")
        return
    
    print("=== 로드된 NPC 목록 ===")
    for npc_id in manager.loaded_npcs:
        info = manager.get_npc_info(npc_id)
        print(f"- {info.get('name', npc_id)}: {info.get('description', '')}")
    
    # 김샐프와 간단한 대화 테스트
    if "god" in manager.loaded_npcs:
        print("\n=== 김샐프와 대화 테스트 ===")
        response = manager.chat_with_npc("god", "안녕하세요!")
        print(f"김샐프: {response}")
        
        # 질문지 시스템 테스트
        print("\n=== 질문지 시스템 테스트 ===")
        questionnaire = GodNPCQuestionnaire(manager)
        
        # 질문지 시작
        greeting = questionnaire.start_questionnaire(num_questions=3)  # 테스트용 3문제
        print(f"김샐프: {greeting}")
        
        # 첫 번째 질문
        question1 = questionnaire.get_current_question()
        print(f"\n질문 1: {question1}")
        
        # 테스트 답변
        answer1 = "정의를 위해 싸우는 것이 가장 중요합니다."
        response1 = questionnaire.answer_question(answer1)
        print(f"김샐프: {response1}")
        
        # 진행 상황 확인
        progress = questionnaire.get_progress()
        print(f"\n진행 상황: {progress['current_question']}/{progress['total_questions']}")
        print(f"현재 스탯: {progress['current_stats']}")

if __name__ == "__main__":
    main()