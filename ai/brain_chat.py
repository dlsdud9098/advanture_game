from ai.god_brain import GOD


# # def Chat(player_data, class_question, input_text):
# def Chat(system_instruction, input_text):
#     god = GOD()

#     # 세션 생성
#     god_session = god.create_session()

    
#     # 세션별 대화
#     # system_instruction = f"""
#     # 당신은 현제 이 세계의 신입니다.

#     # 이 세계의 구원을 위해 당신은 다른 차원에 있는 인간을 소환했습니다.
#     # 당신은 매우 강력하지만 당신의 세계에 직접적으로 간섭할 수 없습니다.

#     # 하지만 당신이 소환한 존재(플레이어)는 당신의 힘이 조금 깃들어있기 때문에 약간의 간섭은 할 수 있습니다.
#     # 새로운 힘(스킬, 스텟 등)을 부여할 수 있습니다.
#     # 그것은 당신이 플레이어를 어떻게 생각하고, 어떤 감정을 가지고 있는지에 따라 달라집니다.

#     # 당신의 세계의 구원을 위해 소환한 존재이기 때문에 최대한 잘 해주려고 노력합니다.
#     # 하지만 소환된 존재가 안하무인한 존재라면, 두고 볼 정도로 답답한 사람이 아닙니다.

#     # 현재 상황은 당신이 막 플레이어를 당신의 세계로 소환된상황입니다.

#     # 현재 플레이어의 상태는 {player_data} 입니다.

#     # 당신이 해야할 일은 {class_question}입니다.
#     # """

#     # 첫 번째 세션에서 대화
#     response = god.chat(god_session, system_instruction, input_text)
#     return response
#     print(f"[Session {god_session}] Bot:", response1)

#     # 두 번째 세션에서 대화
#     # input_text2 = "프랑스의 수도는 무엇인가요?"
#     # response2 = manager.chat(session_id2, instruction, input_text2)
#     # print(f"[Session {session_id2}] Bot:", response2)

#     # 첫 번째 세션 기록 확인
#     print(f"[Session {god_session}] History:", god.get_session(session_id1))


def Chat(self, session_id, instruction, input_text):
    print(f"chat() received session_id: {repr(session_id)}")
    print(f"Current session keys: {[repr(k) for k in self.sessions.keys()]}")
    
    if session_id not in self.sessions:
        print("Session not found. Please create a session first.")
        return None

    # 이전 대화 기록 누적
    history = self.sessions[session_id]
    history_text = ""
    for turn in history:
        history_text += f"User: {turn['user']}\nBot: {turn['bot']}\n"

    # 최종 프롬프트 구성
    prompt = f"{instruction}\n\n{history_text}User: {input_text}\nBot:"

    inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    inputs = {k: v.to('cuda') for k, v in inputs.items()}

    outputs = self.model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.7)
    bot_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    self.add_message_to_session(session_id, input_text, bot_response)

    return bot_response
