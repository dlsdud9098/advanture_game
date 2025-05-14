import importlib

class CreateCharacter:
    def __init__(self, name, CLASS):
        self.name = name
        self.CLASS = CLASS
        
        self.select_class()
    
    def select_class(self):
        ch_class = 'player'
        # 동적으로 character_class 모듈 불러오기
        class_module = f"unit.{ch_class}"
        module = importlib.import_module(class_module)
        
        if hasattr(module, 'Player'):
            player_class = getattr(module, 'Player')  # Player 클래스를 가져옴
            player_instance = player_class(self.name, self.CLASS)  # Player 인스턴스를 생성
            
            return player_instance