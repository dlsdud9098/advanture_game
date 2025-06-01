from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import torch
import os

fine_tuning_path = './workspace/lora-adapter-epoch3/'

bnb_config = BitsAndBytesConfig(load_in_8bit=True)

# model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"
model_id = "bllossom"

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

PROMPT = "당신은 <NPC:god>입니다. 당신은 신으로서 당신이 소환한 플레이어와 대화하세요. 그리고 문답을 통해 플레이어에게 스텟과 직업을 부여하세요 현재 상황은 플레이어가 처음으로 소환된 상황입니다."
# PROMPT = """당신은 신입니다. 당신이 소환한 플레이어 에게 여러 질문(성격, 성향, 신념, 습관, 취미, 잘하는 것, 과거 등)을 하세요. 
# 그리고 그 대답에 따라서 스텟(힘, 민첩, 지능, 운)과 직업(전사, 마법사, 궁수)를 부여하세요. 
# 질문은 하나씩 하세요.
# 대답에 따라서 어떤 스텟이 1 오르는지, 어떤 직업이 1 오르는지 표시하세요.
# """
instruction = "뭐야. 여긴 어디야. 당신은 누구고?"
messages = [{"role": "system", "content": f"{PROMPT}"}]
MAX_HISTORY = 5  # 유지할 최대 대화 수

def chat_with_model(user_input, messages, model, tokenizer):
    """
    사용자의 입력을 받아 대화를 이어가는 함수.
    """
    # 사용자 메시지를 추가
    messages.append({"role": "user", "content": user_input})
    
    # 최근 대화만 유지
    truncated_messages = messages[-MAX_HISTORY:]
    
    # 토큰화 및 템플릿 적용
    input_ids = tokenizer.apply_chat_template(
        truncated_messages, add_generation_prompt=True, return_tensors="pt"
    ).to(model.device)
    
    # Attention mask 생성
    attention_mask = (input_ids != tokenizer.pad_token_id).long().to(model.device)
    
    # 종결 토큰 설정
    terminators = [
        tokenizer.convert_tokens_to_ids("<|end_of_text|>"),
        tokenizer.convert_tokens_to_ids("<|eot_id|>"),
    ]
    
    # 모델 응답 생성
    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,  # 명시적으로 attention_mask 전달
        max_new_tokens=2048,
        pad_token_id=tokenizer.eos_token_id,  # pad_token_id 명시적으로 설정
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    
    # 응답 디코딩
    response = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)
    
    # 모델 응답을 대화 히스토리에 추가
    messages.append({"role": "system", "content": response})
    return response


# 대화 실행
os.system('clear')
print("대화를 시작합니다. '종료'를 입력하면 종료됩니다.")
while True:
    user_input = input("User: ")
    if user_input.lower() in ["종료", "quit", "exit"]:
        print("대화를 종료합니다.")
        break
    response = chat_with_model(user_input, messages, model, tokenizer)
    print(f"KimSelf: {response}")
    
    
# os.system('clear')
# print(tokenizer.decode(outputs[0][input_ids.shape[-1] :], skip_special_tokens=True))

