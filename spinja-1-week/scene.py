from menu import Menu
from credits import Credits
from game import Game
from game_over import GameOver

# Scene Manager
class SceneManager:
    def __init__(self):
        self.scenes = {
            'menu': Menu,
            'credits': Credits,
            'game': Game,
            'game_over': GameOver,
        }
        
        self.current_scene = Menu()
        self.transition = False
    
    def change_scene(self, game_state):
        self.current_scene = self.scenes[game_state]()
        self.transition = True