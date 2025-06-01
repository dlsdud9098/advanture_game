import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import json

class SimpleNPCChat:
    """콘솔용 간단한 NPC 채팅 시스템"""
    
    def __init__(self, base_model_id, adapter_path, npc_data_path=None):
        self.base_model_id = base_model_id
        self.adapter_path = adapter_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # NPC 기본 정보 (JSON 파일이 없을 경우 사용)
        # self.npc_info = {
        #     "name": "신 김샐프",
        #     "display_name": "신 김샐프",
        #     "personality": "다정하고 엄격한 신",
        #     "role": "플레이어의 스탯과 직업을 결정하는 신"
        # }
        
        # NPC 데이터가 있으면 로드
        if npc_data_path and os.path.exists(npc_data_path):
            with open(npc_data_path, 'r', encoding='utf-8') as f:
                npc_data = json.load(f)
                self.npc_info = {
                    "name": npc_data['basic_info']['name'],
                    "display_name": npc_data['basic_info']['display_name'],
                    "personality": ', '.join(npc_data['personality']['primary_traits']),
                    "role": npc_data['role_and_function']['primary_role']
                }
        
        self.model = None
        self.tokenizer = None
        self.conversation_history = []
        
        self.load_model()
        
    def load_model(self):
        """모델 로드"""
        print("🤖 모델 로딩 중... (시간이 좀 걸릴 수 있습니다)")
        
        try:
            # 토크나이저 로드
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_id)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # 베이스 모델 로드
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_id,
                torch_dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True
            )
            
            # LoRA 어댑터 로드
            self.model = PeftModel.from_pretrained(base_model, self.adapter_path)
            self.model.eval()
            
            print(f"✅ {self.npc_info['display_name']} 준비 완료!")
            
        except Exception as e:
            print(f"❌ 모델 로딩 실패: {e}")
            print("파인튜닝된 모델이 있는지 확인해주세요.")
            return False
        
        return True
    
    def generate_response(self, user_input):
        """사용자 입력에 대한 NPC 응답 생성"""
        
        # 시스템 프롬프트
        system_prompt = f"""당신은 게임 '어드벤처 월드'의 NPC '{self.npc_info['display_name']}'입니다.
성격: {self.npc_info['personality']}
역할: {self.npc_info['role']}

이 캐릭터로서 자연스럽게 대화해주세요. 정중한 존댓말을 사용하고, 플레이어를 '용사님'이라고 부르세요."""
        
        # 대화 형식 구성
        conversation = f"<|system|>\n{system_prompt}\n"
        
        # 최근 대화 히스토리 추가 (최대 3개)
        for history in self.conversation_history[-3:]:
            conversation += f"<|user|>\n{history['user']}\n<|assistant|>\n{history['assistant']}\n"
        
        # 현재 사용자 입력
        conversation += f"<|user|>\n{user_input}\n<|assistant|>\n"
        
        try:
            # 토크나이징
            inputs = self.tokenizer.encode(conversation, return_tensors="pt").to(self.device)
            
            # 응답 생성
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=200,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )
            
            # 응답 디코딩
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # 새로 생성된 부분만 추출
            response = full_response[len(conversation):].strip()
            
            # 불필요한 토큰 제거
            if "<|endoftext|>" in response:
                response = response.split("<|endoftext|>")[0].strip()
            if "<|user|>" in response:
                response = response.split("<|user|>")[0].strip()
            
            return response
            
        except Exception as e:
            print(f"❌ 응답 생성 실패: {e}")
            return "죄송합니다. 일시적인 문제가 발생했습니다."
    
    def chat(self, user_input):
        """대화 처리"""
        response = self.generate_response(user_input)
        
        # 대화 히스토리에 추가
        self.conversation_history.append({
            "user": user_input,
            "assistant": response
        })
        
        return response
    
    def reset_conversation(self):
        """대화 히스토리 초기화"""
        self.conversation_history = []
        print("💭 대화 히스토리가 초기화되었습니다.")

def main():
    """메인 실행 함수"""
    
    # 설정
    base_model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"
    adapter_path = "workspace/npc-god-adapter"
    npc_data_path = "data/npcs/npc_god.json"  # 없어도 동작함
    
    # 파일 존재 확인
    if not os.path.exists(adapter_path):
        print(f"❌ 파인튜닝된 모델을 찾을 수 없습니다: {adapter_path}")
        print("먼저 fine_tune_npc.py를 실행하여 모델을 훈련해주세요.")
        return
    
    print("🎮 어드벤처 월드 - NPC 채팅 시스템")
    print("="*50)
    
    # NPC 채팅 시스템 초기화
    npc_chat = SimpleNPCChat(base_model_id, adapter_path, npc_data_path)
    
    if npc_chat.model is None:
        return
    
    print("\n명령어:")
    print("- 'quit' 또는 'exit': 종료")
    print("- 'reset': 대화 히스토리 초기화") 
    print("- 'help': 도움말")
    print("- 그 외: NPC와 대화")
    print("="*50)
    
    # 환영 메시지
    welcome_msg = npc_chat.chat("안녕하세요")
    print(f"\n⭐ {npc_chat.npc_info['display_name']}: {welcome_msg}\n")
    
    # 대화 루프
    while True:
        try:
            user_input = input("👤 당신: ").strip()
            
            # 종료 명령
            if user_input.lower() in ['quit', 'exit', '종료', 'q']:
                print(f"\n⭐ {npc_chat.npc_info['display_name']}: 안녕히 가세요, 용사님!")
                break
            
            # 초기화 명령
            if user_input.lower() in ['reset', '초기화']:
                npc_chat.reset_conversation()
                continue
            
            # 도움말
            if user_input.lower() in ['help', '도움말']:
                print("\n📋 사용 가능한 명령어:")
                print("- quit/exit: 프로그램 종료")
                print("- reset: 대화 기록 삭제")
                print("- help: 이 도움말 표시")
                print("- 일반 텍스트: NPC와 대화\n")
                continue
            
            # 빈 입력 무시
            if not user_input:
                continue
            
            # NPC 응답 생성
            print("🤔 (생각 중...)", end="", flush=True)
            response = npc_chat.chat(user_input)
            print(f"\r⭐ {npc_chat.npc_info['display_name']}: {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n⭐ {npc_chat.npc_info['display_name']}: 갑작스럽게 떠나시는군요. 안녕히 가세요!")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            print("다시 시도해주세요.\n")

if __name__ == "__main__":
    main()