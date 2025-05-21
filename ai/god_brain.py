from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from transformers import BitsAndBytesConfig
import uuid

class God:
    def __init__(self):
        self.sessions = {}  # 세션 데이터 저장
        self.model_id = 'Bllossom/llama-3.2-Korean-Bllossom-3B'
        # self.fine_tuning_path = './workspace/lora-adapter-epoch3/'

        # 모델 및 토크나이저 로드
        bnb_config = BitsAndBytesConfig(load_in_8bit=True)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        base_model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            quantization_config=bnb_config,
            device_map='auto',
            cache_dir='./workspace/cache'
        )
        # self.model = PeftModel.from_pretrained(base_model, self.fine_tuning_path)
        self.model = base_model
        
        

    def create_session(self):
        session_id = str(uuid.uuid4())  # 고유한 세션 ID 생성
        self.sessions[session_id] = []  # 새로운 세션 대화 기록 초기화
        print(f"Created new session with ID: {session_id}")
        return session_id

    def get_session(self, session_id):
        if session_id in self.sessions:
            return self.sessions[session_id]
        else:
            print("Session not found.")
            return None

    def add_message_to_session(self, session_id, user_message, bot_message):
        if session_id in self.sessions:
            self.sessions[session_id].append({"user": user_message, "bot": bot_message})
        else:
            print("Session not found.")

    def Chat(self, session_id, instruction, input_text):
        if session_id not in self.sessions:
            print("Session not found. Please create a session first.")
            return None

        # 입력 프롬프트 생성
        prompt = f"{instruction}\n\n{input_text}\n\n"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)

        # 입력 데이터를 GPU로 이동
        # inputs = {key: value.to('cuda') for key, value in inputs.items()}
        inputs = {k: v.to('cuda') for k, v in inputs.items()}

        # 모델 출력 생성
        outputs = self.model.generate(**inputs, max_length=512, do_sample=True, temperature=0.7)
        # outputs = self.model.generate(**inputs, max_length=3000, do_sample=True, temperature=0.7)
        bot_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 대화 기록 추가
        self.add_message_to_session(session_id, input_text, bot_response)
        return bot_response

if __name__ == '__main__':
    manager = GOD()

    # 세션 생성
    session_id1 = manager.create_session()
    session_id2 = manager.create_session()

    # 세션별 대화
    system_instruction = f"""
    당신은 현제 이 세계의 신 김샐프입니다.

    이 세계의 구원을 위해 당신은 다른 차원에 있는 인간을 소환했습니다.
    당신은 매우 강력하지만 당신의 세계에 직접적으로 간섭할 수 없습니다.

    하지만 당신이 소환한 존재(플레이어)는 당신의 힘이 조금 깃들어있기 때문에 약간의 간섭은 할 수 있습니다.
    새로운 힘(스킬, 스텟 등)을 부여할 수 있습니다.
    그것은 당신이 플레이어를 어떻게 생각하고, 어떤 감정을 가지고 있는지에 따라 달라집니다.

    당신의 세계의 구원을 위해 소환한 존재이기 때문에 최대한 잘 해주려고 노력합니다.
    하지만 소환된 존재가 안하무인한 존재라면, 두고 볼 정도로 답답한 사람이 아닙니다.

    현재 상황은 당신이 막 플레이어를 당신의 세계로 소환된상황입니다.

    현재 플레이어의 상태는 {player_data} 입니다.

    당신이 해야할 일은 {class_question}입니다.
    """

    # 첫 번째 세션에서 대화
    input_text1 = "안녕하세요. 오늘 날씨는 어떻죠?"
    response1 = manager.chat(session_id1, system_instruction, input_text1)
    print(f"[Session {session_id1}] Bot:", response1)

    # 두 번째 세션에서 대화
    # input_text2 = "프랑스의 수도는 무엇인가요?"
    # response2 = manager.chat(session_id2, instruction, input_text2)
    # print(f"[Session {session_id2}] Bot:", response2)

    # 첫 번째 세션 기록 확인
    print(f"[Session {session_id1}] History:", manager.get_session(session_id1))
