from unit.player import Player
from saves.save_loads import SAVE_LOADS
# from game.main_game import MAIN_GAME
import os

def select_charater_display():
    os.system('clear')
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

def NewGameDisplay(svld):
    name, CLASS = select_charater_display()
    player = Player(name=name, CLASS = CLASS)
    
    data = player.get_status()
    SAMENAME = svld.data_update(data)
    
    player.DisplayStatus()
    
    
    return SAMENAME, player

def LoadGameDisplay(player_data):
    os.system('clear')
    for idx, data in enumerate(player_data):
        print(f"{idx+1}. LV: {data['LV']}, name: {data['name']}")
        
    player_idx = input('불러올 데이터 선택')
    if not player_idx.isdigit():
        print('잘못 입력하셨습니다.')
    player_idx = int(player_idx) - 1
    
    if player_idx > len(player_data) or (player_idx < 0):
        print('리스트에 없습니다.')
        
    # print(player_data[player_idx])
    player = Player(name='', CLASS='')
    player.set_status(player_data[player_idx])
    
    # player.DisplayStatus()
    return 0, player
    

def MainDisplay():
    os.system('clear')
    
    svld = SAVE_LOADS()
    SAMENAME = 1
    
    while (SAMENAME):
        print('='*15)
        print('1. New Game')
        print('2. Load Game')
        print('3. Exit')
        print('='*15)
        
        sel = input()
        print(sel)
        if sel == '1':
            SAMENAME, player = NewGameDisplay(svld)
        elif sel == '2':
            player_data = svld.data_load()
            if not bool(player_data):
                os.system('clear')
                print('데이터가 비어있습니다.')
                SAMENAME = 1
            else:
                AGAIN = 1
                while (AGAIN):
                    AGAIN, player = LoadGameDisplay(player_data)
                break
        elif sel == '3':
            print('종료')
            os.system('clear')
            return 
        else:
            print('잘못 입력하셨습니다.')
            os.system('clear')
            
    return player
        # main = MAIN_GAME()
        # main.MENU(player)