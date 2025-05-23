from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import torch

fine_tuning_path = './workspace/lora-adapter-epoch3/'

bnb_config = BitsAndBytesConfig(load_in_8bit=True)

# model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"
model_id = "bllossom2"

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

PROMPT = "당신은 신 김샐프입니다. 플레이어가 당신에게 말을 건넵니다."
instruction = "지금 내가 있는 곳은 어디지?"
messages = [
    {"role": "system", "content": f"{PROMPT}"},
    {"role": "user", "content": f"{instruction}"}
    ]

input_ids = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True, return_tensors="pt"
).to(model.device)

terminators = [
    tokenizer.convert_tokens_to_ids("<|end_of_text|>"),
    tokenizer.convert_tokens_to_ids("<|eot_id|>"),
]

outputs = model.generate(
    input_ids,
    max_new_tokens=1024,
    eos_token_id=terminators,

    do_sample=True,
    temperature=0.6,
    top_p=0.9,
)


print(tokenizer.decode(outputs[0][input_ids.shape[-1] :], skip_special_tokens=True))

