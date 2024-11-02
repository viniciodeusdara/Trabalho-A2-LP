import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DEFINIR NOME")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 100, 255)
MOSS = (126, 140, 84)


font = pygame.font.Font(None, 50)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = font.render(text, True, WHITE)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, self.text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


start_button = Button(300, 150, 200, 60, "Start")
difficulty_button = Button(300, 250, 200, 60, "Difficulty")
options_button = Button(300, 350, 200, 60, "Options")


running = True
while running:
    screen.fill(MOSS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button.is_hovered(mouse_pos):
                print("Game started")
            elif difficulty_button.is_hovered(mouse_pos):
                print("Difficulty selected")
            elif options_button.is_hovered(mouse_pos):
                print("Options selected")


    for button in [start_button, difficulty_button, options_button]:
        if button.is_hovered(pygame.mouse.get_pos()):
            button.color = BLUE
        else:
            button.color = GRAY
        button.draw(screen)

    pygame.display.flip()
