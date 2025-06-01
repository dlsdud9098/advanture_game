"""
완전한 룰 기반 질문지 시스템
AI 모델 없이도 완벽하게 작동하는 김샐프 질문지
"""

import json
import random
from typing import Dict, List, Optional

class RuleBasedGodNPC:
    """
    룰 기반 김샐프 NPC 시스템 (AI 모델 불필요)
    """
    
    def __init__(self):
        """
        초기화
        """
        self.npc_data = self.load_npc_data()
        self.selected_questions = []
        self.current_question_index = 0
        self.user_answers = []
        self.total_stats = {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
    def load_npc_data(self) -> dict:
        """
        김샐프 NPC 데이터 로드 (JSON 파일 또는 하드코딩)
        """
        # JSON 파일이 있으면 로드, 없으면 하드코딩된 데이터 사용
        try:
            with open('god_npc_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # 하드코딩된 기본 데이터
            return self.get_default_npc_data()
    
    def get_default_npc_data(self) -> dict:
        """
        기본 NPC 데이터 (JSON 파일이 없을 때 사용)
        """
        return {
            "name": "김샐프",
            "questions": [
                {
                    "id": 1,
                    "question": "당신이 가장 중요하게 생각하는 가치는 무엇입니까?",
                    "stat_keywords": {
                        "STR": ["정의", "용기", "힘", "보호", "싸움", "강함"],
                        "AGI": ["자유", "속도", "민첩", "순발력", "빠름", "기동력"],
                        "INT": ["지혜", "지식", "학습", "연구", "분석", "사고"],
                        "LUCK": ["운명", "기회", "행운", "직감", "우연", "인연"]
                    }
                },
                {
                    "id": 2,
                    "question": "위험한 상황에 처했을 때, 당신의 첫 번째 반응은 무엇입니까?",
                    "stat_keywords": {
                        "STR": ["정면돌파", "맞서다", "싸우다", "돌진", "공격"],
                        "AGI": ["회피", "도망", "빠르게", "움직이다", "피하다"],
                        "INT": ["분석", "계획", "생각", "전략", "관찰"],
                        "LUCK": ["직감", "기다리다", "운에맡기다", "느낌"]
                    }
                },
                {
                    "id": 3,
                    "question": "당신이 꿈꾸는 이상향은 어떤 모습입니까?",
                    "stat_keywords": {
                        "STR": ["평화", "질서", "안전", "보호받는", "강한"],
                        "AGI": ["자유로운", "제약없는", "빠른", "활동적인"],
                        "INT": ["지적인", "발전된", "학문적인", "합리적인"],
                        "LUCK": ["행복한", "운이좋은", "기적적인", "신비로운"]
                    }
                },
                {
                    "id": 4,
                    "question": "동료와의 갈등이 생겼을 때, 어떻게 해결하시겠습니까?",
                    "stat_keywords": {
                        "STR": ["직접", "당당하게", "맞서다", "강하게"],
                        "AGI": ["유연하게", "빠르게", "피하다", "돌아서"],
                        "INT": ["대화", "설득", "분석", "이해", "논리적"],
                        "LUCK": ["시간", "운", "자연스럽게", "우연히"]
                    }
                },
                {
                    "id": 5,
                    "question": "당신이 가장 두려워하는 것은 무엇입니까?",
                    "stat_keywords": {
                        "STR": ["약함", "무력감", "보호못함", "패배"],
                        "AGI": ["속박", "제약", "느림", "갇힘"],
                        "INT": ["무지", "실수", "어리석음", "모름"],
                        "LUCK": ["불운", "재앙", "운명", "예측불가"]
                    }
                },
                {
                    "id": 6,
                    "question": "새로운 기술이나 능력을 배울 때, 어떤 방식을 선호합니까?",
                    "stat_keywords": {
                        "STR": ["반복", "훈련", "몸으로", "직접"],
                        "AGI": ["빠르게", "즉석", "실전", "체험"],
                        "INT": ["이론", "연구", "체계적", "단계적"],
                        "LUCK": ["감각", "직감", "자연스럽게", "운"]
                    }
                },
                {
                    "id": 7,
                    "question": "리더가 되어야 하는 상황에서, 당신의 리더십 스타일은?",
                    "stat_keywords": {
                        "STR": ["카리스마", "강력한", "결단력", "앞장"],
                        "AGI": ["유연한", "빠른결정", "적응", "기민한"],
                        "INT": ["계획적", "분석적", "논리적", "체계적"],
                        "LUCK": ["직감적", "운에맡김", "자연스러운", "영감"]
                    }
                },
                {
                    "id": 8,
                    "question": "당신에게 있어 진정한 성공이란 무엇입니까?",
                    "stat_keywords": {
                        "STR": ["목표달성", "승리", "강해짐", "보호"],
                        "AGI": ["자유", "빠른성장", "기회포착", "변화"],
                        "INT": ["지식습득", "이해", "발견", "진리"],
                        "LUCK": ["행복", "만족", "운명", "기적"]
                    }
                },
                {
                    "id": 9,
                    "question": "어려운 결정을 내려야 할 때, 무엇에 의존합니까?",
                    "stat_keywords": {
                        "STR": ["신념", "의지", "용기", "결심"],
                        "AGI": ["상황판단", "순발력", "즉흥", "기민함"],
                        "INT": ["논리", "분석", "데이터", "이성"],
                        "LUCK": ["직감", "느낌", "운", "영감"]
                    }
                },
                {
                    "id": 10,
                    "question": "당신이 가장 자신있어 하는 분야는 무엇입니까?",
                    "stat_keywords": {
                        "STR": ["체력", "힘", "격투", "운동", "경쟁"],
                        "AGI": ["민첩성", "속도", "반응", "움직임", "기술"],
                        "INT": ["학습", "분석", "기억", "추리", "연구"],
                        "LUCK": ["운", "감각", "직감", "타이밍", "기회"]
                    }
                },
                {
                    "id": 11,
                    "question": "타인을 돕는 이유는 무엇입니까?",
                    "stat_keywords": {
                        "STR": ["의무", "정의", "보호", "책임"],
                        "AGI": ["효율", "빠름", "기회", "상황"],
                        "INT": ["이해", "논리", "합리", "분석"],
                        "LUCK": ["감정", "직감", "운명", "인연"]
                    }
                },
                {
                    "id": 12,
                    "question": "실패했을 때, 어떻게 극복하십니까?",
                    "stat_keywords": {
                        "STR": ["다시시도", "더강하게", "노력", "의지"],
                        "AGI": ["빠른회복", "변화", "적응", "전환"],
                        "INT": ["분석", "학습", "계획수정", "연구"],
                        "LUCK": ["시간", "기회", "운", "자연스럽게"]
                    }
                },
                {
                    "id": 13,
                    "question": "당신의 인생에서 가장 중요한 순간은 언제였습니까?",
                    "stat_keywords": {
                        "STR": ["도전", "싸움", "극복", "승리"],
                        "AGI": ["변화", "기회", "빠른결정", "전환점"],
                        "INT": ["깨달음", "학습", "이해", "발견"],
                        "LUCK": ["우연", "운명", "만남", "기적"]
                    }
                },
                {
                    "id": 14,
                    "question": "이세계에서 이루고 싶은 목표는 무엇입니까?",
                    "stat_keywords": {
                        "STR": ["평화", "정의", "보호", "구원"],
                        "AGI": ["모험", "자유", "탐험", "경험"],
                        "INT": ["지식", "진리", "발견", "이해"],
                        "LUCK": ["행복", "만족", "운명", "조화"]
                    }
                },
                {
                    "id": 15,
                    "question": "당신이 생각하는 진정한 용기란 무엇입니까?",
                    "stat_keywords": {
                        "STR": ["강함", "맞서다", "굽히지않음", "정면"],
                        "AGI": ["유연함", "빠른대응", "적응", "기민함"],
                        "INT": ["지혜", "이해", "신중함", "판단"],
                        "LUCK": ["직감", "믿음", "운명", "자연스러움"]
                    }
                }
            ],
            "class_mapping": {
                "전사": {
                    "primary_stat": "STR",
                    "secondary_stat": "LUCK",
                    "min_ratio": 0.3,
                    "description": "강인한 체력과 용기를 바탕으로 전면에서 싸우는 직업"
                },
                "마법사": {
                    "primary_stat": "INT", 
                    "secondary_stat": "AGI",
                    "min_ratio": 0.3,
                    "description": "지혜와 지식을 바탕으로 마법을 다루는 직업"
                },
                "궁수": {
                    "primary_stat": "AGI",
                    "secondary_stat": "LUCK", 
                    "min_ratio": 0.3,
                    "description": "민첩함과 정확성으로 원거리에서 공격하는 직업"
                }
            }
        }
    
    def start_questionnaire(self, num_questions: int = 15) -> str:
        """
        질문지 시작
        """
        # 질문 랜덤 선택
        all_questions = self.npc_data['questions']
        self.selected_questions = random.sample(all_questions, min(num_questions, len(all_questions)))
        
        # 초기화
        self.current_question_index = 0
        self.user_answers = []
        self.total_stats = {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
        # 인사말
        return "용사여, 이세계에 오신 것을 환영합니다. 저는 이 세계를 관장하는 신 김샐프입니다. 당신에게 적절한 힘을 부여하기 위해 몇 가지 질문을 드리겠습니다."
    
    def get_current_question(self) -> str:
        """
        현재 질문 반환
        """
        if self.current_question_index < len(self.selected_questions):
            return self.selected_questions[self.current_question_index]['question']
        else:
            return "모든 질문이 완료되었습니다."
    
    def analyze_answer(self, user_answer: str) -> Dict[str, int]:
        """
        사용자 답변 분석하여 스탯 점수 계산
        """
        if self.current_question_index >= len(self.selected_questions):
            return {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
        current_question = self.selected_questions[self.current_question_index]
        stat_points = {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
        # 키워드 매칭으로 스탯 점수 계산
        for stat, keywords in current_question['stat_keywords'].items():
            for keyword in keywords:
                if keyword in user_answer:
                    stat_points[stat] += 2
        
        # 키워드가 하나도 매칭되지 않으면 답변 길이와 내용으로 추정
        if sum(stat_points.values()) == 0:
            stat_points = self.analyze_by_sentiment(user_answer)
        
        return stat_points
    
    def analyze_by_sentiment(self, user_answer: str) -> Dict[str, int]:
        """
        키워드 매칭이 안 될 때 답변 감정/성향 분석
        """
        answer_lower = user_answer.lower()
        
        # 간단한 감정 분석 룰
        str_indicators = ["싸우", "강하", "정의", "보호", "책임", "의무"]
        agi_indicators = ["빠르", "자유", "유연", "변화", "적응"]
        int_indicators = ["생각", "분석", "계획", "연구", "논리", "이해"]
        luck_indicators = ["행복", "운", "느낌", "직감", "자연", "우연"]
        
        stat_points = {"STR": 0, "AGI": 0, "INT": 0, "LUCK": 0}
        
        for indicator in str_indicators:
            if indicator in answer_lower:
                stat_points["STR"] += 1
        
        for indicator in agi_indicators:
            if indicator in answer_lower:
                stat_points["AGI"] += 1
        
        for indicator in int_indicators:
            if indicator in answer_lower:
                stat_points["INT"] += 1
        
        for indicator in luck_indicators:
            if indicator in answer_lower:
                stat_points["LUCK"] += 1
        
        # 아무 매칭도 없으면 답변 길이로 추정
        if sum(stat_points.values()) == 0:
            if len(user_answer) > 20:
                stat_points["INT"] = 2  # 긴 답변은 신중함
            elif len(user_answer) <= 5:
                stat_points["LUCK"] = 2  # 짧은 답변은 직감적
            else:
                stat_points["STR"] = 1  # 중간 길이는 균형
        
        return stat_points
    
    def generate_response(self, user_answer: str) -> str:
        """
        사용자 답변에 대한 김샐프의 응답 생성
        """
        # 답변 분석
        stat_points = self.analyze_answer(user_answer)
        
        # 가장 높은 스탯 찾기
        max_stat = max(stat_points, key=stat_points.get) if sum(stat_points.values()) > 0 else "STR"
        
        # 스탯별 응답 템플릿
        responses = {
            "STR": [
                "강인한 의지가 느껴집니다.",
                "용기 있는 마음을 가지고 계시는군요.",
                "정의로운 힘이 당신 안에 있습니다.",
                "굳건한 신념이 보입니다.",
                "용사다운 답변입니다."
            ],
            "AGI": [
                "민첩하고 기민한 성향이 보입니다.",
                "빠른 판단력을 가지고 계시는군요.",
                "유연한 사고방식이 돋보입니다.",
                "적응력이 뛰어나시는군요.",
                "기민한 지혜가 느껴집니다."
            ],
            "INT": [
                "지혜로운 판단력을 보여주시는군요.",
                "깊이 있는 사고를 하시는 분이군요.",
                "현명한 접근 방식입니다.",
                "통찰력이 뛰어나시군요.",
                "학자의 기질이 보입니다."
            ],
            "LUCK": [
                "직감적이고 영감이 풍부하시군요.",
                "운명의 흐름을 잘 읽으시는군요.",
                "자연스러운 감각을 가지고 계시는군요.",
                "신비로운 힘이 느껴집니다.",
                "천성적인 감각이 있으시군요."
            ]
        }
        
        # 기본 응답 + 스탯 응답 조합
        base_responses = [
            "그렇군요.",
            "훌륭한 답변입니다.",
            "좋습니다.",
            "흥미로운 관점이군요.",
            "깊이 있는 생각이 담긴 답변입니다."
        ]
        
        base = random.choice(base_responses)
        stat_comment = random.choice(responses[max_stat])
        
        return f"{base} {stat_comment}"
    
    def answer_question(self, user_answer: str) -> str:
        """
        질문에 답변하고 다음 질문으로 진행
        """
        if self.current_question_index >= len(self.selected_questions):
            return "모든 질문이 완료되었습니다."
        
        # 답변 분석 및 스탯 누적
        stat_points = self.analyze_answer(user_answer)
        for stat, points in stat_points.items():
            self.total_stats[stat] += points
        
        # 답변 저장
        current_question = self.selected_questions[self.current_question_index]
        self.user_answers.append({
            'question_id': current_question['id'],
            'question': current_question['question'],
            'answer': user_answer,
            'stat_points': stat_points
        })
        
        # 응답 생성
        response = self.generate_response(user_answer)
        
        # 다음 질문으로 진행
        self.current_question_index += 1
        
        return response
    
    def get_progress(self) -> Dict:
        """
        진행 상황 반환
        """
        return {
            'current_question': self.current_question_index + 1,
            'total_questions': len(self.selected_questions),
            'current_stats': self.total_stats.copy(),
            'completed': self.current_question_index >= len(self.selected_questions)
        }
    
    def determine_class(self) -> str:
        """
        최종 직업 결정
        """
        if sum(self.total_stats.values()) == 0:
            return "전사"  # 기본값
        
        # 가장 높은 스탯 찾기
        max_stat = max(self.total_stats, key=self.total_stats.get)
        
        # 직업 매핑
        class_mapping = self.npc_data.get('class_mapping', {})
        
        for class_name, class_info in class_mapping.items():
            if class_info['primary_stat'] == max_stat:
                return class_name
        
        return "전사"  # 기본값
    
    def finalize_questionnaire(self) -> Dict:
        """
        질문지 완료 및 최종 결과 반환
        """
        final_class = self.determine_class()
        
        result = {
            'completed': True,
            'final_stats': self.total_stats.copy(),
            'assigned_class': final_class,
            'class_description': self.npc_data.get('class_mapping', {}).get(final_class, {}).get('description', ''),
            'answers': self.user_answers.copy(),
            'final_message': '훌륭합니다. 당신의 마음을 충분히 이해했습니다. 이제 당신에게 적합한 힘을 부여하겠습니다.'
        }
        
        return result


class RuleBasedQuestionnaire:
    """
    완전한 룰 기반 질문지 시스템 (AI 모델 불필요)
    """
    
    def __init__(self):
        """
        초기화
        """
        print("=" * 60)
        print("🎮 김샐프 NPC 룰 기반 질문지 시스템")
        print("=" * 60)
        
        # 룰 기반 NPC 초기화
        self.god_npc = RuleBasedGodNPC()
        print("✅ 김샐프 NPC 준비 완료! (AI 모델 불필요)")
        
    def run_full_questionnaire(self, num_questions: int = 15):
        """
        전체 질문지 실행
        """
        print("\n" + "=" * 60)
        print("🌟 캐릭터 생성을 위한 질문지를 시작합니다!")
        print("=" * 60)
        
        # 질문지 시작
        greeting = self.god_npc.start_questionnaire(num_questions)
        self.display_message("김샐프", greeting)
        
        # 질문-답변 루프
        while True:
            # 현재 진행 상황 확인
            progress = self.god_npc.get_progress()
            
            if progress['completed']:
                # 질문지 완료
                self.complete_questionnaire()
                break
            
            # 현재 질문 표시
            current_question = self.god_npc.get_current_question()
            
            print("\n" + "-" * 40)
            print(f"📋 질문 {progress['current_question']}/{progress['total_questions']}")
            print("-" * 40)
            
            self.display_question(current_question)
            
            # 현재 스탯 상황 표시
            if progress['current_question'] > 1:
                self.show_current_stats(progress['current_stats'])
            
            # 사용자 답변 받기
            user_answer = self.get_user_input()
            
            if user_answer.lower() in ['quit', '종료', 'exit']:
                print("질문지를 종료합니다.")
                break
            
            # 답변 처리 및 NPC 응답
            npc_response = self.god_npc.answer_question(user_answer)
            self.display_message("김샐프", npc_response)
    
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
        final_result = self.god_npc.finalize_questionnaire()
        
        # 최종 메시지
        self.display_message("김샐프", final_result['final_message'])
        
        # 결과 분석 표시
        self.display_final_results(final_result)
    
    def display_final_results(self, result: dict):
        """
        최종 결과 예쁘게 표시
        """
        print("\n" + "🎯 분석 결과")
        print("=" * 30)
        
        # 스탯 분석
        stats = result['final_stats']
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
        assigned_class = result['assigned_class']
        class_desc = result['class_description']
        
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
        분석 점수를 게임 스탯 보너스로 변환
        """
        return {
            "STR": max(2, ai_stats.get("STR", 0) // 3),
            "AGI": max(2, ai_stats.get("AGI", 0) // 3),
            "INT": max(2, ai_stats.get("INT", 0) // 3),
            "LUCK": max(2, ai_stats.get("LUCK", 0) // 3)
        }


def main():
    """
    룰 기반 질문지 실행
    """
    try:
        questionnaire = RuleBasedQuestionnaire()
        questionnaire.run_full_questionnaire(num_questions=15)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()