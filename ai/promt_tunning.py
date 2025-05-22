from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments,
    BitsAndBytesConfig,
)
from peft import PromptTuningConfig, get_peft_model
from trl import SFTTrainer
from datasets import Dataset, concatenate_datasets
import torch
import os
from glob import glob

base_path = '/home/apic/python/advanture_game'
model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True
    )

# 모델 및 토크나이저 로드
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    cache_dir=os.path.join(base_path, 'workspace/cache'),
    torch_dtype=torch.float16,  # 데이터 타입 명시
    device_map='auto',  # device_map 제거 또는 None 설정
    quantization_config = bnb_config
)
tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    cache_dir=os.path.join(base_path, 'workspace/cache'),
)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = 'right'

# Prompt Tuning 설정
prompt_config = PromptTuningConfig(
    task_type="CAUSAL_LM",
    num_virtual_tokens=20,
)
model = get_peft_model(model, prompt_config)


# 데이터셋 로드
train_files = glob(os.path.join(base_path, 'data/data_files/npc_instruction/npc_god.json'))
datasets = [Dataset.from_json(file) for file in train_files]
train = concatenate_datasets(datasets)

def prompting(instruction, input, output):
    return f"<설정>\n{instruction}\n\n<대화>\n질문: {input}\n답변: {output}\n"

def chat_format(row):
    # 입력 포맷 생성
    prompt = prompting(row["instruction"], row["input_ids"], row["output"])
    
    # 토큰화
    tokens = tokenizer(prompt, truncation=True, padding="max_length", max_length=1024)
    
    # 정답 시퀀스 생성
    output_tokens = tokenizer(row["output"], truncation=True, padding="max_length", max_length=1024)["input_ids"]
    
    # 레이블 처리: `tokens["input_ids"]`와 길이를 맞춤
    labels = [-100] * len(tokens["input_ids"])
    labels[:len(output_tokens)] = output_tokens
    
    # 데이터셋에 추가
    row["input_ids"] = tokens["input_ids"]
    row["attention_mask"] = tokens["attention_mask"]
    row["labels"] = labels
    return row

class CustomTrainer(SFTTrainer):
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits

        shift_logits = logits[..., :-1, :].contiguous()
        shift_labels = labels[..., 1:].contiguous()

        # 시퀀스 길이 맞추기
        min_len = min(shift_logits.size(1), shift_labels.size(1))
        shift_logits = shift_logits[:, :min_len, :]
        shift_labels = shift_labels[:, :min_len]

        loss_fct = torch.nn.CrossEntropyLoss(ignore_index=-100)
        loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))

        return (loss, outputs) if return_outputs else loss

train = train.map(chat_format, batched=False, num_proc=4)

# 학습 설정
training_args = TrainingArguments(
    output_dir=os.path.join(base_path, "result"),
    num_train_epochs=20,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    optim="paged_adamw_32bit",
    logging_steps=10,
    save_steps=50,
    fp16=True,
)
model.gradient_checkpointing_enable()


# trainer = SFTTrainer(
#     model=model,
#     train_dataset=train,
#     args=training_args,
#     peft_config=prompt_config,
# ) 

# CustomTrainer 정의
trainer = CustomTrainer(
    model=model,
    train_dataset=train,
    args=training_args,
    peft_config=prompt_config,
)

trainer.train()

# 모델 저장
trainer.model.save_pretrained(os.path.join(base_path, 'workspace/prompt-tuning-adapter'))
print(f"모델이 저장되었습니다.")
