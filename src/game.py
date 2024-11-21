import pygame
import sys
from config import *
from sprites import *

class Game:
    def __init__(self):  
        pygame.init()

        pygame.display.set_caption("COLOCAR NOME DO JOGO")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.character_spritesheet = Spritesheet("public/images/coelho.png")
        self.terrain_spritesheet = Spritesheet("public/images/terrain.png")

    def create_map(self):
        for i, row in enumerate(MAPA_1):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    Player(self, j, i)

    def new(self):

        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_map()

        # while True:
        #     self.screen.fill((14, 219, 248))

        #     self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
        #     self.img_pos[0] += (self.movement[3] - self.movement[2]) * 5
        #     self.screen.blit(self.img, self.img_pos)

        #     img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
        #     if img_r.colliderect(self.collision_area):
        #         pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
        #     else:
        #         pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                
    def update(self):
        self.all_sprites.update()
        
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        self.clock.tick(60)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass


g = Game()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()