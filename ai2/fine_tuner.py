"""
개선된 파인튜닝 트레이너
효율적인 메모리 사용과 안정적인 학습을 위한 모듈
"""

import os
import torch
import json
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, TaskType
from typing import List, Dict, Any
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NPCFineTuner:
    def __init__(self, 
                 model_name: str = "Bllossom/llama-3.2-Korean-Bllossom-3B",
                 base_path: str = "/home/apic/python/advanture_game"):
        self.model_name = model_name
        self.base_path = base_path
        self.workspace_path = os.path.join(base_path, "workspace")
        self.cache_dir = os.path.join(self.workspace_path, "cache")
        
        # CUDA 및 메모리 설정
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
        torch.cuda.empty_cache()
        
        # 토크나이저와 모델 초기화
        self.tokenizer = None
        self.model = None
        self.setup_model()
        
    def setup_model(self):
        """모델과 토크나이저 설정"""
        logger.info("모델과 토크나이저를 로드하는 중...")
        
        # 토크나이저 로드
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            cache_dir=self.cache_dir,
            trust_remote_code=True
        )
        
        # pad_token 설정
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        # BitsAndBytes 설정 (메모리 효율성을 위해)
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_enable_fp32_cpu_offload=True
        )
        
        # 모델 로드
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            cache_dir=self.cache_dir,
            trust_remote_code=True,
            torch_dtype=torch.float16
        )
        
        logger.info("모델 로드 완료")
        
    def setup_lora(self, 
                   r: int = 8,
                   lora_alpha: int = 32,
                   lora_dropout: float = 0.1):
        """LoRA 설정 적용"""
        logger.info("LoRA 설정 적용 중...")
        
        lora_config = LoraConfig(
            r=r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj"
            ],
            bias="none",
            task_type=TaskType.CAUSAL_LM,
        )
        
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
        
        logger.info("LoRA 설정 완료")
        
    def prepare_dataset(self, dataset_path: str) -> Dataset:
        """데이터셋 준비 및 토크나이징"""
        logger.info(f"데이터셋 로드 중: {dataset_path}")
        
        # JSON 데이터 로드
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 텍스트 형식으로 변환
        texts = []
        for item in data:
            # ChatML 형식으로 포맷팅
            text = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{item['system']}<|eot_id|><|start_header_id|>user<|end_header_id|>
{item['user']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{item['assistant']}<|eot_id|><|end_of_text|>"""
            texts.append(text)
            
        # Dataset 객체 생성
        dataset = Dataset.from_dict({"text": texts})
        
        # 토크나이징
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding=False,
                max_length=2048,
                return_overflowing_tokens=False
            )
            
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        
        logger.info(f"토크나이징 완료. 데이터 수: {len(tokenized_dataset)}")
        return tokenized_dataset
        
    def train(self,
              dataset_path: str,
              output_dir: str = None,
              num_epochs: int = 3,
              batch_size: int = 1,
              gradient_accumulation_steps: int = 4,
              learning_rate: float = 2e-4,
              warmup_steps: int = 100,
              logging_steps: int = 10,
              save_steps: int = 500):
        """파인튜닝 실행"""
        
        if output_dir is None:
            output_dir = os.path.join(self.workspace_path, "npc_model")
            
        logger.info("파인튜닝 시작...")
        
        # LoRA 설정
        self.setup_lora()
        
        # 데이터셋 준비
        train_dataset = self.prepare_dataset(dataset_path)
        
        # 데이터 콜레이터 설정
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False  # Causal LM이므로 False
        )
        
        # 학습 인자 설정
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            warmup_steps=warmup_steps,
            logging_steps=logging_steps,
            save_steps=save_steps,
            save_total_limit=2,
            prediction_loss_only=True,
            remove_unused_columns=False,
            dataloader_pin_memory=False,
            fp16=True,  # 메모리 효율성을 위해
            gradient_checkpointing=True,  # 메모리 절약
            report_to=None,  # wandb 비활성화
        )
        
        # 트레이너 생성
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer,
        )
        
        # 학습 실행
        try:
            logger.info("학습 시작...")
            trainer.train()
            
            # 모델 저장
            logger.info(f"모델 저장 중: {output_dir}")
            trainer.save_model()
            self.tokenizer.save_pretrained(output_dir)
            
            logger.info("파인튜닝 완료!")
            return output_dir
            
        except Exception as e:
            logger.error(f"학습 중 오류 발생: {e}")
            raise e
            
    def create_merged_model(self, adapter_path: str, output_path: str = None):
        """LoRA 어댑터를 베이스 모델과 병합"""
        if output_path is None:
            output_path = os.path.join(self.workspace_path, "merged_model")
            
        logger.info("모델 병합 중...")
        
        # 베이스 모델 로드
        base_model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            cache_dir=self.cache_dir
        )
        
        # 어댑터 로드 및 병합
        from peft import PeftModel
        model = PeftModel.from_pretrained(base_model, adapter_path)
        merged_model = model.merge_and_unload()
        
        # 병합된 모델 저장
        merged_model.save_pretrained(output_path)
        self.tokenizer.save_pretrained(output_path)
        
        logger.info(f"병합된 모델이 {output_path}에 저장되었습니다.")
        return output_path


def main():
    """메인 실행 함수"""
    # 데이터 처리기로 데이터셋 생성
    from data_processor import NPCDataProcessor
    
    processor = NPCDataProcessor()
    dataset = processor.create_fine_tuning_dataset()
    
    # 데이터셋 저장
    dataset_path = "/home/apic/python/advanture_game/ai2/data/training_dataset.json"
    os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
    processor.save_dataset(dataset, dataset_path)
    
    # 파인튜너 생성 및 학습
    trainer = NPCFineTuner()
    
    try:
        # 학습 실행
        model_path = trainer.train(
            dataset_path=dataset_path,
            num_epochs=3,
            batch_size=1,
            gradient_accumulation_steps=4
        )
        
        logger.info(f"학습 완료! 모델 경로: {model_path}")
        
    except Exception as e:
        logger.error(f"학습 실패: {e}")


if __name__ == "__main__":
    main()
