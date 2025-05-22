from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

base_model_name = "Bllossom/llama-3.2-Korean-Bllossom-3B"
peft_model_dir = "workspace/prompt-tuning-adapter"

tokenizer = AutoTokenizer.from_pretrained(base_model_name)

bnb_config = BitsAndBytesConfig(load_in_8bit=True)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    quantization_config=bnb_config,
    device_map='auto',
    cache_dir='./workspace/cache'
    )
model = PeftModel.from_pretrained(base_model, peft_model_dir)
model.to('cuda')
model.eval()

while True:
    prompt = input('입력: ')
    # 추론
    # prompt = "안녕하세요, 당신의 이름은 무엇인가요?"
    inputs = tokenizer(prompt, return_tensors="pt").to('cuda')
    outputs = model.generate(
        **inputs, 
        max_length=100,
        no_repeat_ngram_size=3,
        temperature=0.8,
        top_p=0.9,
        repetition_penalty=1.2,
        pad_token_id=tokenizer.pad_token_id
        )
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
