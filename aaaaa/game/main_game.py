from display.display_select import MainDisplay
import random

class MAIN_GAME:
    def __init__(self):
        pass
    
    def GAMESTART(self):
        player = MainDisplay()
        
        self.MENU(player)
    
    def MENU(self, player):
        sel = input(f"{'='*50}\n1. 상태창\n2. 진행하기\n3. 저장하기\n{'='*50}")
        
        AGAIN = 1
        while AGAIN:
            if sel == '1':
                player.DisplayStatus()
                AGAIN = 0
            elif sel == '2':
                AGAIN = 0
                pass
            elif sel == '3':
                AGAIN = 0
                pass
            else:
                print('잘못 입력하셨습니다.')
            
    # 전투    
    def BATTLE(self, player, monster):
        pass

    # 거래
    def TRADE(self, plyaer, NPC):
        pass
    
    """
    나중에 AI를 넣었을 때 우리가 직업을 선택하는 것이 아닌
    주어진 질문에 답하여 클래스를 지정
    """
    def SelectClass(self):
        pass