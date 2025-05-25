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
from datasets import load_dataset

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
    # GPU 메모리 초기화
    torch.cuda.empty_cache()
    torch.cuda.reset_accumulated_memory_stats()
    torch.cuda.reset_peak_memory_stats()



    base_path = '/home/apic/python/advanture_game'
    # 8-bit BitsAndBytes config (8-bit uses bfloat16)
    bnb_config = BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_enable_fp32_cpu_offload=True
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

    # pad_token 설정
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    train_data = []
    files = []
    files.extend(glob("data/data_files/npc_instruction/*.txt"))
    files.extend(glob('data/data_files/other_instruction/*.txt'))
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            texts = "".join(f.readlines())
            train_data.append(texts)

    # 토큰화, 여기서 return_tensors를 안 써서 리스트형 반환
    tokenized_data = tokenizer(
        train_data,
        truncation=True,
        padding=True,
    )

    # Dataset 객체로 변환
    train_dataset = Dataset.from_dict(tokenized_data)

    # LoRA 설정
    lora_config = LoraConfig(
        r=8,
        lora_alpha = 32,
        lora_dropout = 0.1,
        target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
        task_type="CAUSAL_LM",
    )
    
    model = get_peft_model(model, lora_config)
    model.train()

    try:
        training_args = TrainingArguments(
            seed=42,
            output_dir=os.path.join(base_path, 'result'),
            num_train_epochs=20,
            per_device_train_batch_size=5,  # vram 부족할 시 감소
            per_device_eval_batch_size=2,   # vram 부족할 시 증가
            gradient_accumulation_steps=1,  # vram 부족할 시 감소
            optim="paged_adamw_8bit",
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
            train_dataset=train_dataset,
            args=training_args,
            peft_config=lora_config,
        )

        trainer.train()

        trainer.model.save_pretrained(os.path.join(base_path, 'workspace/lora-adapter-epoch3'))
        tokenizer.save_pretrained('workspace/lora-adapter-epoch3')
        print(f'./workspace/에 저장되었습니다.')
    except RuntimeError as e:
            print(f"배치 크기에서 VRAM 부족: {e}")
    
    







    