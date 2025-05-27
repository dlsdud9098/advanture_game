"""
GUI와 AI 시스템을 연결하는 브릿지 모듈
"""

import json
from typing import Dict, Any, Optional
from .session_manager import get_session_manager
import logging

logger = logging.getLogger(__name__)


class NPCAIBridge:
    """GUI와 AI 시스템 간의 브릿지 클래스"""
    
    def __init__(self):
        self.session_manager = get_session_manager()
        self.current_sessions: Dict[str, str] = {}  # npc_type -> session_id 매핑
        
    def start_npc_conversation(self, npc_type: str, player_data: Dict[str, Any]) -> str:
        """NPC와의 대화 시작"""
        try:
            # 기존 세션이 있다면 삭제
            if npc_type in self.current_sessions:
                old_session_id = self.current_sessions[npc_type]
                self.session_manager.delete_session(old_session_id)
            
            # 새 세션 생성
            session_id = self.session_manager.create_npc_session(npc_type, player_data)
            self.current_sessions[npc_type] = session_id
            
            logger.info(f"NPC 대화 시작: {npc_type} -> {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"NPC 대화 시작 실패: {e}")
            return None
    
    def send_message_to_npc(self, npc_type: str, message: str) -> str:
        """NPC에게 메시지 전송"""
        try:
            if npc_type not in self.current_sessions:
                logger.error(f"활성 세션이 없음: {npc_type}")
                return "대화를 먼저 시작해주세요."
            
            session_id = self.current_sessions[npc_type]
            response = self.session_manager.chat_with_npc(session_id, message)
            
            logger.info(f"NPC 메시지 전송 완료: {npc_type}")
            return response
            
        except Exception as e:
            logger.error(f"NPC 메시지 전송 실패: {e}")
            return "메시지 전송 중 오류가 발생했습니다."
    
    def update_player_data(self, npc_type: str, player_data: Dict[str, Any]):
        """플레이어 데이터 업데이트"""
        try:
            if npc_type in self.current_sessions:
                session_id = self.current_sessions[npc_type]
                self.session_manager.update_player_data(session_id, player_data)
                logger.info(f"플레이어 데이터 업데이트: {npc_type}")
                
        except Exception as e:
            logger.error(f"플레이어 데이터 업데이트 실패: {e}")
    
    def end_npc_conversation(self, npc_type: str):
        """NPC와의 대화 종료"""
        try:
            if npc_type in self.current_sessions:
                session_id = self.current_sessions[npc_type]
                self.session_manager.delete_session(session_id)
                del self.current_sessions[npc_type]
                logger.info(f"NPC 대화 종료: {npc_type}")
                
        except Exception as e:
            logger.error(f"NPC 대화 종료 실패: {e}")
    
    def get_active_sessions(self) -> Dict[str, str]:
        """활성 세션 목록 반환"""
        return self.current_sessions.copy()
    
    def is_session_active(self, npc_type: str) -> bool:
        """세션 활성 상태 확인"""
        return npc_type in self.current_sessions


# GUI에서 사용할 전역 브릿지 인스턴스
_ai_bridge = None

def get_ai_bridge() -> NPCAIBridge:
    """AI 브릿지 싱글톤 인스턴스 반환"""
    global _ai_bridge
    if _ai_bridge is None:
        _ai_bridge = NPCAIBridge()
    return _ai_bridge


class GameAIController:
    """게임 메인 UI에서 사용할 AI 컨트롤러"""
    
    def __init__(self):
        self.ai_bridge = get_ai_bridge()
        self.current_npc = None
        
    def initialize_god_conversation(self, player_data: Dict[str, Any]) -> str:
        """신 NPC와의 대화 초기화"""
        try:
            session_id = self.ai_bridge.start_npc_conversation("npc_god", player_data)
            if session_id:
                self.current_npc = "npc_god"
                # 초기 인사말 생성
                initial_response = self.ai_bridge.send_message_to_npc("npc_god", "처음 만나뵙겠습니다.")
                return initial_response
            else:
                return "AI 시스템 초기화에 실패했습니다."
                
        except Exception as e:
            logger.error(f"신 대화 초기화 실패: {e}")
            return "대화 초기화 중 오류가 발생했습니다."
    
    def send_player_message(self, message: str) -> str:
        """플레이어 메시지를 현재 NPC에게 전송"""
        if not self.current_npc:
            return "대화할 NPC가 선택되지 않았습니다."
        
        return self.ai_bridge.send_message_to_npc(self.current_npc, message)
    
    def update_player_status(self, player_data: Dict[str, Any]):
        """플레이어 상태 업데이트"""
        if self.current_npc:
            self.ai_bridge.update_player_data(self.current_npc, player_data)
    
    def switch_npc(self, npc_type: str, player_data: Dict[str, Any]) -> str:
        """다른 NPC로 전환"""
        try:
            # 기존 NPC와의 대화 종료
            if self.current_npc:
                self.ai_bridge.end_npc_conversation(self.current_npc)
            
            # 새 NPC와의 대화 시작
            session_id = self.ai_bridge.start_npc_conversation(npc_type, player_data)
            if session_id:
                self.current_npc = npc_type
                return f"{npc_type}와의 대화를 시작합니다."
            else:
                return "NPC 전환에 실패했습니다."
                
        except Exception as e:
            logger.error(f"NPC 전환 실패: {e}")
            return "NPC 전환 중 오류가 발생했습니다."
    
    def cleanup(self):
        """정리 작업"""
        if self.current_npc:
            self.ai_bridge.end_npc_conversation(self.current_npc)
            self.current_npc = None


if __name__ == "__main__":
    # 테스트 코드
    controller = GameAIController()
    
    test_player_data = {
        "name": "테스트플레이어",
        "lv": 1,
        "class": "미정",
        "hp": 100,
        "mp": 50,
        "STR": 10,
        "AGI": 10,
        "INT": 10,
        "LUCK": 10
    }
    
    # 신과의 대화 초기화
    initial_response = controller.initialize_god_conversation(test_player_data)
    print(f"초기 응답: {initial_response}")
    
    # 테스트 메시지 전송
    response = controller.send_player_message("안녕하세요, 저는 누구인가요?")
    print(f"AI 응답: {response}")
    
    # 정리
    controller.cleanup()
