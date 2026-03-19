import pygame

class button():
    def __init__(self, scale, x,y,w,h, text, colour, hover_colour):
        sca=scale/100
        self.rect = pygame.Rect(sca*x, sca*y, sca*w, sca*h)
        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour
        self.current_colour = colour
        self.font = pygame.font.SysFont(None, round(sca*85))

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_colour, self.rect)
        text = self.font.render(self.text, True, (255,255,255))
        screen.blit(text,(self.rect.centerx - text.get_width()//2, self.rect.centery - text.get_height()//2))

    def update(self, mx, my):
        if self.rect.collidepoint(mx, my):
            self.current_colour = self.hover_colour
        else:
            self.current_colour = self.colour

    def clicked(self, mx, my):
        return self.rect.collidepoint(mx, my)