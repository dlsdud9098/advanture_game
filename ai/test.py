"""
김샐프 NPC 질문-답변 완전한 루프 시스템
콘솔 버전과 게임 UI 통합 버전 모두 제공
"""

from npc_inference import NPCManager, GodNPCQuestionnaire
import time
import json

class ConsoleQuestionnaire:
    """
    콘솔에서 실행되는 완전한 질문-답변 시스템
    """
    
    def __init__(self):
        """
        초기화
        """
        print("=" * 60)
        print("🎮 김샐프 NPC 질문지 시스템")
        print("=" * 60)
        
        # NPC 시스템 초기화
        print("📁 NPC 모델 로딩 중...")
        self.npc_manager = NPCManager()
        self.npc_manager.auto_load_npcs()
        
        if "god" not in self.npc_manager.loaded_npcs:
            print("❌ 김샐프 NPC를 찾을 수 없습니다.")
            print("먼저 npc_training.py로 모델을 학습시켜주세요.")
            exit(1)
        
        print("✅ 김샐프 NPC 로드 완료!")
        self.questionnaire = GodNPCQuestionnaire(self.npc_manager)
        
    def run_full_questionnaire(self, num_questions: int = 15):
        """
        전체 질문지 실행
        
        Args:
            num_questions (int): 질문 개수
        """
        print("\n" + "=" * 60)
        print("🌟 캐릭터 생성을 위한 질문지를 시작합니다!")
        print("=" * 60)
        
        # 질문지 시작
        greeting = self.questionnaire.start_questionnaire(num_questions)
        self.display_message("김샐프", greeting)
        
        # 질문-답변 루프
        while True:
            # 현재 진행 상황 확인
            progress = self.questionnaire.get_progress()
            
            if progress['completed']:
                # 질문지 완료
                self.complete_questionnaire()
                break
            
            # 현재 질문 표시
            current_question = self.questionnaire.get_current_question()
            
            print("\n" + "-" * 40)
            print(f"📋 질문 {progress['current_question']}/{progress['total_questions']}")
            print("-" * 40)
            
            self.display_question(current_question)
            
            # 현재 스탯 상황 표시 (간략하게)
            if progress['current_question'] > 1:
                self.show_current_stats(progress['current_stats'])
            
            # 사용자 답변 받기
            user_answer = self.get_user_input()
            
            if user_answer.lower() in ['quit', '종료', 'exit']:
                print("질문지를 종료합니다.")
                break
            
            # 답변 처리 및 NPC 응답
            npc_response = self.questionnaire.answer_question(user_answer)
            self.display_message("김샐프", npc_response)
            
            # 잠시 대기 (읽을 시간 제공)
            time.sleep(1)
    
    def display_message(self, speaker: str, message: str):
        """
        메시지 예쁘게 표시
        """
        print(f"\n💬 {speaker}:")
        print(f"   {message}")
    
    def display_question(self, question: str):
        """
        질문 예쁘게 표시
        """
        print(f"\n❓ {question}")
    
    def show_current_stats(self, stats: dict):
        """
        현재 스탯 상황 표시
        """
        total = sum(stats.values())
        if total > 0:
            print(f"\n📊 현재 성향: ", end="")
            stat_display = []
            for stat, value in stats.items():
                if value > 0:
                    percentage = (value / total) * 100
                    stat_display.append(f"{stat}({percentage:.0f}%)")
            print(" | ".join(stat_display))
    
    def get_user_input(self) -> str:
        """
        사용자 입력 받기
        """
        print("\n✏️  답변을 입력하세요 (종료하려면 'quit' 입력):")
        print("   > ", end="")
        return input().strip()
    
    def complete_questionnaire(self):
        """
        질문지 완료 처리
        """
        print("\n" + "=" * 60)
        print("🎉 모든 질문이 완료되었습니다!")
        print("=" * 60)
        
        # 최종 결과 받기
        final_result = self.questionnaire.finalize_questionnaire()
        
        # 최종 메시지
        if final_result.get('final_message'):
            self.display_message("김샐프", final_result['final_message'])
        
        # 결과 분석 표시
        self.display_final_results(final_result)
        
        # 결과 저장 여부 묻기
        self.save_results_prompt(final_result)
    
    def display_final_results(self, result: dict):
        """
        최종 결과 예쁘게 표시
        """
        print("\n" + "🎯 분석 결과")
        print("=" * 30)
        
        # 스탯 분석
        stats = result.get('final_stats', {})
        total_stats = sum(stats.values())
        
        print("📈 성향 분석:")
        for stat, value in stats.items():
            stat_names = {
                'STR': '힘/용기',
                'AGI': '민첩/적응',
                'INT': '지혜/논리', 
                'LUCK': '직감/운명'
            }
            percentage = (value / total_stats * 100) if total_stats > 0 else 0
            bar_length = int(percentage / 5)  # 20칸 막대그래프
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"   {stat_names.get(stat, stat):8} │{bar}│ {percentage:5.1f}% ({value}점)")
        
        # 부여된 직업
        assigned_class = result.get('assigned_class', '전사')
        class_desc = result.get('class_description', '')
        
        print(f"\n🏆 부여된 직업: {assigned_class}")
        if class_desc:
            print(f"   {class_desc}")
        
        # 권장 스탯 보너스
        bonus_stats = self.calculate_stat_bonus(stats)
        print(f"\n⭐ 추천 스탯 보너스:")
        for stat, bonus in bonus_stats.items():
            if bonus > 0:
                print(f"   {stat}: +{bonus}")
    
    def calculate_stat_bonus(self, ai_stats: dict) -> dict:
        """
        AI 분석 점수를 게임 스탯 보너스로 변환
        """
        return {
            "STR": max(1, ai_stats.get("STR", 0) // 3),
            "AGI": max(1, ai_stats.get("AGI", 0) // 3),
            "INT": max(1, ai_stats.get("INT", 0) // 3),
            "LUCK": max(1, ai_stats.get("LUCK", 0) // 3)
        }
    
    def save_results_prompt(self, result: dict):
        """
        결과 저장 여부 묻기
        """
        print("\n💾 결과를 파일로 저장하시겠습니까? (y/n): ", end="")
        save_choice = input().strip().lower()
        
        if save_choice in ['y', 'yes', '예', 'ㅇ']:
            self.save_results_to_file(result)
            print("✅ 결과가 저장되었습니다!")
        
        print("\n🎮 게임을 시작하세요!")


class GameUIQuestionnaire:
    """
    게임 UI에 통합할 수 있는 질문-답변 시스템
    """
    
    def __init__(self, ui_callback_functions: dict):
        """
        초기화
        
        Args:
            ui_callback_functions (dict): UI 콜백 함수들
                - display_message: 메시지 표시 함수
                - update_progress: 진행률 업데이트 함수
                - show_results: 결과 표시 함수
                - apply_to_player: 플레이어에 적용 함수
        """
        self.ui_callbacks = ui_callback_functions
        self.npc_manager = NPCManager()
        self.npc_manager.auto_load_npcs()
        
        if "god" not in self.npc_manager.loaded_npcs:
            self.ui_callbacks['display_message']("시스템", "김샐프 NPC를 찾을 수 없습니다.")
            return
        
        self.questionnaire = GodNPCQuestionnaire(self.npc_manager)
        self.active = False
        self.waiting_for_answer = False
        
    def start_questionnaire(self, num_questions: int = 15) -> bool:
        """
        질문지 시작
        
        Args:
            num_questions (int): 질문 개수
            
        Returns:
            bool: 시작 성공 여부
        """
        if "god" not in self.npc_manager.loaded_npcs:
            return False
        
        # 질문지 시작
        greeting = self.questionnaire.start_questionnaire(num_questions)
        self.ui_callbacks['display_message']("김샐프", greeting)
        
        # 첫 번째 질문
        first_question = self.questionnaire.get_current_question()
        self.ui_callbacks['display_message']("김샐프", first_question)
        
        self.active = True
        self.waiting_for_answer = True
        
        # 진행률 업데이트
        progress = self.questionnaire.get_progress()
        self.ui_callbacks['update_progress'](progress)
        
        return True
    
    def handle_user_input(self, user_input: str) -> dict:
        """
        사용자 입력 처리
        
        Args:
            user_input (str): 사용자 입력
            
        Returns:
            dict: 처리 결과
        """
        if not self.active or not self.waiting_for_answer:
            return {"handled": False}
        
        # 답변 처리
        npc_response = self.questionnaire.answer_question(user_input)
        self.ui_callbacks['display_message']("김샐프", npc_response)
        
        # 진행 상황 확인
        progress = self.questionnaire.get_progress()
        self.ui_callbacks['update_progress'](progress)
        
        if progress['completed']:
            # 질문지 완료
            final_result = self.questionnaire.finalize_questionnaire()
            self.complete_questionnaire(final_result)
            
            return {
                "handled": True,
                "completed": True,
                "result": final_result
            }
        else:
            # 다음 질문
            next_question = self.questionnaire.get_current_question()
            self.ui_callbacks['display_message']("김샐프", next_question)
            
            return {
                "handled": True,
                "completed": False,
                "progress": progress
            }
    
    def complete_questionnaire(self, final_result: dict):
        """
        질문지 완료 처리
        """
        self.active = False
        self.waiting_for_answer = False
        
        # 최종 메시지
        if final_result.get('final_message'):
            self.ui_callbacks['display_message']("김샐프", final_result['final_message'])
        
        # 결과 표시
        self.ui_callbacks['show_results'](final_result)
        
        # 플레이어에 적용
        self.ui_callbacks['apply_to_player'](final_result)


def save_results_to_file(result: dict, filename: str = None):
    """
    결과를 JSON 파일로 저장
    """
    if filename is None:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"questionnaire_result_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        return filename
    except Exception as e:
        print(f"파일 저장 실패: {e}")
        return None


def run_console_questionnaire():
    """
    콘솔 버전 질문지 실행
    """
    try:
        questionnaire = ConsoleQuestionnaire()
        questionnaire.run_full_questionnaire(num_questions=15)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {e}")


def create_ui_integration_example():
    """
    게임 UI 통합 예시 코드
    """
    
    # UI 콜백 함수들 정의
    def display_message_callback(speaker: str, message: str):
        """메시지 표시 콜백 (실제로는 UI의 add_typing_label 등을 호출)"""
        print(f"{speaker}: {message}")
    
    def update_progress_callback(progress: dict):
        """진행률 업데이트 콜백"""
        current = progress['current_question']
        total = progress['total_questions']
        stats = progress['current_stats']
        print(f"진행: {current}/{total}, 현재 스탯: {stats}")
    
    def show_results_callback(result: dict):
        """결과 표시 콜백"""
        stats = result.get('final_stats', {})
        assigned_class = result.get('assigned_class', '전사')
        print(f"최종 결과 - 스탯: {stats}, 직업: {assigned_class}")
    
    def apply_to_player_callback(result: dict):
        """플레이어에 적용 콜백"""
        # 실제로는 player_data 수정
        print("플레이어 데이터에 AI 결과를 적용했습니다.")
    
    # UI 콜백 함수들
    ui_callbacks = {
        'display_message': display_message_callback,
        'update_progress': update_progress_callback, 
        'show_results': show_results_callback,
        'apply_to_player': apply_to_player_callback
    }
    
    # 게임 UI 질문지 시스템 생성
    ui_questionnaire = GameUIQuestionnaire(ui_callbacks)
    
    # 질문지 시작
    if ui_questionnaire.start_questionnaire(num_questions=5):  # 테스트용 5문제
        print("✅ 게임 UI 질문지 시작됨")
        
        # 테스트 답변들
        test_answers = [
            "정의를 위해 싸우는 것이 중요합니다.",
            "빠르게 상황을 파악하고 움직입니다.",
            "신중하게 계획을 세웁니다.",
            "직감을 믿고 행동합니다.",
            "모든 것을 균형있게 생각합니다."
        ]
        
        for answer in test_answers:
            result = ui_questionnaire.handle_user_input(answer)
            if result.get('completed'):
                print("🎉 질문지 완료!")
                break
    else:
        print("❌ 질문지 시작 실패")


if __name__ == "__main__":
    print("🎮 김샐프 NPC 질문지 시스템")
    print("1. 콘솔 버전 실행")
    print("2. UI 통합 예시 실행")
    print("3. 종료")
    
    choice = input("\n선택하세요 (1-3): ").strip()
    
    if choice == "1":
        run_console_questionnaire()
    elif choice == "2":
        create_ui_integration_example()
    elif choice == "3":
        print("👋 안녕히 가세요!")
    else:
        print("❌ 잘못된 선택입니다.")