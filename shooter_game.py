from random import *
from pygame import *
from time import time as timer

width = 700
height = 500
window = display.set_mode((width, height))
display.set_caption('Space shoot')
game = True

FPS = 60
clock = time.Clock()

galaxy = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')



amount_kill = 0



amount_lose = 0


num_bullet = 0

reload_time = False

life = 3

font.init()
font1 = font.Font(None, 30)
score_kill = font1.render(f'Вы уничтожили: '+ str(amount_kill), True, (100, 100, 100))
score_lose = font1.render(f'Вы упустили: '+ str(amount_lose), True, (100, 100, 100))
score_life = font1.render(f'Количество жизней: '+ str(life), True, (100, 100, 100))
font2 = font.SysFont('Arial', 70)

win = font2.render('Вы выйграли!', True, (100, 0, 0))
defeat = font2.render('Вы проиграли!', True, (100, 0, 0))

class GameSprite (sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y , player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрок
class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
    
    def fire (self):
        #keys = key.get_pressed()
        
        bulet = Bullet('bullet.png', self.rect.x + 20, Hero.rect.y, 20, 20 , 5)
        fire.play()
        bullets.add(bulet)
            
            

            
        

#----Создание противников------
class Enemy (GameSprite):
    direction = 'left'
    def update(self):
        self.rect.y += self.speed
        global amount_lose
        if self.rect.y >= 490:
            self.rect.y = 0
            self.rect.x = randint(10, 690)
            amount_lose+= 1

        
#класс пули
class Bullet (GameSprite):
    
    def update(self):
        global amount_kill
        self.rect.y -= self.speed
        if self.rect.y < 5:
            self.kill()



class Asteroid (Enemy):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 490:
            self.rect.y = 0
            self.rect.x = randint(10, 690)
        
            
            
        

asteroids = sprite.Group()


for i in range (3):
    asteroid = Asteroid('asteroid.png', randint(10, 690), 10, 65, 65, randint(1,4))
    asteroids.add(asteroid)


        



Hero = Player('rocket.png', 100, 400, 65, 65, 5)


monsters = sprite.Group()

for i in range(5):
    enemy = Enemy('ufo.png', randint(10, 690), 10, 65, 65, randint(1,4))
    monsters.add(enemy)

bullets = sprite.Group()







finish = False



while game:
    
    


    keys = key.get_pressed()
    


    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if reload_time == False and num_bullet < 5 :
                    num_bullet += 1
                    Hero.fire()
    
    if num_bullet >= 5 and reload_time == False:
        last_time = timer()
        reload_time = True
    
    


    if finish != True:
        window.blit(galaxy, (0, 0))
        
        #sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        #for sprite in sprite_list:
        #    amount_kill += 1
        #    enemy = Enemy('ufo.png', randint(10, 690), 10, 65, 65, randint(1,4))
        #    monsters.add(enemy)
    


        Hero.reset()
        Hero.update()
        
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        

        score_kill = font1.render(f'Вы уничтожили: '+ str(amount_kill), True, (100, 100, 100))
        score_lose = font1.render(f'Вы упустили: '+ str(amount_lose), True, (100, 100, 100))
        score_life = font1.render(f'Количество жизней: '+ str(life), True, (100, 100, 100))
        window.blit(score_kill, (0, 30))
        window.blit(score_lose, (0, 50))
        window.blit(score_life, (0, 10))


        #monsters.reset()
        
        #if sprite.collide_rect(Hero, exited):
        #    finish = True
        #    money.play()
        #    window.blit(win, (200,200))
        #if sprite.collide_rect(Hero, enemy) or sprite.collide_rect(Hero, wall_1) or sprite.collide_rect(Hero, wall_2) or sprite.collide_rect(Hero, wall_3) or sprite.collide_rect(Hero, wall_4):
        #    finish = True
        #    kick.play()
        #    window.blit(defeat, (200,200))

        if sprite.groupcollide(monsters, bullets, True, True):
            enemy = Enemy('ufo.png', randint(10, 690), 10, 65, 65, randint(1,4))
            monsters.add(enemy)   
            amount_kill += 1
        
        
        if amount_lose > 3 :
            finish = True
            window.blit(defeat, (200,200))
        if amount_kill > 10:
            finish = True
            window.blit(win, (200,200))

        if sprite.spritecollide(Hero, monsters, True) :
            life -= 1
            enemy = Enemy('ufo.png', randint(10, 690), 10, 65, 65, randint(1,4))
            monsters.add(enemy)

        if sprite.spritecollide(Hero, asteroids, True):
            life -= 1
            asteroid = Asteroid('asteroid.png', randint(10, 690), 10, 65, 65, randint(1,4))
            asteroids.add(asteroid)

        if reload_time == True:
            now_time = timer()

            if now_time - last_time < 1.5:
                reload = font2.render('Перезарядка', True, (150, 0, 0))
                window.blit(reload, (260, 400))
            else:
                num_bullet = 0
                reload_time = False



        if life == 0:
            finish = True
            window.blit(defeat, (200,200))

    clock.tick(FPS)
    display.update()