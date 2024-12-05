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
    import pygame
from config import *
import math

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

        self.image = self.game.terrain1_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, current_horde):
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
        self.health = 20
        self.damage = 20
        self.current_horde = current_horde


    def update(self):
        self.move_towards_player()
        self.handle_collisions()
        self.avoid_overlap()
        self.damage_player()
    
    def take_damage(self, amount):
        """Reduz a saúde do inimigo."""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """Remove o inimigo ao morrer."""
        self.kill()

    def damage_player(self):
        """Causa dano ao jogador ao entrar em contato."""
        if self.rect.colliderect(self.game.player.rect):
            current_time = pygame.time.get_ticks()
            if current_time - self.game.player.last_damage_time > 1000:
                self.game.player.take_damage(self.damage)
                self.game.player.last_damage_time = current_time

    def move_towards_player(self):
        player_pos = self.game.player.rect.center
        enemy_pos = self.rect.center

        direction_x = player_pos[0] - enemy_pos[0]
        direction_y = player_pos[1] - enemy_pos[1]

        distance = (direction_x**2 + direction_y**2) ** 0.5
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed  

    def handle_collisions(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)

        for block in hits:
            dx = self.rect.centerx - block.rect.centerx
            dy = self.rect.centery - block.rect.centery
            
            if abs(dx) > abs(dy):
                if dx > 0: 
                    self.rect.left = block.rect.right
                else: 
                    self.rect.right = block.rect.left
            else: 
                if dy > 0:  
                    self.rect.top = block.rect.bottom
                else:  
                    self.rect.bottom = block.rect.top

    
    def avoid_overlap(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits:
            if enemy != self:
                dx = self.rect.centerx - enemy.rect.centerx
                dy = self.rect.centery - enemy.rect.centery

                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.rect.left = enemy.rect.right
                    else:
                        self.rect.right = enemy.rect.left
                else:
                    if dy > 0:
                        self.rect.top = enemy.rect.bottom
                    else:
                        self.rect.bottom = enemy.rect.top


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

class Boss(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, current_horde=0)
        self.health = 500
        self.damage = 50
        self.speed = 1
        self.image = self.game.boss_spritesheet.get_sprite(0, 0, TILESIZE * 2, TILESIZE * 2)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def special_attack(self):
        """O boss pode ter um ataque especial."""
        if random.random() < 0.01:
            print("O Boss realizou um ataque especial!")

    def update(self):
        self.move_towards_player()
        self.handle_collisions()
        self.avoid_overlap()
        self.damage_player()
        self.special_attack()
