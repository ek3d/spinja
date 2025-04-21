import pygame
pygame.mixer.init(44100, -16, 2, 64)


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 180

SCREEN_MIDDLE = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
SCREEN_TOP_LEFT = pygame.Vector2(0, 0)
SCREEN_TOP_RIGHT = pygame.Vector2(SCREEN_WIDTH, 0)
SCREEN_BOTTOM_RIGHT = pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_BOTTOM_LEFT = pygame.Vector2(0, SCREEN_HEIGHT)

VSYNC = 1
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CYBORG_NINJA = pygame.mixer.Sound('assets/music/cyborg_ninja.ogg')
VOXEL_REVOLUTION = pygame.mixer.Sound('assets/music/voxel_revolution.ogg')

background_music = pygame.mixer.Channel(5)
background_music.set_volume(0.25)
background_music.play(VOXEL_REVOLUTION, -1)
