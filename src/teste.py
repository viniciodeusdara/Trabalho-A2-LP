import pygame
import sys
import webbrowser

# Inicializa o Pygame
pygame.init()

# Dimensões da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lobby Soul Knight")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 149, 237)
BLACK = (0, 0, 0)
HOVER_GRAY = (50, 50, 50)
GRAY = (70, 70, 70)

# Fonte
title_font = pygame.font.Font(None, 74)
font = pygame.font.Font(None, 36)

# Carrega a imagem de fundo
background = pygame.image.load("public/images/background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Carrega as imagens dos botões
button_size = (60, 60)
megafone_img = pygame.image.load("public/images/som.png")
megafone_hover_img = pygame.image.load("public/images/somHover.png")
gear_img = pygame.image.load("public/images/settings.png")
gear_hover_img = pygame.image.load("public/images/settingsHover.png")
instagram_img = pygame.image.load("public/images/instagram.png")
instagram_hover_img = pygame.image.load("public/images/instagramHover.png")

# Carrega a imagem da seta para o botão de voltar
back_arrow_img = pygame.image.load("public/images/settings.png")
back_arrow_img = pygame.transform.scale(back_arrow_img, (40, 40))

# Redimensiona as imagens principais
megafone_img = pygame.transform.scale(megafone_img, button_size)
megafone_hover_img = pygame.transform.scale(megafone_hover_img, button_size)
gear_img = pygame.transform.scale(gear_img, button_size)
gear_hover_img = pygame.transform.scale(gear_hover_img, button_size)
instagram_img = pygame.transform.scale(instagram_img, button_size)
instagram_hover_img = pygame.transform.scale(instagram_hover_img, button_size)

# Função para desenhar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Função para desenhar texto justificado
def draw_justified_text(text, font, color, surface, rect, line_height):
    words = text.split(' ')
    lines = []
    current_line = words[0]

    # Quebra o texto em linhas que caibam no retângulo
    for word in words[1:]:
        if font.size(current_line + ' ' + word)[0] <= rect.width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    # Desenha cada linha no retângulo
    y = rect.top
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(midtop=(rect.centerx, y))
        surface.blit(text_surface, text_rect)
        y += line_height

# Texto explicativo (Lorem Ipsum)
instructions_text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Praesent volutpat nunc et ligula congue, nec tincidunt mi tincidunt. "
    "1. Use as setas para mover o personagem. "
    "2. Pressione espaço para interagir com objetos. "
    "3. Complete os desafios para avançar de nível. "
    "Boa sorte e divirta-se!"
)

# Função para criar botões
def draw_button(screen, x, y, width, height, text, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if mouse_click[0]:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_render, text_rect)
    return False

# Função principal para o lobby
def game_lobby():
    sound_button_rect = pygame.Rect(50, 300, *button_size)
    config_button_rect = pygame.Rect(50, 370, *button_size)
    instagram_button_rect = pygame.Rect(screen_width - 100, screen_height - 90, *button_size)

    settings_open = False
    como_jogar = False

    running = True
    while running:
        screen.blit(background, (0, 0))
        draw_text("THE GAME", title_font, WHITE, screen, screen_width // 2, 100)
        draw_text("Toque para iniciar", font, WHITE, screen, screen_width // 2, screen_height - 50)

        mouse_pos = pygame.mouse.get_pos()

        if sound_button_rect.collidepoint(mouse_pos):
            screen.blit(megafone_hover_img, sound_button_rect)
        else:
            screen.blit(megafone_img, sound_button_rect)

        if config_button_rect.collidepoint(mouse_pos):
            screen.blit(gear_hover_img, config_button_rect)
        else:
            screen.blit(gear_img, config_button_rect)

        if instagram_button_rect.collidepoint(mouse_pos):
            screen.blit(instagram_hover_img, instagram_button_rect)
        else:
            screen.blit(instagram_img, instagram_button_rect)

        if settings_open:
            pygame.draw.rect(screen, GRAY, (200, 150, 400, 300))  # Retângulo centralizado
            draw_text("Configurações", font, WHITE, screen, screen_width // 2, 170)

            # Botão de "Voltar" com a imagem da seta
            back_arrow_rect = pygame.Rect(210, 160, 40, 40)  # Posição da seta
            screen.blit(back_arrow_img, back_arrow_rect)

            # Detecta clique na área da seta
            if back_arrow_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                settings_open = False

            if draw_button(screen, 250, 230, 300, 50, "COMO JOGAR?", BLACK, HOVER_GRAY):
                como_jogar = True

            if draw_button(screen, 250, 300, 300, 50, "DIFICULDADE", BLACK, HOVER_GRAY):
                print("Botão 'DIFICULDADE' clicado")
            if draw_button(screen, 250, 370, 300, 50, "CRÉDITOS", BLACK, HOVER_GRAY):
                print("Botão 'CRÉDITOS' clicado")

        if como_jogar:
            # Exibe o retângulo e o texto explicativo justificado
            pygame.draw.rect(screen, GRAY, (200, 150, 400, 300))  # Retângulo centralizado
            draw_text("Como jogar?", font, WHITE, screen, screen_width // 2, 160)

            text_rect = pygame.Rect(210, 200, 380, 200)
            draw_justified_text(instructions_text, font, WHITE, screen, text_rect, line_height=30)

            # Botão de "Voltar" com a imagem da seta
            back_arrow_rect = pygame.Rect(210, 160, 40, 40)  # Posição da seta
            screen.blit(back_arrow_img, back_arrow_rect)

            # Detecta clique na área da seta
            if back_arrow_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                como_jogar = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button_rect.collidepoint(event.pos):
                    print("Botão de som clicado")
                elif config_button_rect.collidepoint(event.pos):
                    settings_open = True
                elif instagram_button_rect.collidepoint(event.pos):
                    webbrowser.open("https://www.instagram.com/fgvjr?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==")

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Executa a tela do lobby
game_lobby()
