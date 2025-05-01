import importlib
from unit.player import Player
from saves.save_loads import SAVE_LOADS

def select_charater_display():
    print('='*50)
    name = input('캐릭터 이름을 입력해주세요')
    CLASS = input(
'''
직업을 선택해 주세요.
1. 전사
2. 마법사
''')
    print('='*50)
    
    if CLASS == '1' or CLASS == '전사':
        CLASS = '전사'
    elif CLASS == '2' or CLASS == '마법사':
        CLASS = '마법사'
    
    return name, CLASS
def Display():
    svld = SAVE_LOADS()
    SAMENAME = 1
    while (SAMENAME):
        print('='*15)
        print('1. New Game')
        print('2. Load Game')
        print('3. Exit')
        print('='*15)
        
        sel = input()
        if sel == '1':
            name, CLASS = select_charater_display()
            player = Player(name=name, CLASS = CLASS)
            
            data = player.status()
            SAMENAME = svld.update_player_data(data)
        elif sel == '2':
            svld.save_loads()
        elif sel == '3':
            print('종료')
            return 
        else:
            print('잘못 입력하셨습니다.')

    return sel
    