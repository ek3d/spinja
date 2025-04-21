import pygame
import random


class AnimationHandler():
    def __init__(self, speed=10):
        self.current_index = 0
        self.speed = speed
    
    def animate(self, keyframes, dt):
        self.current_index += self.speed * dt
        
        self.current_index %= len(keyframes)
        
        return keyframes[int(self.current_index)]


def clip(surface, pos, size):
    rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    return surface.subsurface(rect).copy()


def color_swap_image(image, color, swapped_color):
    color_mask = pygame.mask.from_threshold(image, color, threshold=(1, 1, 1, 255))
    color_change_surf = color_mask.to_surface(setcolor=swapped_color, unsetcolor=(0, 0, 0, 0))
    image_copy = image.copy()
    image_copy.blit(color_change_surf, (0, 0))
    return image_copy


def sign(number):
    return -1 if number < 0 else (1 if number > 0 else 0)


def play_sound(path, volume=1, loops=0):
    music = pygame.mixer.Sound(path)
    music.set_volume(volume)
    music.play(loops)
    return music


class Particles:
    def __init__(self, screen, amount, time, color, size_change, direction):
        self.screen = screen
        
        self.particles = []
        
        self.amount = amount
        self.time = time
        self.color = color
        self.size_change = size_change
        self.direction = direction
    
    
    def spawn_particles(self, pos, size):
        for _ in range(self.amount):
            self.particles.append([pygame.Vector2(pos), size, pygame.Vector2(random.randint(-50, 50), random.randint(-100, -50)), 0])
    
    
    def update(self, dt, camera_pos):
        for particle in self.particles:
            particle[0] += particle[2] * dt # Move Particle
            particle[1] += self.size_change * dt # Change size
            particle[2] += self.direction * dt # Apply acceleration
            particle[3] += dt # Increment time since birth
            
            # Draw particle
            pygame.draw.circle(self.screen, self.color, particle[0] - camera_pos, particle[1])
            
            # Particle death
            if particle[3] >= self.time:
                self.particles.remove(particle)