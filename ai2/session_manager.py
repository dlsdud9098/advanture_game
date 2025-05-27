"""
NPC AI 세션 관리자
각 NPC별로 독립적인 대화 세션을 관리하고 추론을 수행하는 모듈
"""

import os
import torch
import uuid
import json
from typing import Dict, List, Any, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import logging

logger = logging.getLogger(__name__)


class NPCSessionManager:
    def __init__(self, 
                 model_path: str = None,
                 base_model_name: str = "Bllossom/llama-3.2-Korean-Bllossom-3B",
                 base_path: str = "/home/apic/python/advanture_game"):
        
        self.base_path = base_path
        self.base_model_name = base_model_name
        self.model_path = model_path or os.path.join(base_path, "workspace", "npc_model")
        self.cache_dir = os.path.join(base_path, "workspace", "cache")
        
        # 세션 저장소
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        # 모델 및 토크나이저
        self.tokenizer = None
        self.model = None
        
        # NPC 설정 데이터
        self.npc_configs = self._load_npc_configs()
        
        # 모델 로드
        self._load_model()
        
    def _load_npc_configs(self) -> Dict[str, str]:
        """NPC 설정 파일들을 로드"""
        configs = {}
        npc_path = os.path.join(self.base_path, "data", "data_files", "npc_instruction")
        
        if os.path.exists(npc_path):
            for file_name in os.listdir(npc_path):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(npc_path, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        npc_name = file_name.replace('.txt', '')
                        configs[npc_name] = content
                        
        return configs
        
    def _load_model(self):
        """모델과 토크나이저 로드"""
        logger.info("모델 로드 중...")
        
        try:
            # 토크나이저 로드
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.base_model_name,
                cache_dir=self.cache_dir
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # 파인튜닝된 모델이 있는지 확인
            if os.path.exists(self.model_path) and os.path.exists(os.path.join(self.model_path, "adapter_config.json")):
                logger.info(f"파인튜닝된 모델 로드: {self.model_path}")
                
                # 베이스 모델 로드
                bnb_config = BitsAndBytesConfig(
                    load_in_8bit=True,
                    llm_int8_enable_fp32_cpu_offload=True
                )
                
                base_model = AutoModelForCausalLM.from_pretrained(
                    self.base_model_name,
                    quantization_config=bnb_config,
                    device_map="auto",
                    cache_dir=self.cache_dir,
                    torch_dtype=torch.float16
                )
                
                # LoRA 어댑터 로드
                self.model = PeftModel.from_pretrained(base_model, self.model_path)
                
            else:
                logger.info("베이스 모델만 로드")
                
                bnb_config = BitsAndBytesConfig(
                    load_in_8bit=True,
                    llm_int8_enable_fp32_cpu_offload=True
                )
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.base_model_name,
                    quantization_config=bnb_config,
                    device_map="auto",
                    cache_dir=self.cache_dir,
                    torch_dtype=torch.float16
                )
                
            self.model.eval()  # 추론 모드
            logger.info("모델 로드 완료")
            
        except Exception as e:
            logger.error(f"모델 로드 실패: {e}")
            raise e
    
    def create_npc_session(self, npc_type: str, player_data: Dict[str, Any] = None) -> str:
        """NPC 세션 생성"""
        session_id = str(uuid.uuid4())
        
        # NPC 설정 가져오기
        npc_config = self.npc_configs.get(npc_type, "")
        if not npc_config:
            logger.warning(f"NPC 설정을 찾을 수 없음: {npc_type}")
            npc_config = "일반적인 NPC입니다."
        
        # 시스템 프롬프트 생성
        system_prompt = self._create_system_prompt(npc_config, player_data)
        
        # 세션 데이터 생성
        session_data = {
            "npc_type": npc_type,
            "system_prompt": system_prompt,
            "conversation_history": [],
            "player_data": player_data or {},
            "created_at": torch.cuda.current_device() if torch.cuda.is_available() else 0
        }
        
        self.sessions[session_id] = session_data
        logger.info(f"NPC 세션 생성: {session_id} (타입: {npc_type})")
        
        return session_id
    
    def _create_system_prompt(self, npc_config: str, player_data: Dict[str, Any] = None) -> str:
        """시스템 프롬프트 생성"""
        prompt = f"""당신은 게임 세계의 NPC입니다.

NPC 설정:
{npc_config}

"""
        
        if player_data:
            prompt += f"""현재 플레이어 정보:
{json.dumps(player_data, ensure_ascii=False, indent=2)}

"""
        
        # 상황 설정 추가
        situation_path = os.path.join(self.base_path, "data", "data_files", "other_instruction", "player_spawn.txt")
        if os.path.exists(situation_path):
            with open(situation_path, 'r', encoding='utf-8') as f:
                situation = f.read().strip()
                prompt += f"""현재 상황:
{situation}

"""
        
        prompt += """지침:
1. 위의 NPC 설정에 맞게 일관되게 행동하세요.
2. 플레이어와 자연스럽고 몰입감 있는 대화를 나누세요.
3. 캐릭터의 성격과 역할에 맞는 말투와 행동을 보여주세요.
4. 게임 세계관에 맞는 응답을 제공하세요.
5. 응답은 한국어로 해주세요.
"""
        
        return prompt
    
    def chat_with_npc(self, session_id: str, user_input: str, max_length: int = 512) -> str:
        """NPC와 대화"""
        if session_id not in self.sessions:
            logger.error(f"세션을 찾을 수 없음: {session_id}")
            return "세션을 찾을 수 없습니다."
        
        session = self.sessions[session_id]
        
        try:
            # 대화 기록 구성
            conversation_text = self._build_conversation_text(session, user_input)
            
            # 토크나이징
            inputs = self.tokenizer(
                conversation_text,
                return_tensors="pt",
                truncation=True,
                max_length=2048
            )
            
            # GPU로 이동
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            # 추론 실행
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # 응답 디코딩
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # 입력 부분 제거하여 응답만 추출
            assistant_response = self._extract_assistant_response(response, conversation_text)
            
            # 대화 기록 업데이트
            session["conversation_history"].append({
                "user": user_input,
                "assistant": assistant_response
            })
            
            logger.info(f"NPC 응답 생성 완료: {session_id}")
            return assistant_response
            
        except Exception as e:
            logger.error(f"NPC 대화 중 오류: {e}")
            return "죄송합니다. 응답을 생성하는 중 오류가 발생했습니다."
    
    def _build_conversation_text(self, session: Dict[str, Any], user_input: str) -> str:
        """대화 텍스트 구성"""
        system_prompt = session["system_prompt"]
        history = session["conversation_history"]
        
        # ChatML 형식으로 구성
        conversation = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_prompt}<|eot_id|>"
        
        # 이전 대화 기록 추가
        for turn in history[-5:]:  # 최근 5턴만 유지
            conversation += f"<|start_header_id|>user<|end_header_id|>\n{turn['user']}<|eot_id|>"
            conversation += f"<|start_header_id|>assistant<|end_header_id|>\n{turn['assistant']}<|eot_id|>"
        
        # 현재 사용자 입력 추가
        conversation += f"<|start_header_id|>user<|end_header_id|>\n{user_input}<|eot_id|>"
        conversation += f"<|start_header_id|>assistant<|end_header_id|>\n"
        
        return conversation
    
    def _extract_assistant_response(self, full_response: str, input_text: str) -> str:
        """전체 응답에서 어시스턴트 응답 부분만 추출"""
        try:
            # 입력 텍스트 이후의 내용만 추출
            if input_text in full_response:
                response_part = full_response.split(input_text)[-1]
            else:
                response_part = full_response
            
            # 어시스턴트 응답 시작 부분 찾기
            if "<|start_header_id|>assistant<|end_header_id|>" in response_part:
                response_part = response_part.split("<|start_header_id|>assistant<|end_header_id|>")[-1]
            
            # 종료 토큰 제거
            response_part = response_part.replace("<|eot_id|>", "").replace("<|end_of_text|>", "")
            
            # 앞뒤 공백 제거
            response_part = response_part.strip()
            
            return response_part if response_part else "..."
            
        except Exception as e:
            logger.error(f"응답 추출 중 오류: {e}")
            return "응답을 처리하는 중 오류가 발생했습니다."
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 정보 조회"""
        return self.sessions.get(session_id)
    
    def update_player_data(self, session_id: str, player_data: Dict[str, Any]):
        """세션의 플레이어 데이터 업데이트"""
        if session_id in self.sessions:
            self.sessions[session_id]["player_data"] = player_data
            # 시스템 프롬프트도 업데이트
            npc_config = self.npc_configs.get(self.sessions[session_id]["npc_type"], "")
            self.sessions[session_id]["system_prompt"] = self._create_system_prompt(npc_config, player_data)
    
    def delete_session(self, session_id: str):
        """세션 삭제"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"세션 삭제: {session_id}")
    
    def list_sessions(self) -> List[str]:
        """활성 세션 목록 반환"""
        return list(self.sessions.keys())
    
    def clear_all_sessions(self):
        """모든 세션 삭제"""
        self.sessions.clear()
        logger.info("모든 세션이 삭제되었습니다.")


# 편의를 위한 단일 인스턴스 생성
_session_manager = None

def get_session_manager() -> NPCSessionManager:
    """세션 매니저 싱글톤 인스턴스 반환"""
    global _session_manager
    if _session_manager is None:
        _session_manager = NPCSessionManager()
    return _session_manager


if __name__ == "__main__":
    # 테스트 코드
    manager = NPCSessionManager()
    
    # 테스트용 플레이어 데이터
    test_player_data = {
        "name": "테스트_플레이어",
        "lv": 1,
        "class": "미정",
        "hp": 100,
        "mp": 50
    }
    
    # 신 NPC 세션 생성
    session_id = manager.create_npc_session("npc_god", test_player_data)
    print(f"세션 생성: {session_id}")
    
    # 대화 테스트
    response = manager.chat_with_npc(session_id, "안녕하세요, 신님!")
    print(f"NPC 응답: {response}")
    
    # 세션 정보 확인
    session_info = manager.get_session_info(session_id)
    print(f"세션 정보: {session_info['npc_type']}")
