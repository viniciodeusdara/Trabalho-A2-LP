import pygame
import sys
from config import *
from sprites import *
from enemy import *
from player import *
from random import randint
import time 

def game_lobby():
    pygame.init()
    click_sound = pygame.mixer.Sound("public/sounds/aperta-ao-play-neymar.mp3")
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Tela de Seleção de Dificuldade")
    font = pygame.font.Font(None, 50)

    musica_fundo = pygame.mixer.Sound('public/sounds/main_audio.mp3')
    musica_fundo.set_volume(0.5)
    musica_fundo.play(-1)

    background_image = pygame.image.load('public/images/fgv.png')
    background_image = pygame.transform.scale(background_image, (WIN_WIDTH, WIN_HEIGHT))

    title_image = pygame.image.load('public/images/gametitle.png')
    title_image = pygame.transform.scale(title_image, (400, 150))

    running = True
    difficulty = None

    while running:
        screen.blit(background_image, (0, 0))

        title_rect = title_image.get_rect(center=(WIN_WIDTH // 2, 100)) 
        screen.blit(title_image, title_rect)


        play_button = pygame.Rect(WIN_WIDTH // 2 - 150, 200, 300, 50)

        pygame.draw.rect(screen, (0, 0, 255), play_button)

        play_text = font.render("Jogar", True, (255, 255, 255))
       
        screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2, play_button.centery - play_text.get_height() // 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    difficulty = "Fácil"
                    musica_fundo.stop()
                    time.sleep(0.5)
                    click_sound.play()
                    time.sleep(4.5)
                    click_sound.stop()
                    running = False

        pygame.display.update()

    pygame.quit()
    return difficulty

class Game:
    
    def __init__(self, difficulty):
        pygame.init()
        pygame.display.set_caption("Escape the Matrix")
        musica_fundo = pygame.mixer.Sound('public/sounds/main_audio.mp3')
        musica_fundo.set_volume(0.5)
        musica_fundo.play(-1)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.difficulty = difficulty
        self.character_spritesheet = Spritesheet("public/images/coelho.png")
        self.terrain1_spritesheet = Spritesheet("public/images/terrain.png")
        self.terrain2_spritesheet = Spritesheet("public/images/ground.png")
        self.enemy_spritesheet = Spritesheet("public/images/enemy.png")
        self.boss_spritesheet = Spritesheet("public/images/camacho.png")
        self.attack_spritesheet = Spritesheet("public/images/attack.png")
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.Group()
        self.player = Player(self, 5, 5)
        self.current_horde = 1
        self.enemies_per_horde = 7
        self.horde_cleared = False
        self.horde_message_time = 0
        
        self.time_to_show_enemies = None

    def create_map(self):
        print("Criando mapa...")
        for i, row in enumerate(MAPA_1):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P" and not hasattr(self, 'player'):
                    self.player = Player(self, j, i)

        
        if self.time_to_show_enemies is None:
            self.time_to_show_enemies = pygame.time.get_ticks()
        
        map_width = len(MAPA_1[0])
        map_height = len(MAPA_1)

        
            # Cria os inimigos somente após o tempo de espera de 5 segundos
        if self.current_horde * self.enemies_per_horde <= 25:
            for _ in range(self.current_horde * self.enemies_per_horde):
                Enemy(self, randint(1, map_width - 1), randint(1, map_height - 1), self.current_horde)
        else:
            for _ in range(20):
                Enemy(self, randint(1, map_width - 1), randint(1, map_height - 1), self.current_horde)

    def check_horde_status(self):
        if not self.enemies and not self.horde_cleared:
            self.horde_cleared = True
            self.horde_message_time = pygame.time.get_ticks()

    def spawn_next_horde(self):
        current_time = pygame.time.get_ticks()
        if self.horde_cleared and current_time - self.horde_message_time > 2000:
            self.horde_cleared = False
            self.current_horde += 1
            self.enemies_per_horde += 1
            print(f"Próxima horda: {self.current_horde}")
        
            if self.current_horde % 5 == 0:  # Spawn do Boss na quinta horda
                self.spawn_boss()
            else:
                self.create_map()

    def spawn_boss(self):
        print("Boss está spawnando!")
        map_width = len(MAPA_1[0])
        map_height = len(MAPA_1)
    
        self.boss = Boss(self, randint(1, map_width - 1), randint(1, map_height - 1))
        self.all_sprites.add(self.boss)

    def draw_horde_message(self):
        if self.horde_cleared:
            font = pygame.font.Font(None, 50)
            if self.current_horde == 1:
                text = font.render(f"Horda {self.current_horde}...", True, (0, 0, 0))
            else:
                text = font.render(f"Horda Eliminada! Horda {self.current_horde}...", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.all_sprites.add(self.player)

        self.create_map()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.attack()

    def update(self):
        self.all_sprites.update()
        self.check_player_health()
        self.check_horde_status()
        self.spawn_next_horde()

        if hasattr(self, 'boss'):
            self.boss.update()

    def check_player_health(self):
        """Verifica a saúde do jogador e finaliza o jogo se ela chegar a 0."""
        if self.player.health <= 0:
            try:
                # Tenta carregar e exibir a imagem de Game Over
                gameover_image = pygame.image.load('public/images/game_over_img.png')
                gameover_image = pygame.transform.scale(gameover_image, (500, 300))
                gameover_rect = gameover_image.get_rect(center=(WIN_WIDTH // 2, 300))

                # Desenha a imagem na tela
                self.screen.blit(gameover_image, gameover_rect)

                # Espera 3 segundos sem travar o jogo (usando um temporizador)
                if not hasattr(self, 'gameover_time'):  # Inicia o temporizador
                    self.gameover_time = pygame.time.get_ticks()

                # Verifica se passaram 3 segundos
                if pygame.time.get_ticks() - self.gameover_time >= 3000:
                    self.playing = False  # Finaliza o jogo após 3 segundos
                pygame.display.update()  # Atualiza a tela

            except pygame.error as e:
                print(f"Erro ao carregar a imagem: {e}")

    def draw_health_bar(self):
        """Desenha a barra de saúde do jogador na tela."""
        health = self.player.health
        max_health = 200  # Aumenta a saúde máxima a cada horda
        if health > max_health:
            health = max_health
        bar_length = 100
        bar_height = 20
        fill = max(0, (health / max_health) * bar_length)
        outline_rect = pygame.Rect(20, 20, bar_length, bar_height)
        fill_rect = pygame.Rect(20, 20, fill, bar_height)

        pygame.draw.rect(self.screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), outline_rect, 2)
    
    def draw_boss_health(self):
        if hasattr(self, 'boss'):
            health = self.boss.health
            max_health = 800
            bar_length = 400
            bar_height = 20
            fill = max(0, (health / max_health) * bar_length)
            outline_rect = pygame.Rect(WIN_WIDTH // 2 - bar_length // 2, 20, bar_length, bar_height)
            fill_rect = pygame.Rect(WIN_WIDTH // 2 - bar_length // 2, 20, fill, bar_height)

            pygame.draw.rect(self.screen, (255, 0, 0), fill_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), outline_rect, 2)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        self.draw_health_bar()
        self.draw_horde_message()
        self.draw_boss_health()
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


if __name__ == "__main__":
    difficulty = game_lobby()
    game = Game(difficulty)
    game.new()
    while game.running:
        game.main()
        game.game_over()

pygame.quit()
sys.exit()
