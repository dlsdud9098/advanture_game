import json
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import os

class NPCPromptTuner:
    def __init__(self):
        self.model_name = "Bllossom/llama-3.2-Korean-Bllossom-3B"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 토크나이저 및 모델 로딩
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        # LoRA 설정 (메모리 효율성을 위해)
        self.setup_lora()
        
    def setup_lora(self):
        """LoRA 설정으로 메모리 효율적 파인튜닝"""
        lora_config = LoraConfig(
            r=16,  # rank
            lora_alpha=32,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        self.model = prepare_model_for_kbit_training(self.model)
        self.model = get_peft_model(self.model, lora_config)
        
    def load_data(self, npc_json_path, question_json_path):
        """NPC 데이터와 질문 데이터 로딩"""
        with open(npc_json_path, 'r', encoding='utf-8') as f:
            npc_data = json.load(f)
            
        with open(question_json_path, 'r', encoding='utf-8') as f:
            question_data = json.load(f)
            
        return npc_data, question_data
    
    def create_training_data(self, npc_data, question_data):
        """훈련 데이터 생성"""
        training_examples = []
        
        for npc in npc_data:
            npc_name = npc.get('name', 'NPC')
            npc_personality = npc.get('personality', '')
            npc_background = npc.get('background', '')
            
            # 시스템 프롬프트 생성
            system_prompt = f"""당신은 {npc_name}입니다.
성격: {npc_personality}
배경: {npc_background}

플레이어와 자연스럽게 대화하세요. 캐릭터의 성격과 배경에 맞게 응답하세요."""

            # 질문-답변 쌍 생성
            for qa in question_data:
                question = qa.get('question', '')
                expected_answer = qa.get('answer', '')
                
                # 대화 형식으로 포맷팅
                conversation = f"""<|system|>
{system_prompt}
<|user|>
{question}
<|assistant|>
{expected_answer}"""
                
                training_examples.append({
                    'text': conversation,
                    'npc_name': npc_name
                })
                
        return training_examples
    
    def tokenize_data(self, examples):
        """데이터 토크나이징"""
        tokenized = self.tokenizer(
            examples['text'],
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        )
        
        # labels를 input_ids와 동일하게 설정 (언어 모델링용)
        tokenized['labels'] = tokenized['input_ids'].clone()
        
        return tokenized
    
    def create_dataset(self, training_examples):
        """Dataset 객체 생성"""
        dataset = Dataset.from_list(training_examples)
        tokenized_dataset = dataset.map(
            self.tokenize_data, 
            batched=True,
            remove_columns=dataset.column_names
        )
        
        return tokenized_dataset
    
    def train(self, dataset, output_dir="./npc_tuned_model"):
        """모델 훈련"""
        
        # 훈련 설정
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=2,  # RTX 3060 12GB에 맞게 조정
            gradient_accumulation_steps=4,
            warmup_steps=100,
            learning_rate=2e-4,
            fp16=True,  # 메모리 절약
            logging_steps=10,
            save_steps=500,
            save_total_limit=2,
            prediction_loss_only=True,
            remove_unused_columns=False,
            dataloader_pin_memory=False,
        )
        
        # 데이터 콜레이터
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,  # 인과적 언어 모델링
        )
        
        # 트레이너 생성
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator,
        )
        
        # 훈련 시작
        print("훈련을 시작합니다...")
        trainer.train()
        
        # 모델 저장
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        print(f"모델이 {output_dir}에 저장되었습니다.")
    
    def test_model(self, prompt, max_length=200):
        """훈련된 모델 테스트"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):]

# 사용 예시
def main():
    # 프롬프트 튜너 초기화
    tuner = NPCPromptTuner()
    
    # 데이터 로딩 (실제 파일 경로로 변경)
    npc_data, question_data = tuner.load_data(
        "data/npc_data.json", 
        "data/questions.json"
    )
    
    # 훈련 데이터 생성
    training_examples = tuner.create_training_data(npc_data, question_data)
    print(f"총 {len(training_examples)}개의 훈련 예시가 생성되었습니다.")
    
    # 데이터셋 생성
    dataset = tuner.create_dataset(training_examples)
    
    # 모델 훈련
    tuner.train(dataset)
    
    # 모델 테스트
    test_prompt = """<|system|>
당신은 마을의 대장장이입니다.
성격: 친근하고 열정적
배경: 30년간 무기와 방어구를 제작해온 숙련된 장인

<|user|>
좋은 검을 하나 만들어주실 수 있나요?
<|assistant|>
"""
    
    response = tuner.test_model(test_prompt)
    print("테스트 응답:", response)

if __name__ == "__main__":
    main()