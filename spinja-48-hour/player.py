import pygame
import utils


class Player:
    def __init__(self, screen, pos, tiles):
        self.screen = screen
        
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(0, 0)
        
        self.tiles = tiles
        
        self.speed = 175
        self.jump_power = 350
        self.gravity = 980
        
        self.spritesheet = pygame.image.load('assets/sprites/player_spritesheet.png').convert_alpha()
        self.idle_sprites = [
            (0, 0),
            (16, 0),
            (32, 0),
            (48, 0),
        ]
        self.run_sprites = [
            (64, 0),
            (80, 0),
            (64, 0),
            (96, 0),
        ]
        self.jump_sprites = [
            (112, 0),
            (144, 0),
        ]
        self.current_sprite_pos = (0, 0)
        self.sprite_flip = False
        self.animation_handler = utils.AnimationHandler()
        
        self.rect = pygame.FRect((0, 0), (8, 32))
        self.rect.center = pos
        
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        
        self.last_direction = 1
        
        self.on_ground = False
    
    
    def input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and self.on_ground:
                    self.velocity.y = -self.jump_power
                    self.jumping = True
                
                if event.key == pygame.K_a:
                    self.moving_left = True
                    self.last_direction = -1
                elif event.key == pygame.K_d:
                    self.moving_right = True
                    self.last_direction = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.moving_left = False
                elif event.key == pygame.K_d:
                    self.moving_right = False
    
    
    def movement(self, dt):
        if not self.on_ground:
            self.velocity.y += self.gravity * dt
        
        # Handle X movement and collisions
        self.velocity.x = (self.moving_right - self.moving_left) * self.speed
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
                    self.jumping = False
        self.rect.center = self.pos
    
    
    def animate(self, dt):
        if self.velocity.x == 0:
            self.current_sprite_pos = self.animation_handler.animate(self.idle_sprites, dt)
        else:
            self.current_sprite_pos = self.animation_handler.animate(self.run_sprites, dt)
            
            self.sprite_flip = self.velocity.x < 0
        
        if not self.on_ground:
            if self.velocity.y < 0:
                self.current_sprite_pos = self.animation_handler.animate(self.jump_sprites, dt)
            else:
                self.current_sprite_pos = (128, 0)
    
    
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
    def update(self, events, dt, camera_pos):
        self.input(events)
        self.movement(dt)
        self.animate(dt)
        self.draw(camera_pos)