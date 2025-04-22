from settings import *
import utils
from player import Player
from enemy import BlueEnemy, GreenEnemy
import ui

import math
import random


class Game:
    def __init__(self):
        if not background_music.get_busy():
            background_music.play(CYBORG_NINJA, -1)
        
        self.tiles = [
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 3, 0, 0, 0, 0, 0, 0, 3, 1],
            [1, 2, 3, 0, 0, 0, 0, 3, 2, 1],
            [1, 2, 1, 0, 0, 0, 0, 1, 2, 1],
            [1, 2, 1, 3, 3, 3, 3, 1, 2, 1],
        ]
        self.tile_data = self.get_tile_data()
        
        self.player = Player(screen, SCREEN_MIDDLE, self.tile_data['rect'])
        
        self.gem = pygame.image.load('assets/sprites/game/gem.png').convert_alpha()
        self.gem_rect = self.gem.get_rect(center=(SCREEN_MIDDLE.x, SCREEN_MIDDLE.y + 50))
        
        self.background = pygame.transform.box_blur(pygame.image.load('assets/sprites/backgrounds/background.png').convert(), 1)
        self.rock = pygame.image.load('assets/sprites/tiles/rock.png').convert()
        self.rock2 = pygame.image.load('assets/sprites/tiles/rock2.png').convert()
        self.rock3 = pygame.image.load('assets/sprites/tiles/rock3.png').convert()
        
        self.time = 0
        
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_rate = 2
        
        self.death_particles = utils.Particles(screen, 5, 3, (255, 0, 0), -15, pygame.Vector2(0, 490))
        
        self.camera_pos = pygame.Vector2(0, 0)
        self.screen_shake = 0
        
        self.score = 0
        self.enemies_killed = 0
        self.wave = 1
    
    
    def get_tile_data(self):
        tile_data = {
            'rect': [],
            'type': [],
        }
        for y, tile_row in enumerate(self.tiles):
            for x, tile_type in enumerate(tile_row):
                if not tile_type == 0:
                    tile_data['rect'].append(pygame.Rect((x * 32, y * 32), (32, 32)))
                    tile_data['type'].append(tile_type)
        return tile_data
    
    
    def draw_tiles(self):
        for tile_index in range(len(self.tile_data['rect'])):
            draw_tile = self.tile_data['rect'][tile_index].move(self.camera_pos)
            tile_type = self.tile_data['type'][tile_index]
            
            if tile_type == 1:
                draw_rock = pygame.transform.scale(self.rock, draw_tile.size)
            elif tile_type == 2:
                draw_rock = pygame.transform.scale(self.rock2, draw_tile.size)
            elif tile_type == 3:
                draw_rock = pygame.transform.scale(self.rock3, draw_tile.size)
            else:
                continue
            
            screen.blit(draw_rock, draw_tile)
    
    
    def gem_animation(self):
        self.gem_rect.centery = math.sin(self.time * 5) * 3 + SCREEN_MIDDLE.y + 50
        self.gem_rect.centerx = math.cos(self.time * 5) * 3 + SCREEN_MIDDLE.x
    
    
    def update_screen_shake(self, dt):
        if self.screen_shake > 0:
            self.screen_shake -= dt
            self.camera_pos = pygame.Vector2(random.randint(-1, 1), random.randint(-1, 1))
        elif not self.camera_pos == pygame.Vector2(0, 0):
            self.camera_pos = pygame.Vector2(0, 0)
    
    
    def update_enemies(self, dt, scene_manager):
        for enemy in self.enemies:
            enemy.update(dt, self.camera_pos)
            
            if enemy.rect.colliderect(self.player.rect):
                if self.player.jumping:
                    self.score += 1
                    self.enemies_killed += 1
                    self.death_particles.spawn_particles(enemy.pos, 7)
                    self.enemies.remove(enemy)
                    
                    utils.play_sound('assets/music/hurt.ogg', 5)
                    self.screen_shake = 0.2
                    screen.fill((255, 255, 255))
                    pygame.time.wait(50)
                    continue
                else:
                    utils.play_sound('assets/music/death.ogg', 5)
                    background_music.stop()
                    scene_manager.change_scene('game_over')
            
            if enemy.rect.colliderect(self.gem_rect):
                utils.play_sound('assets/music/death.ogg', 5)
                background_music.stop()
                scene_manager.change_scene('game_over')
        
        if self.enemies_killed >= 5:
            self.wave += 1
            self.enemy_spawn_rate = pygame.math.clamp(2 - self.wave / 4, 0.5, 2)
            self.enemies_killed = 0
        
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= self.enemy_spawn_rate:
            random_number = random.randint(0, 5)
            if random_number == 5:
                self.enemies.append(GreenEnemy(screen, (random.choice([32, SCREEN_WIDTH - 32]), -32), self.tile_data['rect'], self.player))
            else:
                self.enemies.append(BlueEnemy(screen, (random.choice([32, SCREEN_WIDTH - 32]), -32), self.tile_data['rect'], self.player))
            self.enemy_spawn_timer = 0
    
    
    # Called every frame
    def update(self, events, dt, scene_manager):
        screen.fill((64, 64, 64))
        screen.blit(self.background, (0, 0))
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        self.gem_animation()
        screen.blit(self.gem, self.gem_rect)
        
        self.draw_tiles()
        
        self.player.update(events, dt, self.camera_pos)
        
        self.update_enemies(dt, scene_manager)
        
        self.death_particles.update(dt, self.camera_pos)
        
        self.update_screen_shake(dt)
        
        ui.text(screen, (SCREEN_MIDDLE.x + 35, 30), 'Wave')
        ui.text(screen, (SCREEN_MIDDLE.x + 35, 45), f'{self.wave}')
        
        ui.text(screen, (SCREEN_MIDDLE.x - 35, 30), 'Score')
        ui.text(screen, (SCREEN_MIDDLE.x - 35, 45), f'{self.score}')
        
        self.time += dt
        # ui.text(screen, (SCREEN_MIDDLE.x + 70, 30), 'Time')
        # ui.text(screen, (SCREEN_MIDDLE.x + 70, 45), f'{round(self.time, 1)}')
