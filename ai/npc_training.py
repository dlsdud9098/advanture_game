import json
import random
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType
import logging
from pathlib import Path
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NPCTrainer:
    def __init__(self, model_name="Bllossom/llama-3.2-Korean-Bllossom-3B"):
        """
        NPC 학습을 위한 클래스 초기화
        
        Args:
            model_name (str): 사용할 모델명
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.npc_data = None
        
    def load_npc_data(self, npc_file_path):
        """
        NPC JSON 데이터 로드
        
        Args:
            npc_file_path (str): NPC JSON 파일 경로
        """
        try:
            with open(npc_file_path, 'r', encoding='utf-8') as f:
                self.npc_data = json.load(f)
            logger.info(f"NPC 데이터 로드 완료: {self.npc_data['name']}")
            return True
        except Exception as e:
            logger.error(f"NPC 데이터 로드 실패: {e}")
            return False
    
    def load_model_and_tokenizer(self):
        """
        모델과 토크나이저 로드
        """
        try:
            logger.info(f"모델 로드 중: {self.model_name}")
            
            # 토크나이저 로드
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # pad_token 설정
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            
            # 토크나이저가 좌측 패딩을 사용하지 않도록 설정
            self.tokenizer.padding_side = "right"
            
            # 모델 로드
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
            
            logger.info("모델 및 토크나이저 로드 완료")
            return True
            
        except Exception as e:
            logger.error(f"모델 로드 실패: {e}")
            return False
    
    def setup_lora(self, lora_config=None):
        """
        LoRA 설정
        
        Args:
            lora_config (dict): LoRA 설정 파라미터
        """
        if lora_config is None:
            lora_config = {
                "r": 16,
                "lora_alpha": 32,
                "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
                "lora_dropout": 0.1,
                "bias": "none",
                "task_type": TaskType.CAUSAL_LM
            }
        
        try:
            config = LoraConfig(**lora_config)
            self.model = get_peft_model(self.model, config)
            self.model.print_trainable_parameters()
            logger.info("LoRA 설정 완료")
            return True
        except Exception as e:
            logger.error(f"LoRA 설정 실패: {e}")
            return False
    
    def generate_training_data(self, num_samples=100):
        """
        학습 데이터 생성
        
        Args:
            num_samples (int): 생성할 추가 샘플 수 (기본 예시 제외)
        """
        if not self.npc_data:
            logger.error("NPC 데이터가 로드되지 않았습니다.")
            return []
        
        training_conversations = []
        questions = self.npc_data['questions']
        examples = self.npc_data['conversation_examples']
        
        # 기본 예시 대화 추가
        for example in examples:
            conversation = self._format_conversation(
                system_msg=self.npc_data['system_instruction'],
                user_msg=example['user'],
                assistant_msg=example['assistant']
            )
            training_conversations.append(conversation)
        
        # 질문-답변 패턴으로 추가 데이터 생성
        for i in range(num_samples):
            # 하나의 질문 선택
            question_data = random.choice(questions)
            
            # 랜덤 답변 패턴 생성
            user_answer = self._generate_sample_answer(question_data)
            assistant_response = self._generate_assistant_response(question_data, user_answer)
            
            conversation = self._format_conversation(
                system_msg=self.npc_data['system_instruction'],
                user_msg=f"질문: {question_data['question']}\n답변: {user_answer}",
                assistant_msg=assistant_response
            )
            training_conversations.append(conversation)
        
        logger.info(f"총 {len(training_conversations)}개의 학습 대화 생성 완료")
        return training_conversations
    
    def _format_conversation(self, system_msg, user_msg, assistant_msg):
        """
        대화를 학습 포맷으로 변환
        """
        # 더 간단한 포맷으로 변경
        conversation = f"시스템: {system_msg}\n사용자: {user_msg}\n어시스턴트: {assistant_msg}"
        return conversation
    
    def _generate_sample_answer(self, question_data):
        """
        질문에 대한 샘플 답변 생성
        """
        stat_keywords = question_data['stat_keywords']
        # 랜덤하게 스탯 선택하고 해당 키워드 사용
        selected_stat = random.choice(list(stat_keywords.keys()))
        keywords = stat_keywords[selected_stat]
        selected_keyword = random.choice(keywords)
        
        # 간단한 답변 패턴들
        answer_patterns = [
            f"저는 {selected_keyword}을/를 중요하게 생각합니다.",
            f"{selected_keyword}이/가 제일 중요하다고 생각해요.",
            f"무엇보다 {selected_keyword}을/를 우선시합니다.",
            f"{selected_keyword}에 대해 깊이 생각해봤는데, 이것이 가장 의미있다고 봅니다."
        ]
        
        return random.choice(answer_patterns)
    
    def _generate_assistant_response(self, question_data, user_answer):
        """
        신 NPC의 응답 생성
        """
        # 답변에서 키워드 분석
        stat_points = {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
        for stat, keywords in question_data['stat_keywords'].items():
            for keyword in keywords:
                if keyword in user_answer:
                    stat_points[stat] += 2
        
        # 응답 패턴
        responses = [
            "그렇군요. 당신의 마음이 느껴집니다.",
            "훌륭한 답변입니다. 당신의 성향을 이해했습니다.",
            "흥미로운 관점이군요. 이는 용사로서 중요한 자질입니다.",
            "깊이 있는 생각이 담긴 답변입니다."
        ]
        
        response = random.choice(responses)
        
        # 스탯 반영 코멘트 추가
        max_stat = max(stat_points, key=stat_points.get)
        if stat_points[max_stat] > 0:
            stat_comments = {
                "STR": "강인한 의지가 느껴집니다.",
                "AGI": "민첩하고 기민한 성향이 보입니다.",
                "INT": "지혜로운 판단력을 보여주시는군요.",
                "LUCK": "직감적이고 영감이 풍부하시군요."
            }
            response += f" {stat_comments.get(max_stat, '')}"
        
        return response
    
    def prepare_dataset(self, conversations):
        """
        학습용 데이터셋 준비
        """
        def tokenize_function(examples):
            # 배치 처리 시 return_tensors 제거, padding도 DataCollator에서 처리
            tokens = self.tokenizer(
                examples['text'],
                truncation=True,
                max_length=1024,
                padding=False  # DataCollator에서 처리
            )
            # labels도 같은 방식으로 설정
            tokens["labels"] = tokens["input_ids"].copy()
            return tokens
        
        dataset = Dataset.from_dict({"text": conversations})
        tokenized_dataset = dataset.map(
            tokenize_function, 
            batched=True,
            remove_columns=dataset.column_names  # 원본 텍스트 컬럼 제거
        )
        
        return tokenized_dataset
    
    def train(self, 
              output_dir="./npc_models", 
              num_train_epochs=3,
              per_device_train_batch_size=1,
              gradient_accumulation_steps=8,
              learning_rate=2e-4,
              save_steps=500,
              logging_steps=100):
        """
        모델 학습 실행
        """
        if not self.model or not self.tokenizer:
            logger.error("모델이 로드되지 않았습니다.")
            return False
        
        # 학습 데이터 생성
        logger.info("학습 데이터 생성 중...")
        conversations = self.generate_training_data(num_samples=50)  # 테스트용으로 작게
        if not conversations:
            logger.error("학습 데이터 생성 실패")
            return False
        
        logger.info(f"첫 번째 대화 예시:\n{conversations[0][:200]}...")
        
        # 데이터셋 준비
        logger.info("데이터셋 토크나이제이션 중...")
        train_dataset = self.prepare_dataset(conversations)
        
        # 학습 인자 설정
        training_args = TrainingArguments(
            output_dir=f"{output_dir}/{self.npc_data['npc_id']}",
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            save_steps=save_steps,
            logging_steps=logging_steps,
            save_total_limit=3,
            remove_unused_columns=False,
            dataloader_pin_memory=False,
            fp16=torch.cuda.is_available(),
            report_to=None
        )
        
        # 데이터 콜레이터
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
            pad_to_multiple_of=8  # 성능 최적화
        )
        
        # 트레이너 초기화
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer
        )
        
        try:
            logger.info("학습 시작")
            trainer.train()
            
            # 모델 저장
            model_save_path = f"{output_dir}/{self.npc_data['npc_id']}/final_model"
            trainer.save_model(model_save_path)
            self.tokenizer.save_pretrained(model_save_path)
            
            logger.info(f"학습 완료. 모델 저장 경로: {model_save_path}")
            return True
            
        except Exception as e:
            logger.error(f"학습 중 오류 발생: {e}")
            return False
    
    def save_training_config(self, output_dir="./npc_models"):
        """
        학습 설정 저장
        """
        config = {
            "npc_id": self.npc_data['npc_id'],
            "npc_name": self.npc_data['name'],
            "model_name": self.model_name,
            "num_questions": len(self.npc_data['questions']),
            "training_timestamp": str(torch.cuda.current_device()) if torch.cuda.is_available() else "cpu"
        }
        
        config_path = f"{output_dir}/{self.npc_data['npc_id']}/training_config.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"학습 설정 저장: {config_path}")

def main():
    """
    메인 실행 함수
    """
    # NPC 트레이너 초기화
    trainer = NPCTrainer()
    
    # NPC 데이터 로드
    npc_file = "./data/data_files/npc_instruction/god_npc_data.json"  # JSON 파일 경로
    if not trainer.load_npc_data(npc_file):
        return
    
    # 모델 로드
    if not trainer.load_model_and_tokenizer():
        return
    
    # LoRA 설정
    if not trainer.setup_lora():
        return
    
    # 학습 실행
    success = trainer.train(
        num_train_epochs=1,  # 테스트용으로 1 에포크
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,  # 줄임
        learning_rate=2e-4
    )
    
    if success:
        # 학습 설정 저장
        trainer.save_training_config()
        print("김샐프 NPC 학습이 성공적으로 완료되었습니다!")
    else:
        print("학습 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main()