import pygame
import pygame_gui

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Screen Transition Example")

# 매니저 설정
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# 메뉴 화면 버튼 정의
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 200), (100, 50)),
    text='Start',
    manager=manager
)

options_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 300), (100, 50)),
    text='Options',
    manager=manager
)

quit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 400), (100, 50)),
    text='Quit',
    manager=manager
)

# 뒤로가기 버튼 (초기에는 생성되지 않음)
back_button = None

# 화면 상태 변수
current_screen = "menu"  # 초기 화면 상태: "menu"

# 메인 루프
clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(60) / 1000.0  # 프레임 시간 계산
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 메뉴 화면 이벤트 처리
        if current_screen == "menu":
            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        print("Start button clicked!")
                        current_screen = "game"  # 화면 상태 변경
                        
                        # 메뉴 버튼 제거
                        start_button.kill()
                        options_button.kill()
                        quit_button.kill()

                        # 뒤로가기 버튼 생성
                        back_button = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect((10, 10), (100, 50)),
                            text='Back',
                            manager=manager
                        )
                    elif event.ui_element == options_button:
                        print("Options button clicked!")
                    elif event.ui_element == quit_button:
                        print("Quit button clicked!")
                        running = False

        # 게임 화면 이벤트 처리
        elif current_screen == "game":
            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        print("Back button clicked!")
                        current_screen = "menu"  # 메뉴 화면으로 전환
                        
                        # 뒤로가기 버튼 제거
                        back_button.kill()
                        back_button = None

                        # 메뉴 버튼 다시 생성
                        start_button = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect((350, 200), (100, 50)),
                            text='Start',
                            manager=manager
                        )
                        options_button = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect((350, 300), (100, 50)),
                            text='Options',
                            manager=manager
                        )
                        quit_button = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect((350, 400), (100, 50)),
                            text='Quit',
                            manager=manager
                        )

    # 화면 렌더링
    screen.fill((255, 255, 255))  # 배경 색상

    if current_screen == "menu":
        manager.update(time_delta)
        manager.draw_ui(screen)
    elif current_screen == "game":
        # 게임 화면 렌더링
        screen.fill((0, 100, 200))  # 새로운 화면 색상 (파란색)
        font = pygame.font.Font(None, 50)
        text_surface = font.render("Game Screen", True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2))

        # 뒤로가기 버튼 렌더링
        manager.update(time_delta)
        manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
