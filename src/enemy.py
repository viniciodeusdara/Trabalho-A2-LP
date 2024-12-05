import pygame
from config import *
import math
import random

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
