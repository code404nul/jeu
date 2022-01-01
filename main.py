import pygame
import math
import time
from sound import SoundManager
pygame.init()
import random
import animation

import time

start = time.time()


monster_ded = 0
tir_num = 0
clock = pygame.time.Clock()
FPS = 90


class Game:
    def __init__(self):
        
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.comet_event = CometFallEvent(self)
        self.all_monsters = pygame.sprite.Group()
        self.sound_manager = SoundManager()
        self.font = pygame.font.Font("assets/font.ttf", 25)
        self.score = 0
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def add_score(self, points = 10):
        self.score += points

    def game_over(self):
        
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        self.sound_manager.play('game_over')

    def update(self, screen):

        
        score_text = self.font.render(f"Score : {self.score}", 1 , (0, 0, 0))
        screen.blit (score_text, (20, 20))

        screen.blit(self.player.image, self.player.rect)
        self.player.update_health_bar(screen)

        self.comet_event.update_bar(screen)


        self.player.update_animation()

        for projectile in self.player.all_projectiles:
            projectile.move()

        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        for comet in self.comet_event.all_comets:
            comet.fall()

        self.player.all_projectiles.draw(screen)
        self.all_monsters.draw(screen)

        self.comet_event.all_comets.draw(screen)

        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x < 900:
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > -15:
            self.player.move_left()
    

    def check_collision (self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False,pygame.sprite.collide_mask)

    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 3
        self.player = player
        self.image = pygame.image.load('assets\projectile.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        ale_rot = random.uniform(0, 1.5)
        self.angle += ale_rot
        self.image= pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.x += self.velocity
        self.rotate()
        for monster in  self.player.game.check_collision(self, self.player.game.all_monsters):
            self.remove()
            monster.damage(self.player.attack)

        if self.rect.x > 1000:
            self.remove 

class CometFallEvent:

    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 5
        self.game = game
        self.fall_mode = False
        self.all_comets = pygame.sprite.Group()

    def add_percent(self):
        self.percent += self.percent_speed / 200

    def is_full_loaded(self):
        return self.percent >= 100

    def reset_percent(self):
        self.percent = 0

    def meteor_fall(self):
        
        for i in range(1, 5):
            self.all_comets.add(Comet(self))

    def attempt_fall(self):

        if self.is_full_loaded() and len(self.game.all_monsters) == 0:
            print ("pluie de cometes ! Attention")
            self.meteor_fall()
            self.fall_mode = True

    def update_bar(self, surface): 

        self.add_percent()
        

        pygame.draw.rect(surface, (0, 0, 0), [
            0,
            surface.get_height() - 20,
            surface.get_width(),
            10
        ])
        pygame.draw.rect(surface, (187, 11, 11), [
            0,
            surface.get_height() - 20,
            (surface.get_width() / 100) * self.percent,
            10
        ])

class Comet(pygame.sprite.Sprite):

    def __init__(self, comet_event):
        super().__init__()
        
        self.image = pygame.image.load('assets/comet.png')
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 3)
        self.rect.x = random.randint (20 , 800)
        self.rect.y = - random.randint (0 , 800)
        self.comet_event = comet_event

    def remove(self):
        self.comet_event.all_comets.remove(self)
        self.comet_event.game.sound_manager.play ('meteorite')
        if len(self.comet_event.all_comets) == 0:
            print ("l'evenement est fini")
            self.comet_event.reset_percent()    
            game.start()

    def fall(self):
        self.rect.y += self.velocity

        if self.rect.y >= 500:
            print ("sol")
            self.remove()

            if len(self.comet_event.all_comets) == 0:
                print ("l'evenement est fini")
                self.comet_event.reset_percent()
                self.comet_event.fall_mode = False

        if self.comet_event.game.check_collision(
            self, self.comet_event.game.all_players
        ):
            print ("jouer touché ! ")
            self.remove()
            self.comet_event.game.player.damage(20)

class Player(animation.AnimateSprite):
    def __init__(self, game):
        super().__init__('player')
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 3
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def damage(self, amount):
        if self.health - amount > amount:
            self.health -= amount
        else:
            
            self.game.game_over()

    def update_animation(self):
        self.animate()

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))
        self.start_animation()
        tir_num + 1      
        self.game.sound_manager.play('tir')        
        

    
    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
        

    def move_left(self):
        self.rect.x -= self.velocity

    def update_health_bar (self, suface):

        bar_color = (28, 249, 0)
        back_bar_color = (150, 150, 150)

        bar_position = [self.rect.x + 50, self.rect.y + 25, self.health, 7]
        bar_position_back = [self.rect.x + 50, self.rect.y + 25, self.max_health, 7]

        pygame.draw.rect(suface, back_bar_color, bar_position_back)
        pygame.draw.rect(suface, bar_color, bar_position)

class Monster(animation.AnimateSprite):
    def __init__(self, game, name, size, offset=0):
        
        super().__init__(name, size)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.3
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint (0, 300)
        self.rect.y = 550 - offset
        self.loot_amount = 10
        self.start_animation()

    def set_speed(self, speed):
        
        self.default_speed = speed
        self.velocity = random.uniform(0.5, 1.5)

    def set_loot_amount(self, amount):
        self.loot_amount = amount


    def damage(self, amount):

        self.health-= amount
        if self.health<= 0:
            self.rect.x = 1000 + random.randint(0,300)
            self.velocity = random.uniform(1, self.default_speed)
            self.health = self.max_health
            self.game.add_score(self.loot_amount)

            if self.game.comet_event.is_full_loaded():
                self.game.all_monsters.remove(self)
                monster_ded + 1
                self.game.comet_event.attempt_fall()



    def update_animation(self):
        self.animate(loop=True)
    
    def update_health_bar (self, suface):

        bar_color = (28, 249, 0)
        back_bar_color = (150, 150, 150)

        bar_position = [self.rect.x + 10, self.rect.y - 7, self.health, 5]
        bar_position_back = [self.rect.x + 10, self.rect.y - 7, self.max_health, 5]

        pygame.draw.rect(suface, back_bar_color, bar_position_back)
        pygame.draw.rect(suface, bar_color, bar_position)


    def forward(self):
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity

        else:
            self.game.player.damage(self.attack)

class Mummy(Monster):
    
    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.set_speed(3)
        self.set_loot_amount(20)

class Alien(Monster):
    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), 130)
        self.health = 250
        self.max_health = 250
        self.attack = 0.8
        self.set_speed(1)
        self.set_loot_amount(80)



pygame.display.set_caption("Commet Shooter")
screen = pygame.display.set_mode((1080,720))

background = pygame.image.load('assets/bg.jpg')

banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner,(500, 500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button,(400,150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)

game = Game()

running = True
while running:

    screen.blit(background,(0,-200))
    if game.is_playing:
        game.update(screen)
    else:

        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            running = False
            pygame.quit()
            print ("fermeture du jeu")
            end = time.time()
            elapsed = end - start

            print ("------TIME------")
            print ("votre temps est de : " + str(elapsed) + "seconde")

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.launch_projectile()
                else:
                    game.start()
                    game.sound_manager.play('click')
                

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if play_button_rect.collidepoint(event.pos):
                
                game.start()
                game.sound_manager.play('click')

    clock.tick(FPS)

