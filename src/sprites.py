import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
    
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.health = 100
        self.last_damage_time = 0
    
    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = "down"
            
    def take_damage(self, amount):
        """Reduz a saúde do jogador."""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """Lógica para quando o jogador morrer."""
        print("O jogador morreu!")

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        imagem = pygame.image.load("public/images/base_block.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(imagem, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 2 
        self.damage = 10

    def update(self):
        self.move_towards_player()
        self.handle_collisions()
        self.avoid_overlap()
        self.damage_player()

    def damage_player(self):
        """Causa dano ao jogador ao entrar em contato."""
        if self.rect.colliderect(self.game.player.rect):
            current_time = pygame.time.get_ticks()
            # Controla para que o dano seja periódico (ex.: 1 segundo entre danos)
            if current_time - self.game.player.last_damage_time > 1000:  # 1000 ms = 1 segundo
                self.game.player.take_damage(self.damage)
                self.game.player.last_damage_time = current_time

    def move_towards_player(self):
        player_pos = self.game.player.rect.center
        enemy_pos = self.rect.center

        # Calcular a direção do movimento
        direction_x = player_pos[0] - enemy_pos[0]
        direction_y = player_pos[1] - enemy_pos[1]

        # Normalizar o vetor de direção
        distance = (direction_x**2 + direction_y**2) ** 0.5
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Mover o inimigo em direção ao jogador
        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed  

    def handle_collisions(self):
        # Verificar colisões com blocos
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        for block in hits:
            if self.rect.right >= block.rect.left and self.rect.left <= block.rect.left:
                self.rect.right = block.rect.left
            if self.rect.left <= block.rect.right and self.rect.right >= block.rect.right:
                self.rect.left = block.rect.right
            if self.rect.bottom >= block.rect.top and self.rect.top <= block.rect.top:
                self.rect.bottom = block.rect.top
            if self.rect.top <= block.rect.bottom and self.rect.bottom >= block.rect.bottom:
                self.rect.top = block.rect.bottom
    
    def avoid_overlap(self):
        # Verificar colisões com outros inimigos
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits:
            if enemy != self:  
                if self.rect.right > enemy.rect.left and self.rect.left < enemy.rect.left:
                    self.rect.right = enemy.rect.left
                if self.rect.left < enemy.rect.right and self.rect.right > enemy.rect.right:
                    self.rect.left = enemy.rect.right
                if self.rect.bottom > enemy.rect.top and self.rect.top < enemy.rect.top:
                    self.rect.bottom = enemy.rect.top
                if self.rect.top < enemy.rect.bottom and self.rect.bottom > enemy.rect.bottom:
                    self.rect.top = enemy.rect.bottom