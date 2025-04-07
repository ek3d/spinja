import pygame


# Must call pygame.font.init() in order to initialize the font variable
pygame.font.init()
font = pygame.font.Font('assets/kenney_mini_square_mono.ttf')


# Draw Text
def text(screen, position, text, font_size=12, color=(255, 255, 255), anti_alias=False, center=True):
    # Change font size
    if not font.point_size == font_size:
        font.point_size = font_size
    
    # Render font with arguments
    font_rendered = font.render(text, anti_alias, color)
    if center:
        # Center text by using rect's center property
        rect = font_rendered.get_rect(center=position)
        
        # Blit text on screen
        screen.blit(font_rendered, rect)
    else:
        # Blit text on screen
        screen.blit(font_rendered, position)


# Button Class
class Button:
    def __init__(self, screen, position, text, font_size=12, text_color=(0, 0, 0), color=(255, 255, 255)):
        self.screen = screen
        self.position = position
        
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        
        self.normal_sprite = pygame.transform.scale2x(pygame.image.load('assets/sprites/button.png').convert_alpha())
        self.click_sprite = pygame.transform.scale2x(pygame.image.load('assets/sprites/button_click.png').convert_alpha())
        self.current_sprite = self.normal_sprite
        # self.rect = pygame.Rect((0, 0), (128, 64))
        self.rect = self.normal_sprite.get_rect(center=position)
        
        self.color = color
    
    
    def draw(self):
        # Draw button with rounded corners
        # pygame.draw.rect(self.screen, self.color, self.rect, border_radius = 100)
        self.screen.blit(self.current_sprite, self.rect)
        text(self.screen, (self.position[0], self.position[1]), self.text, self.font_size, self.text_color)
    
    
    def check_click(self, events, volume):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            for event in events:
                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.current_sprite = self.click_sprite
                    return False
                
                # Let go
                if event.type == pygame.MOUSEBUTTONUP:
                    self.current_sprite = self.normal_sprite
                    # Register when button is let go
                    return True
        else:
            self.current_sprite = self.normal_sprite
        
        return False