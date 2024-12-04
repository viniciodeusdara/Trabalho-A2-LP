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
        self.current_horde = 1
        self.enemies_per_horde = 10
        self.horde_cleared = False
        self.horde_message_time = 0

    def create_map(self):
        for i, row in enumerate(MAPA_1):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
            # Não recrie o jogador se ele já existir
                if column == "P" and not hasattr(self, 'player'):
                    self.player = Player(self, j, i)

        map_width = len(MAPA_1[0])
        map_height = len(MAPA_1)

    # Spawnar inimigos da horda
        for _ in range(self.enemies_per_horde):
            Enemy(self, randint(1, map_width - 1), randint(1, map_height - 1))
    
    def check_horde_status(self):
        if not self.enemies and not self.horde_cleared:
            self.horde_cleared = True
            self.horde_message_time = pygame.time.get_ticks()

    def spawn_next_horde(self):
        current_time = pygame.time.get_ticks()
        if self.horde_cleared and current_time - self.horde_message_time > 2000:  # Exibe a mensagem por 2 segundos
            self.horde_cleared = False
            self.current_horde += 1
            self.enemies_per_horde += 5  # Aumenta a dificuldade
            self.create_map()
    
    def draw_horde_message(self):
        if self.horde_cleared:
            font = pygame.font.Font(None, 50)
            text = font.render("Horda Eliminada! Próxima Horda...", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

    def new(self):
        self.playing = True

    # Reinitialize apenas os grupos necessários
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

    # Adicione o jogador ao grupo de sprites
        self.all_sprites.add(self.player)

    # Crie o mapa e os inimigos
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
        self.check_horde_status()
        self.spawn_next_horde()


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
        self.draw_horde_message()
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