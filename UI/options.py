import pygame
import pygame_gui

def options_screen(manager, screen):
    """Options 화면을 관리하는 함수."""
    running = True
    clock = pygame.time.Clock()

    # 뒤로가기 버튼
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 10), (100, 50)),
        text='Back',
        manager=manager
    )

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            
            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        running = False
                        return "menu"  # 메뉴로 돌아가기

        # 화면 렌더링
        screen.fill((50, 50, 50))  # 회색 배경
        font = pygame.font.Font(None, 50)
        text_surface = font.render("Options Screen", True, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, screen.get_height() // 2))

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
