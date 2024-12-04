import pygame
import sys
from config import *
from sprites import *
from random import randint

class Game:
    def __init__(self):  
        pygame.init()

        pygame.display.set_caption("COLOCAR NOME DO JOGO")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True 
        self.character_spritesheet = Spritesheet("public/images/coelho.png")
        self.terrain_spritesheet = Spritesheet("public/images/terrain.png")
        self.enemy_spritesheet = Spritesheet("public/images/enemy.png")
        self.attack_spritesheet = Spritesheet("public/images/attack.png")
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.Group()
        self.player = Player(self, 5, 5)

    def create_map(self):
        for i, row in enumerate(MAPA_1):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                

        map_width = len(MAPA_1[0])
        map_height = len(MAPA_1)

        # Meio do lado superior
        Enemy(self, randint(1, map_width - 1), randint(1, map_height-1))
        Enemy(self, randint(1, map_width - 1), randint(1, map_height-1))
        Enemy(self, randint(1, map_width - 1), randint(1, map_height-1))
        Enemy(self, randint(1, map_width - 1), randint(1, map_height-1))
    
    def new(self):

        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_map()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Barra de espaço para atacar]
                    
                    self.player.attack()       
                
    def update(self):
        self.all_sprites.update()
        self.check_player_health()

    def check_player_health(self):
        """Verifica a saúde do jogador e finaliza o jogo se ela chegar a 0."""
        if self.player.health <= 0:
            self.playing = False

    def draw_health_bar(self):
        """Desenha a barra de saúde do jogador na tela."""
        health = self.player.health
        max_health = 100
        bar_length = 200
        bar_height = 20
        fill = max(0, (health / max_health) * bar_length)  # Garante que não seja negativo
        outline_rect = pygame.Rect(20, 20, bar_length, bar_height)
        fill_rect = pygame.Rect(20, 20, fill, bar_height)

        # Desenha a barra preenchida (vermelho)
        pygame.draw.rect(self.screen, (255, 0, 0), fill_rect)
        # Desenha o contorno da barra (branco)
        pygame.draw.rect(self.screen, (255, 255, 255), outline_rect, 2)
        
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        self.draw_health_bar()
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