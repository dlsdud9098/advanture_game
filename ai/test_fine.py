from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import torch

fine_tuning_path = './workspace/lora-adapter-epoch3/'

bnb_config = BitsAndBytesConfig(load_in_8bit=True)

model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"

tokenizer = AutoTokenizer.from_pretrained(model_id)

base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map='auto',
    cache_dir='./workspace/cache'
)

model = PeftModel.from_pretrained(base_model, fine_tuning_path)
model.to('cuda')
model.eval()

def prompt(instruction, input_text):
    prompt_text = f"instruction: {instruction}\n\ninput: {input_text}\n\noutput: "
    inputs = tokenizer(prompt_text, return_tensors="pt", truncation=True, max_length=2048)
    inputs = {k: v.to('cuda') for k, v in inputs.items()}
    
    outputs = model.generate(**inputs, max_length=512, do_sample=True, temperature=0.7, top_p=0.9, no_repeat_ngram_size=2)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 불필요한 프롬프트 부분 제외 (필요 시)
    response = result[len(prompt_text):].strip()
    
    return response

instruction = "당신에게 말을 건넵니다."
input_text = "지금 내가 있는 곳은 어디지?"

print(prompt(instruction, input_text))
