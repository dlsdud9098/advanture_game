import os
import torch
# from datasets import load_dataset
from datasets import Dataset, concatenate_datasets
from datasets import load_dataset

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

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
    dataset = load_dataset('json', data_files={'train': 'data/data_files/npc_instruction/npc_god2.json'})

    def chat_format(row):
        return tokenizer(row["text"], truncation=True, padding="max_length", max_length=512)
        
    train = dataset.map(chat_format, batched=False, num_proc=4)
    
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

    try:
        training_args = TrainingArguments(
            seed=42,
            output_dir=os.path.join(base_path, 'result'),
            num_train_epochs=3,
            per_device_train_batch_size=1,  # vram 부족할 시 감소
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
            model=model.model,
            train_dataset=train['train'],
            args=training_args,
            peft_config=lora_config,
            # formatting_func=lambda x: x['input_ids']
        )

        trainer.train()
    except RuntimeError as e:
            print(f"배치 크기에서 VRAM 부족: {e}")
    
    trainer.model.save_pretrained(os.path.join(base_path, 'workspace/lora-adapter-epoch3'))
    print(f'./workspace/에 저장되었습니다.')