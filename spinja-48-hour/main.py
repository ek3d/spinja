# Import libraries
from settings import *
from scene import SceneManager

import pygame
import sys
pygame.init()


# Setup the game
pygame.display.set_caption('spinja')
clock = pygame.time.Clock()
scene_manager = SceneManager()


# Main loop
def main():
    can_update = True
    transition_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    transition_surface.fill((0, 0, 0))
    transition_position = pygame.Vector2(0, -SCREEN_HEIGHT)
    
    run = True
    while run:
        dt = clock.tick(FPS) / 1000
        events = pygame.event.get()
        for event in events:
            # Quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        if can_update:
            scene_manager.current_scene.update(events, dt, scene_manager)
        
        # Wipe down transition
        if scene_manager.transition:
            can_update = False
            transition_position.y += dt * 400
            
            if transition_position.y >= 0:
                can_update = True
            
            if transition_position.y >= SCREEN_HEIGHT:
                transition_position.y = -SCREEN_HEIGHT
                scene_manager.transition = False
            
            screen.blit(transition_surface, transition_position)
        pygame.display.update()

main()