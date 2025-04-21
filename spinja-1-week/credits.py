from settings import *
import ui


class Credits:
    def __init__(self):
        self.credits = [
            'Spinja',
            'Credits',
            '',
            'Font',
            'Kenney Mini Square Mono',
            '',
            'Music and Sounds',
            'Cyborg Ninja: Kevin MacLeod',
            'Voxel Revolution: Kevin MacLeod',
            'Hit/Hurt Sound: sfxr.me',
            'Death/Explosion Sound: sfxr.me',
            '',
            'Sprites',
            'Backgrounds: Ansimuz Legacy Collection',
            'Tiles: Ansimuz Legacy Collection',
            'Player and Gem: ek3d',
            '',
            'UI',
            'Button: ek3d',
            '',
            'Made in Pygame-CE 2.5.2',
            'Compiled with Pygbag',
        ]
        
        self.credits_surface = pygame.Surface((SCREEN_WIDTH, len(self.credits) * 15 + 60))
        self.credits_pos = pygame.Vector2(0, 0)
        
        for index, credit in enumerate(self.credits):
            ui.text(self.credits_surface, (SCREEN_MIDDLE.x, index * 15 + 60), credit, 10)
        
        self.skip_text_surface = pygame.Surface((SCREEN_WIDTH, 30))
        ui.text(self.skip_text_surface, (SCREEN_MIDDLE.x, 15), 'Click again to skip')
        self.skip_text_showing = False
    
    
    # Called every frame
    def update(self, events, dt, scene_manager):
        screen.fill((0, 0, 0))
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.skip_text_showing:
                    scene_manager.change_scene('menu')
                self.skip_text_showing = True
        
        self.credits_pos.y -= dt * 25
        screen.blit(self.credits_surface, self.credits_pos)
        
        if self.skip_text_showing:
            screen.blit(self.skip_text_surface, (0, SCREEN_HEIGHT - 30))
        
        if self.credits_pos.y <= -self.credits_surface.get_height() - 25:
            scene_manager.change_scene('menu')