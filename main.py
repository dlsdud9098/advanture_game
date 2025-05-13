import pygame
import pygame_gui
from UI.start import start_screen
from UI.options import options_screen
from pygame_gui.core.resource_loaders import BlockingThreadedResourceLoader

def remove_main_menu_buttons():
    """메인 메뉴 버튼을 제거합니다."""
    start_button.kill()
    options_button.kill()
    quit_button.kill()

def create_main_menu_buttons():
    """메인 메뉴 버튼을 다시 생성합니다."""
    global start_button, options_button, quit_button
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 200), (100, 50)),
        text='New Game',
        manager=manager
    )
    options_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 300), (100, 50)),
        text='Load Game',
        manager=manager
    )
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 400), (100, 50)),
        text='Quit',
        manager=manager
    )
    
if __name__ == '__main__':

    pygame.init()

    # 화면 설정
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Modular Screen Transition")
    font = pygame.font.SysFont("malgungothic", 80) # 시스템 폰트 사용 시

    # 매니저 설정
    # manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT), "theme.json")


    # 메인 메뉴 버튼
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 200), (100, 50)),
        # text = font.render('새로 만들기', True, (255,255,255)),
        text='New Game',
        manager=manager
    )

    options_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 300), (100, 50)),
        text='Load Game',
        manager=manager
    )

    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 400), (100, 50)),
        text='Quit',
        manager=manager
    )


    current_screen = "menu"
    running = True
    clock = pygame.time.Clock()

    while running:
        time_delta = clock.tick(60) / 1000.0

        if current_screen == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                manager.process_events(event)

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == start_button:
                            current_screen = "start"
                            remove_main_menu_buttons()  # 버튼 제거
                        elif event.ui_element == options_button:
                            current_screen = "options"
                            remove_main_menu_buttons()  # 버튼 제거
                        elif event.ui_element == quit_button:
                            running = False
            
            # 메인 메뉴 렌더링
            screen.fill((255, 255, 255))
            manager.update(time_delta)
            manager.draw_ui(screen)
            pygame.display.flip()

        elif current_screen == "start":
            current_screen = start_screen(manager, screen)
            if current_screen == "menu":
                create_main_menu_buttons()  # 버튼 다시 생성
        
        elif current_screen == "options":
            current_screen = options_screen(manager, screen)
            if current_screen == "menu":
                create_main_menu_buttons()  # 버튼 다시 생성

    pygame.quit()
