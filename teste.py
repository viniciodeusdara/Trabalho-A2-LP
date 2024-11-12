import pygame
import sys
import webbrowser
import time

# Inicializa o Pygame
pygame.init()

# Dimensões da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lobby Soul Knight")

# Cores
WHITE = (255, 255, 255)

# Carrega a imagem de fundo
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Carrega as imagens dos botões (estado normal e hover)
megafone_img = pygame.image.load("som.png")
megafone_hover_img = pygame.image.load("somHover.png")
gear_img = pygame.image.load("settings.png")
gear_hover_img = pygame.image.load("settingsHover.png")
instagram_img = pygame.image.load("instagram.png")
instagram_hover_img = pygame.image.load("instagramHover.png")

# Redimensiona as imagens para o tamanho dos botões
button_size = (60, 60)
megafone_img = pygame.transform.scale(megafone_img, button_size)
megafone_hover_img = pygame.transform.scale(megafone_hover_img, button_size)
gear_img = pygame.transform.scale(gear_img, button_size)
gear_hover_img = pygame.transform.scale(gear_hover_img, button_size)
instagram_img = pygame.transform.scale(instagram_img, button_size)
instagram_hover_img = pygame.transform.scale(instagram_hover_img, button_size)

# Fonte para o texto
title_font = pygame.font.Font(None, 74)  # Fonte maior para o título
font = pygame.font.Font(None, 36)

# Carrega o som de clique
click_sound = pygame.mixer.Sound("aperta-ao-play-neymar.mp3")  # Substitua pelo caminho do seu som

# Função para desenhar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Função principal para o lobby
def game_lobby():
    # Define as áreas dos botões (ajustados para ficarem mais para baixo)
    button1_rect = pygame.Rect(50, 300, *button_size)         # Botão de som (megafone)
    button2_rect = pygame.Rect(50, 370, *button_size)         # Botão de configurações (gear)
    instagram_button_rect = pygame.Rect(screen_width - 100, screen_height - 90, *button_size)  # Botão do Instagram

    # Loop principal do lobby
    running = True
    while running:
        screen.blit(background, (0, 0))  # Exibe o fundo

        # Exibe o título no topo
        draw_text("THE GAME", title_font, WHITE, screen, screen_width // 2, 100)

        """
        # Exibe aviso no topo direito
        draw_text("AVISO: Jogo feito por:", font, WHITE, screen, screen_width - 230, 30)
        draw_text("Lucas Dressler, Lucas Coelho, Roger Vinícius e Vinício Deusdará", font, WHITE, screen, screen_width - 230, 60)
        draw_text("EMAP - CD", font, WHITE, screen, screen_width - 230, 90)
        """
        # Desenha os botões com as imagens de hover
        mouse_pos = pygame.mouse.get_pos()
        
        # Escolhe a imagem de megafone conforme hover
        if button1_rect.collidepoint(mouse_pos):
            screen.blit(megafone_hover_img, button1_rect)
        else:
            screen.blit(megafone_img, button1_rect)
        
        # Escolhe a imagem de configurações conforme hover
        if button2_rect.collidepoint(mouse_pos):
            screen.blit(gear_hover_img, button2_rect)
        else:
            screen.blit(gear_img, button2_rect)
        
        # Escolhe a imagem do Instagram conforme hover
        if instagram_button_rect.collidepoint(mouse_pos):
            screen.blit(instagram_hover_img, instagram_button_rect)
        else:
            screen.blit(instagram_img, instagram_button_rect)

        # Exibe o texto "Toque para iniciar" na parte inferior
        draw_text("Toque para iniciar", font, WHITE, screen, screen_width // 2, screen_height - 50)

        # Verifica eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se foi clicado em algum botão
                if button1_rect.collidepoint(event.pos):
                    print("Botão de som clicado")
                elif button2_rect.collidepoint(event.pos):
                    print("Botão de configurações clicado")
                elif instagram_button_rect.collidepoint(event.pos):
                    # Abre o site do Instagram ao clicar no botão
                    webbrowser.open("https://www.instagram.com/fgvjr?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==")
                else:
                    # Toca o som se clicado fora dos botões
                    click_sound.play()
                    time.sleep(4.5)
                    click_sound.stop()

        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Executa a tela do lobby
game_lobby()
