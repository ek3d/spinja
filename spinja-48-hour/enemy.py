import pygame
import utils


class Enemy:
    def __init__(self, screen, pos, tiles, player):
        self.screen = screen
        self.player = player
        
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(0, 0)
        
        self.tiles = tiles
        
        self.speed = 125
        self.jump_power = 200
        self.gravity = 980
        
        self.spritesheet = utils.color_swap_image(pygame.image.load('assets/sprites/player_spritesheet.png').convert_alpha(), (255, 0, 0), (0, 0, 255))
        self.jump_sprites = [
            (112, 0),
            (144, 0),
        ]
        self.current_sprite_pos = (0, 0)
        self.sprite_flip = False
        self.animation_handler = utils.AnimationHandler()
        
        self.rect = pygame.FRect((0, 0), (8, 32))
        self.rect.center = pos
        
        self.last_direction = 1
        
        self.on_ground = False
    
    
    def calculate_velocity(self, dt):
        self.velocity.x = pygame.math.lerp(self.velocity.x, utils.sign(self.player.pos.x - self.pos.x) * self.speed, dt * 3)
    
    
    def movement(self, dt):
        if not self.on_ground:
            self.velocity.y += self.gravity * dt
        
        # Handle X movement and collisions
        self.pos.x += self.velocity.x * dt
        self.rect.center = self.pos
        for tile in self.tiles:
            if self.rect.colliderect(tile):
                if self.velocity.x > 0:
                    self.pos[0] = tile.left - self.rect.width / 2
                if self.velocity.x < 0:
                    self.pos[0] = tile.right + self.rect.width / 2
                self.velocity.x = 0
        self.rect.center = self.pos
        
        # Handle Y movement and collisions
        self.pos.y += self.velocity.y * dt
        self.rect.center = self.pos
        self.on_ground = False
        for tile in self.tiles:
            if self.rect.colliderect(tile):
                if self.velocity.y < 0:
                    self.pos[1] = tile.bottom + self.rect.height / 2
                    self.velocity.y = 0
                if self.velocity.y > 0:
                    self.pos[1] = tile.top - self.rect.height / 2
                    self.on_ground = True
                    self.velocity.y = -self.jump_power
        self.rect.center = self.pos
    
    
    def animate(self, dt):
        if not self.velocity.x == 0:
            self.sprite_flip = self.velocity.x < 0
        
        self.current_sprite_pos = self.animation_handler.animate(self.jump_sprites, dt)
    
    
    def draw(self, camera_pos):
        draw_rect = self.rect.move((-camera_pos.x - 4, -camera_pos.y))
        self.screen.blit(
            pygame.transform.flip(
                utils.clip(
                    self.spritesheet,
                    self.current_sprite_pos,
                    (16, 32)
                ),
                self.sprite_flip,
                False
            ),
            draw_rect
        )
    
    
    # Called every frame
    def update(self, dt, camera_pos):
        self.calculate_velocity(dt)
        self.movement(dt)
        self.animate(dt)
        self.draw(camera_pos)