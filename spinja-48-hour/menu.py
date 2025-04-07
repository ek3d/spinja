from settings import *
import ui


class Menu:
    def __init__(self):
        self.play_button = ui.Button(screen, SCREEN_MIDDLE, 'Play')
        
        self.background = pygame.image.load('assets/sprites/menu_background.png').convert()
    
    
    # Called every frame
    def update(self, events, dt, scene_manager):
        screen.fill((10, 10, 10))
        screen.blit(self.background)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        ui.text(screen, (SCREEN_MIDDLE.x, 30), 'SPINJA')
        ui.text(screen, (SCREEN_MIDDLE.x, 45), '48 Hour Edition')
        ui.text(screen, (SCREEN_MIDDLE.x, 125), "Don't let them get to the portal!", color=(255, 0, 0))
        
        self.play_button.draw()
        if self.play_button.check_click(events, 0):
            scene_manager.change_scene('game')
        
        ui.text(screen, (SCREEN_BOTTOM_LEFT.x + 10, SCREEN_BOTTOM_LEFT.y - 20), 'ek3d', center=False)