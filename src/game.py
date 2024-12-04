import pygame
import sys
from config import *
from sprites import *
from random import randint
import time 

def game_lobby():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("ESCAPE THE MATRIX")
    font = pygame.font.Font(None, 50)
    pygame.mixer.init()

    # Carrega a imagem de fundo
    background_image = pygame.image.load('public/images/fgv.png')
    background_image = pygame.transform.scale(background_image, (WIN_WIDTH, WIN_HEIGHT))  # Redimensiona para preencher a tela

    running = True
    difficulty = None

    while running:
        # Desenha a imagem de fundo
        screen.blit(background_image, (0, 0))
        # Desenha o título
        title_text = font.render("Escape the Matrix!", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Botões de dificuldade
        easy_button = pygame.Rect(WIN_WIDTH // 2 - 150, 200, 300, 50)
        medium_button = pygame.Rect(WIN_WIDTH // 2 - 150, 280, 300, 50)
        hard_button = pygame.Rect(WIN_WIDTH // 2 - 150, 360, 300, 50)

        pygame.draw.rect(screen, (0, 0, 255), easy_button)
        pygame.draw.rect(screen, (0, 0, 255), medium_button)
        pygame.draw.rect(screen, (0, 0, 255), hard_button)

        easy_text = font.render("Fácil", True, (255, 255, 255))
        medium_text = font.render("Médio", True, (255, 255, 255))
        hard_text = font.render("Difícil", True, (255, 255, 255))

        screen.blit(easy_text, (easy_button.centerx - easy_text.get_width() // 2, easy_button.centery - easy_text.get_height() // 2))
        screen.blit(medium_text, (medium_button.centerx - medium_text.get_width() // 2, medium_button.centery - medium_text.get_height() // 2))
        screen.blit(hard_text, (hard_button.centerx - hard_text.get_width() // 2, hard_button.centery - hard_text.get_height() // 2))

        # Verifica os eventos de clique
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    difficulty = "Fácil"
                    running = False
                elif medium_button.collidepoint(event.pos):
                    difficulty = "Médio"
                    running = False
                elif hard_button.collidepoint(event.pos):
                    difficulty = "Difícil"
                    running = False

        pygame.display.update()

    pygame.quit()
    return difficulty

class Game:
    def __init__(self, difficulty):  # Recebe a dificuldade escolhida
        pygame.init()
        pygame.display.set_caption("COLOCAR NOME DO JOGO")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.difficulty = difficulty  # Armazena a dificuldade
        self.character_spritesheet = Spritesheet("public/images/coelho.png")
        self.terrain1_spritesheet = Spritesheet("public/images/terrain.png")
        self.terrain2_spritesheet = Spritesheet("public/images/ground.png")
        self.enemy_spritesheet = Spritesheet("public/images/enemy.png")
        self.attack_spritesheet = Spritesheet("public/images/attack.png")
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.Group()
        self.player = Player(self, 5, 5)
        self.current_horde = 1
        self.enemies_per_horde = 8
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

        if self.current_horde * self.enemies_per_horde <= 25:
            for _ in range(self.current_horde * self.enemies_per_horde):
                Enemy(self, randint(1, map_width - 1), randint(1, map_height - 1), self.current_horde)
        else:
            for _ in range(25):
                Enemy(self, randint(1, map_width - 1), randint(1, map_height - 1), self.current_horde)

    def create_map_2(self):
        for i, row in enumerate(MAPA_2):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
            # Não recrie o jogador se ele já existir
                if column == "P" and not hasattr(self, 'player'):
                    self.player = Player(self, j, i)

        map_width = len(MAPA_2[0])
        map_height = len(MAPA_2) 

        # Spawnar inimigos da horda
        if self.current_horde * self.enemies_per_horde <= 25:
            for _ in range(self.current_horde * self.enemies_per_horde):
                Enemy(self, randint(1, map_width - 1), randint(1, map_height - 1), self.current_horde)
        else:
            for _ in range(25):
                Enemy(self, randint(1, map_width - 1), randint(1, map_height - 1), self.current_horde)

    def create_map_boss(self):
        for i, row in enumerate(MAPA_2):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
            # Não recrie o jogador se ele já existir
                if column == "P" and not hasattr(self, 'player'):
                    self.player = Player(self, j, i)

        map_width = len(MAPA_2[0])
        map_height = len(MAPA_2) 

        # Spawnar boss
        Boss(self, randint(1, map_width - 1), randint(1, map_height - 1))

    def check_horde_status(self):
        if not self.enemies and not self.horde_cleared:
            self.horde_cleared = True
            self.horde_message_time = pygame.time.get_ticks()

    def spawn_next_horde(self):
        current_time = pygame.time.get_ticks()
        if self.horde_cleared and current_time - self.horde_message_time > 2000:  # Exibe a mensagem por 2 segundos
            self.horde_cleared = False
            self.current_horde += 1
            self.enemies_per_horde += 1  # Aumenta a dificuldade
            if self.current_horde == 2:
                self.create_map_2()
            elif self.current_horde != 2:
                self.create_map()
            if self.current_horde == 6:  # Boss após a 5ª horda
                self.spawn_boss()

    def spawn_boss(self):
        map_width = len(MAPA_1[0])
        map_height = len(MAPA_1)
    # Crie o Boss em um local aleatório no mapa
        x = randint(1, map_width - 1)
        y = randint(1, map_height - 1)
        self.boss = Boss(self, x, y)  # Cria o Boss
        self.all_sprites.add(self.boss)
        self.enemies.add(self.boss)

    def draw_horde_message(self):
        if self.horde_cleared:
            font = pygame.font.Font(None, 50)
            text = font.render(f"Horda Eliminada! Horda {self.current_horde}...", True, (0, 0, 0))
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
        if self.current_horde == 1:
            self.create_map()
        elif self.current_horde == 6:
            self.create_map_boss()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Barra de espaço para atacar
                    self.player.attack()

    def update(self):
        self.all_sprites.update()
        self.check_player_health()
        self.check_horde_status()
        self.spawn_next_horde()

    # Se houver um boss, atualizar ele também
        if hasattr(self, 'boss'):
            self.boss.update()

    def check_player_health(self):
        """Verifica a saúde do jogador e finaliza o jogo se ela chegar a 0."""
        if self.player.health <= 0:
            self.playing = False

    def draw_health_bar(self):
        """Desenha a barra de saúde do jogador na tela."""
        health = self.player.health
        max_health = 100 + self.current_horde * 20  # Aumenta a saúde máxima a cada horda
        if health > max_health:
            health = max_health
        bar_length = 200
        bar_height = 20
        fill = max(0, (health / max_health) * bar_length)  # Garante que não seja negativo
        outline_rect = pygame.Rect(20, 20, bar_length, bar_height)
        fill_rect = pygame.Rect(20, 20, fill, bar_height)

        # Desenha a barra preenchida (vermelho)
        pygame.draw.rect(self.screen, (255, 0, 0), fill_rect)
        # Desenha o contorno da barra (branco)
        pygame.draw.rect(self.screen, (255, 255, 255), outline_rect, 2)
    
    def draw_boss_health(self):
        if hasattr(self, 'boss'):
            health = self.boss.health
            max_health = 500
            bar_length = 400
            bar_height = 20
            fill = max(0, (health / max_health) * bar_length)  # Garante que não seja negativo
            outline_rect = pygame.Rect(WIN_WIDTH // 2 - bar_length // 2, 20, bar_length, bar_height)
            fill_rect = pygame.Rect(WIN_WIDTH // 2 - bar_length // 2, 20, fill, bar_height)

            # Desenha a barra preenchida (vermelho)
            pygame.draw.rect(self.screen, (255, 0, 0), fill_rect)
            # Desenha o contorno da barra (branco)
            pygame.draw.rect(self.screen, (255, 255, 255), outline_rect, 2)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        self.draw_health_bar()
        self.draw_horde_message()
        self.draw_boss_health()  # Desenha a barra de saúde do Boss, se existir
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

# Função principal
if __name__ == "__main__":
    difficulty = game_lobby()  # Chama o lobby
    g = Game(difficulty)  # Passa a dificuldade para o jogo
    g.new()
    while g.running:
        g.main()
        g.game_over()

pygame.quit()
sys.exit()
