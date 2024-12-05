import pygame
from config import *
import math
import random

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction_x, direction_y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.spritesheet = self.game.attack_spritesheet

        self.frames = self.load_frames()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = 10

        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 1000

    def load_frames(self):
        """Carrega os quadros de animação do ataque a partir do spritesheet."""
        frames = []
        for i in range(4):
            frame = self.spritesheet.get_sprite(i * TILESIZE, 0, TILESIZE, TILESIZE)
            frames.append(frame)
        return frames

    def update(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[self.current_frame]

        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits:
            enemy.take_damage(40)
            self.kill()

        if pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

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

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.health = 200
        self.last_damage_time = 0
    
    def attack(self):
        """Cria um ataque direcionado ao mouse."""
        x, y = self.rect.center
        mouse_x, mouse_y = pygame.mouse.get_pos()

        direction_x = mouse_x - x
        direction_y = mouse_y - y
        distance = math.sqrt(direction_x**2 + direction_y**2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        Attack(self.game, x, y, direction_x, direction_y)

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