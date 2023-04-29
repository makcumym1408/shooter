from time import time as timer
from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, speed, player_x, player_y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 15, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)
      
lost = 0
score = 0
num_fire = 0
lifes = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

font.init()
font2 = font.SysFont('Arial', 80)
font1 = font.SysFont('Arial', 50)
win = font2.render('You win!', True, (255, 255, 0))
lose = font2.render('You lose!', True, (255, 255, 0))

window = display.set_mode((700,500))
display.set_caption('ସାହାଯ୍ୟ')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

player = Player('rocket.png', 10, 350, 400, 80, 100)
monsters = sprite.Group()
for i in range(4):
    monster = Enemy('ufo.png', randint(1, 2), randint(80, 620), -40, 80, 50)
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid('asteroid.png', randint(1, 2), randint(80, 620), -40, 80, 50)
    asteroids.add(asteroid)
bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

clock = time.Clock()
FPS = 1200

game = True
finish = False
rel_time = False
while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if finish != True:
        
        p_m_collide = sprite.spritecollide(player, monsters, False)
        p_a_collide = sprite.spritecollide(player, asteroids, False)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(1, 3), randint(80, 620), -40, 80, 50)
            monsters.add(monster)
        window.blit(background, (0,0))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render('Пропущено:'+ str(lost), 1, (100, 50, 130))
        text_score = font1.render('Убито:'+ str(score), 1, (100, 50, 130))
        window.blit(text_lose,(10, 50))
        window.blit(text_score,(10, 20))
        if score >= 10:
            finish = True
            window.blit(win, (200,200))
        if lost >= 4 or p_m_collide or p_a_collide:
            finish = True
            window.blit(lose, (200,200))
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                text_wait = font1.render('Подождите, перезарядка', 1, (200, 0, 0))
                window.blit(text_wait, (220, 460))
            else:
                rel_time = False
                num_fire = 0
    else:
            for i in monsters:
                i.kill()
                del i
            for i in bullets:
                i.kill()
                del i
    display.update()
    clock.tick(FPS)