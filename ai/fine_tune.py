import os
import torch
# from datasets import load_dataset
from datasets import Dataset, concatenate_datasets

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)
from peft import LoraConfig, get_peft_model, PeftModel
from trl import SFTTrainer

from glob import glob

import subprocess

os.environ["WANDB_DISABLED"] = "true"

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

# cuDNN 관련 설정
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
os.environ['CUBLAS_WORKSPACE_CONFIG'] = ":4096:8"  # (PyTorch 1.8 이상에서 추천)
torch.use_deterministic_algorithms(True)

if __name__ == '__main__':
    base_path = '/home/apic/python/advanture_game'
    # 8-bit BitsAndBytes config (8-bit uses bfloat16)
    bnb_config = BitsAndBytesConfig(
    load_in_8bit=True
    )

    # 모델 불러오기
    model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"

    os.makedirs(name=os.path.join(base_path, 'workspace/cache'), exist_ok=os.path.join(base_path, 'workspace/cache'))
    model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map='auto',
    cache_dir = os.path.join(base_path, 'workspace/cache')
    )
    
    # 토크나이저 설정
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        cache_dir=os.path.join(base_path, 'workspace/cache')
    )

    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = 'right'
    
    # 데이터 불러오기
    
    train_files = glob(os.path.join(base_path, 'data/data_files/npc_instruction/npc_god.json'))
    lora_name = os.path.splitext(os.path.basename(train_files[0]))[0]
    lora_name = os.path.basename(train_files[0])

    # 여러 파일을 하나씩 읽어서 Dataset 객체로 변환하고, 결합
    datasets = [Dataset.from_json(file) for file in train_files]
    train = concatenate_datasets(datasets)  # 여러 데이터셋을 하나로 합침
    
    # 프롬프트 작성
    def prompting(instruction, input, output):
        prompt = (
            "<설정>\n"
            f"{instruction}\n\n"
            "<대화>\n"
            f"질문: {input}\n"
            f"답변: {output}\n"
        )
        return prompt

    def chat_format(row):
        prompt = prompting(row["instruction"], row["input"], row["output"])
        tokens = tokenizer(prompt, truncation=True, padding=True, max_length=1024)
        row["input_ids"] = tokens["input_ids"]  # 토큰화된 input_ids만 저장
        row['attention_mask'] = tokens['attention_mask']  # 토큰화된 attention_mask만 
        
        return row
        
    train = train.map(chat_format, batched=False, num_proc=4)
    
    # LoRA 설정
    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=[
            "q_proj", "v_proj", "k_proj", "o_proj",
            "gate_proj", "down_proj", "up_proj"
        ],
        lora_dropout=0.1,
        bias='none',
        task_type='CAUSAL_LM'
    )
    
    model = get_peft_model(model, lora_config)
    model.train()
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model.to(device)

    try:
        training_args = TrainingArguments(
            seed=42,
            output_dir=os.path.join(base_path, 'result'),
            num_train_epochs=3,
            per_device_train_batch_size=3,  # vram 부족할 시 감소
            per_device_eval_batch_size=2,   # vram 부족할 시 증가
            gradient_accumulation_steps=3,  # vram 부족할 시 감소
            optim="paged_adamw_32bit",
            eval_strategy="no",
            logging_dir=os.path.join(base_path, 'logs'),
            logging_steps=50,
            warmup_steps=20,    
            logging_strategy="steps",
            learning_rate=2e-4,
            group_by_length=True,
            save_strategy="epoch",
            fp16=True
        )

        trainer = SFTTrainer(
            model=model,
            train_dataset=train,
            args=training_args,
            peft_config=lora_config,
            formatting_func=lambda x: x['input_ids']
        )

        trainer.train()
    except RuntimeError as e:
            print(f"배치 크기에서 VRAM 부족: {e}")
    
    trainer.model.save_pretrained(os.path.join(base_path, 'workspace/lora-adapter-epoch3'))
    print(f'./workspace/에 저장되었습니다.')