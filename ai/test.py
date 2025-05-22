from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import torch
from glob import glob

fine_tuning_path = './workspace/lora-adapter-epoch3/'

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True
)

# 모델 이름
model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"

# 기본 모델 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_id)
base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map='auto',
    cache_dir = './workspace/cache'
    # adapter_path = fine_tuning_path
)

# LoRA Adapter 결합
model = PeftModel.from_pretrained(base_model, fine_tuning_path)

def prompt(instruction, input_text):
    # 입력 텍스트 구성
    prompt = f"{instruction}\n\n{input_text}\n\n"

    inputs = tokenizer(prompt, return_tensors="pt")

    # 입력 데이터를 GPU로 이동
    inputs = {key: value.to('cuda') for key, value in inputs.items()}
    
    outputs = model.generate(**inputs, max_length=512, do_sample=True, temperature=0.7)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return result


instruction = "플레이어가 소환되었습니다."
input_text = '''
넌 뭐야?
'''

result = prompt(instruction, input_text)

print(result)