import os
import torch
from datasets import Dataset, concatenate_datasets, load_dataset
from torch.utils.data import DataLoader
from torch.cuda.amp import autocast
from tqdm import tqdm

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
from fine_tune_to_llm import fine_tune_llm
from dynamicdataset import DynamicDataset

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

    # 모델 id
    model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"

    os.makedirs(name=os.path.join(base_path, 'workspace/cache'), exist_ok=os.path.join(base_path, 'workspace/cache'))
    # 모델 불러오기
    base_model = AutoModelForCausalLM.from_pretrained(
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

    # 데이터 불러오기
    files = []
    files.extend(glob('data/data_files/npc_instruction/*.txt'))
    files.extend(glob('data/data_files/other_instruction/*.txt'))
    
    batch_size = 1
    train_dataset = DynamicDataset(files, tokenizer)
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, num_workers=4)
    
    # LoRA 설정
    lora_config = LoraConfig(
        r=8,
        lora_alpha = 32,
        lora_dropout = 0.1,
        target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
        task_type="CAUSAL_LM",
    )
    
    base_model = get_peft_model(base_model, lora_config)
    base_model.train()  # 학습 모드로 변환
    os.system('clear')

    try:
        optimizer = torch.optim.AdamW(base_model.parameters(), lr=2e-4)
        
        base_model.train()
        # scaler = torch.cuda.amp.GradScaler()
        num_epochs = 5
        
        total_loss = 0
        total_correct = 0
        total_tokens = 0
        for epoch in range(num_epochs):
            pbar = tqdm(train_dataloader, desc=f"Epoch {epoch+1}/{num_epochs}")
            
            for batch in pbar:
                optimizer.zero_grad()
                inputs = {key: val.to("cuda") for key, val in batch.items()}
                # with autocast():
                outputs = base_model(**inputs)
                loss = outputs.loss
                
                # scaler.scale(loss).backward()
                # scaler.step(optimizer)
                # scaler.update()
                optimizer.step()
                loss.backward()
                
                total_loss += loss.item() * inputs['input_ids'].size(0)  # 배치 단위 loss 합산

                # 예측 결과 계산 (logits -> argmax)
                logits = outputs.logits  # (batch_size, seq_len, vocab_size)
                predictions = logits.argmax(dim=-1)  # (batch_size, seq_len)

                # 정답(labels)과 비교해서 정확도 계산
                labels = inputs['labels']
                mask = inputs['attention_mask'].bool()

                correct = ((predictions == labels) & mask).sum().item()
                total_correct += correct
                total_tokens += mask.sum().item()
                
            avg_loss = total_loss / total_tokens  # 전체 데이터 수로 나눠 평균 loss 계산
            accuracy = total_correct / total_tokens if total_tokens > 0 else 0

            print(f"Epoch {epoch+1}/{num_epochs} - Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")
            
        adapter_save_path = os.path.join(base_path, 'workspace/lora-adapter-epoch3')

        # torch.cuda.empty_cache()
        base_model.save_pretrained(adapter_save_path)
        tokenizer.save_pretrained(adapter_save_path)
        
        print(f'./workspace/에 저장되었습니다.')
        
        if os.path.exists(adapter_save_path):
            fine_tune_llm()

    except RuntimeError as e:
            print(f"배치 크기에서 VRAM 부족: {e}")
    
    
