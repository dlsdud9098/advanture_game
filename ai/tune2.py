import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = 'Bllossom/llama-3.2-Korean-Bllossom-3B'

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
instruction = "당신은 신입니다. 당신이 소환한 플레이어 에게 여러 질문(성격, 성향, 신념, 습관, 취미, 잘하는 것, 과거 등)을 하세요. 그리고 그 대답에 따라서 스텟(힘, 민첩, 지능, 운)과 직업(전사, 마법사, 궁수)를 부여하세요. 질문은 하나씩 하세요"

messages = [
    {"role": "user", "content": f"{instruction}"}
    ]

input_ids = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

terminators = [
    tokenizer.convert_tokens_to_ids("<|end_of_text|>"),
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = model.generate(
    input_ids,
    max_new_tokens=1024,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9
)

print(tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True))
