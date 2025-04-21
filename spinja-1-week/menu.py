from settings import *
import ui


class Menu:
    def __init__(self):
        if not background_music.get_busy():
            background_music.play(VOXEL_REVOLUTION, -1)
        
        self.play_button = ui.Button(screen, SCREEN_MIDDLE, 'Play')
        self.controls_button = ui.Button(screen, (SCREEN_MIDDLE.x, SCREEN_MIDDLE.y + 45), 'Credits', 10)
        
        self.background = pygame.transform.box_blur(pygame.image.load('assets/sprites/backgrounds/menu_background.png').convert(), 1)
    
    
    # Called every frame
    def update(self, events, dt, scene_manager):
        screen.fill((10, 10, 10))
        screen.blit(self.background)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        ui.text(screen, (SCREEN_MIDDLE.x, 30), 'Spinja')
        ui.text(screen, (SCREEN_MIDDLE.x, 45), '1 Week Edition')
        
        self.play_button.draw()
        if self.play_button.check_click(events, 0):
            background_music.stop()
            scene_manager.change_scene('game')
        
        self.controls_button.draw()
        if self.controls_button.check_click(events, 0):
            scene_manager.change_scene('credits')
        
        ui.text(screen, (SCREEN_BOTTOM_LEFT.x + 10, SCREEN_BOTTOM_LEFT.y - 20), 'ek3d', center=False)