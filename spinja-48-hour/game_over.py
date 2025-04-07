from settings import *
import ui


class GameOver:
    def __init__(self):
        self.menu_button = ui.Button(screen, (SCREEN_MIDDLE.x - 50, SCREEN_MIDDLE.y), 'Menu')
        self.play_button = ui.Button(screen, (SCREEN_MIDDLE.x + 50, SCREEN_MIDDLE.y), 'Play Again', 6)
        
        self.background = pygame.image.load('assets/sprites/game_over_background.png').convert()
    
    
    # Called every frame
    def update(self, events, dt, scene_manager):
        screen.fill((10, 10, 10))
        screen.blit(self.background)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        ui.text(screen, (SCREEN_MIDDLE.x, 30), 'Game', color=(255, 0, 0))
        ui.text(screen, (SCREEN_MIDDLE.x, 45), 'Over', color=(255, 0, 0))
        
        self.menu_button.draw()
        if self.menu_button.check_click(events, 0):
            scene_manager.change_scene('menu')
        
        self.play_button.draw()
        if self.play_button.check_click(events, 0):
            scene_manager.change_scene('game')
        
        ui.text(screen, (SCREEN_BOTTOM_LEFT.x + 10, SCREEN_BOTTOM_LEFT.y - 20), 'ek3d', center=False)