import os
import json
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model

# 환경 설정
os.environ["WANDB_DISABLED"] = "true"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

class NPCDataset:
    """NPC 훈련 데이터를 처리하는 클래스"""
    
    def __init__(self, training_data_path, tokenizer, max_length=1024):
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # JSON 파일에서 훈련 데이터 로드
        with open(training_data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        print(f"✅ {len(self.data)}개의 훈련 샘플을 로드했습니다.")
        
        # 텍스트 데이터 준비
        self.texts = [item["text"] for item in self.data]
    
    def get_dataset(self):
        """Hugging Face Dataset 형식으로 반환"""
        def tokenize_function(examples):
            # 배치 토크나이징
            tokenized = self.tokenizer(
                examples["text"],
                truncation=True,
                padding='max_length',
                max_length=self.max_length,
                return_tensors="pt"
            )
            
            # labels = input_ids (causal LM)
            tokenized["labels"] = tokenized["input_ids"].clone()
            
            return tokenized
        
        # Dataset 생성
        dataset = Dataset.from_dict({"text": self.texts})
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        
        return tokenized_dataset

def setup_model_and_tokenizer(model_id, base_path):
    """모델과 토크나이저 설정"""
    
    # 8-bit quantization 설정
    bnb_config = BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_enable_fp32_cpu_offload=True
    )
    
    # 캐시 디렉토리
    cache_dir = os.path.join(base_path, 'workspace/cache')
    
    # 모델 로드
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map='auto',
        cache_dir=cache_dir,
        torch_dtype=torch.float16,
        trust_remote_code=True
    )
    
    # 토크나이저 로드
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        cache_dir=cache_dir,
        trust_remote_code=True
    )
    
    # pad_token 설정
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    return model, tokenizer

def main():
    print("🚀 NPC 데이터를 활용한 파인튜닝 시작!\n")
    
    # 기본 설정
    base_path = '/home/apic/python/advanture_game'
    model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"
    training_data_path = "data/training/god_npc_training.json"
    
    # 훈련 데이터 파일 존재 확인
    if not os.path.exists(training_data_path):
        print(f"❌ 훈련 데이터 파일을 찾을 수 없습니다: {training_data_path}")
        print("먼저 NPC 데이터를 생성해주세요:")
        print("python save_npc_data.py")
        return
    
    # GPU 메모리 정리
    torch.cuda.empty_cache()
    
    print("🤖 모델과 토크나이저 로딩 중...")
    model, tokenizer = setup_model_and_tokenizer(model_id, base_path)
    
    print("📚 NPC 훈련 데이터 준비 중...")
    npc_dataset = NPCDataset(training_data_path, tokenizer)
    train_dataset = npc_dataset.get_dataset()
    
    print(f"✅ 훈련 데이터셋 준비 완료: {len(train_dataset)}개 샘플")
    
    print("🔧 LoRA 설정 중...")
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        bias="none",
        task_type="CAUSAL_LM",
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    print("⚙️ 훈련 설정 중...")
    output_dir = os.path.join(base_path, 'workspace/npc-god-adapter')
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=50,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=5,
        save_steps=100,
        save_total_limit=3,
        prediction_loss_only=True,
        remove_unused_columns=False,
        dataloader_pin_memory=False,
        report_to="none"
    )
    
    # 데이터 콜레이터
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
        pad_to_multiple_of=8
    )
    
    print("🎯 Trainer 설정 중...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    
    print("🚂 파인튜닝 시작!")
    try:
        # 훈련 실행
        trainer.train()
        
        print("💾 모델 저장 중...")
        trainer.save_model()
        tokenizer.save_pretrained(output_dir)
        
        print(f"✅ 파인튜닝 완료! 모델이 {output_dir}에 저장되었습니다.")
        
        # 간단한 테스트
        print("\n🧪 신 김샐프 테스트:")
        test_prompt = "<|system|>\n당신은 게임 '어드벤처 월드'의 NPC '신 김샐프'입니다.\n<|user|>\n게임을 시작하고 싶습니다.\n<|assistant|>\n"
        
        inputs = tokenizer.encode(test_prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_new_tokens=150,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("응답:", response[len(test_prompt):])
        
        print(f"\n🎉 NPC 파인튜닝이 성공적으로 완료되었습니다!")
        print(f"📁 저장 위치: {output_dir}")
        
    except Exception as e:
        print(f"❌ 훈련 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()