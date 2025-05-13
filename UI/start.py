import pygame
import pygame_gui

def remove_main_menu_buttons(back_button, label, text_entry):
    """메인 메뉴 버튼을 제거합니다."""
    back_button.kill()
    label.kill()
    text_entry.kill()

def start_screen(manager, screen):
    """Start 화면을 관리하는 함수."""
    running = True
    clock = pygame.time.Clock()


    # 뒤로가기 버튼
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 10), (100, 50)),
        text='Back',
        manager=manager
    )
    
    # Add a label
    label_rect = pygame.Rect((200, 250), (200, 50))
    label = pygame_gui.elements.UILabel(
        relative_rect=label_rect,
        text="Name:",
        manager=manager
    )
    
    # Add a text input field
    input_rect = pygame.Rect((360, 250), (200, 50))
    text_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=input_rect,
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
                        remove_main_menu_buttons(back_button, label, text_entry)
                        return "menu"  # 메뉴로 돌아가기
            # When Enter is pressed in the input field
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == text_entry:
                    print(f"입력된 이름: {event.text}")
                    
            
        
        # 화면 렌더링
        screen.fill((255, 255, 255))  # 파란 배경
        font = pygame.font.Font(None, 50)
        
        

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
