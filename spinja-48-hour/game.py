from settings import *
import utils
from player import Player
from enemy import Enemy
import ui

import math
import random


class Game:
    def __init__(self):
        self.tiles = [
            pygame.Rect((SCREEN_BOTTOM_LEFT.x, SCREEN_BOTTOM_LEFT.y - 10), (SCREEN_WIDTH, 10)),
            pygame.Rect(SCREEN_TOP_LEFT, (10, SCREEN_HEIGHT)),
            pygame.Rect((SCREEN_TOP_RIGHT.x - 10, SCREEN_TOP_RIGHT.y), (10, SCREEN_HEIGHT)),
            pygame.Rect((10, SCREEN_MIDDLE.y), (75, 90)),
            pygame.Rect((SCREEN_WIDTH - 85, SCREEN_MIDDLE.y), (75, 90)),
        ]
        
        self.player = Player(screen, SCREEN_MIDDLE, self.tiles)
        
        self.portal = pygame.image.load('assets/sprites/portal.png').convert_alpha()
        self.portal_rect = self.portal.get_rect(center=(SCREEN_MIDDLE.x, SCREEN_MIDDLE.y + 50))
        
        self.background = pygame.image.load('assets/sprites/background.png').convert()
        self.rock = pygame.image.load('assets/sprites/rock.png').convert()
        
        self.time = 0
        
        self.enemies = [Enemy(screen, (32, -32), self.tiles, self.player)]
        self.enemy_spawn_timer = 0
        self.enemy_spawn_rate = 2
        
        self.death_particles = utils.Particles(screen, 15, 3, (255, 255, 255), -15, pygame.Vector2(0, 490))
        
        self.camera_pos = pygame.Vector2(0, 0)
        
        self.score = 0
        self.enemies_killed = 0
        self.wave = 1
    
    
    def draw_tiles(self):
        for tile in self.tiles:
            draw_tile = tile.move(self.camera_pos)
            # pygame.draw.rect(screen, (128, 15, 56), draw_tile)
            draw_rock = pygame.transform.scale(self.rock, draw_tile.size)
            screen.blit(draw_rock, draw_tile)
    
    
    def portal_animation(self):
        self.portal_rect.centery = math.sin(self.time) * 5 + SCREEN_MIDDLE.y + 50
    
    
    # Called every frame
    def update(self, events, dt, scene_manager):
        screen.fill((64, 64, 64))
        screen.blit(self.background)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        self.portal_animation()
        screen.blit(self.portal, self.portal_rect)
        
        self.player.update(events, dt, self.camera_pos)
        
        for enemy in self.enemies:
            enemy.update(dt, self.camera_pos)
            
            if enemy.rect.colliderect(self.player.rect):
                if self.player.jumping:
                    self.score += 1
                    self.enemies_killed += 1
                    self.death_particles.spawn_particles(enemy.pos, 7)
                    self.enemies.remove(enemy)
                    continue
                else:
                    scene_manager.change_scene('game_over')
            
            if enemy.rect.colliderect(self.portal_rect):
                scene_manager.change_scene('game_over')
        
        if self.enemies_killed >= 5:
            self.wave += 1
            self.enemy_spawn_rate = 2 - self.wave / 4
            self.enemies_killed = 0
        
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= self.enemy_spawn_rate:
            self.enemies.append(Enemy(screen, (random.choice([32, SCREEN_WIDTH - 32]), -32), self.tiles, self.player))
            self.enemy_spawn_timer = 0
        
        self.draw_tiles()
        
        self.death_particles.update(dt, self.camera_pos)
        
        ui.text(screen, (SCREEN_MIDDLE.x, 30), 'Wave')
        ui.text(screen, (SCREEN_MIDDLE.x, 45), f'{self.wave}')
        
        ui.text(screen, (SCREEN_MIDDLE.x - 70, 30), 'Score')
        ui.text(screen, (SCREEN_MIDDLE.x - 70, 45), f'{self.score}')
        
        self.time += dt
        ui.text(screen, (SCREEN_MIDDLE.x + 70, 30), 'Time')
        ui.text(screen, (SCREEN_MIDDLE.x + 70, 45), f'{round(self.time, 1)}')