import pygame
from pygame.locals import *
import time
import random
file=open('scores.txt','r')
best=file.readline()
vel=0.35
offset=-200
laze_vel=5
pause=False

pygame.init()
PIXEL=50
COUNT=30
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
running=True

backgroundImg=image=pygame.image.load("space_rs/back.png")
backgroundImg=image =pygame.transform.scale(backgroundImg, (WIDTH, HEIGHT))
#Enemy
RED_SHIP=image=pygame.image.load("space_rs/red ship.png")
RED_SHIP=image =pygame.transform.scale(RED_SHIP, (PIXEL, PIXEL))
BLUE_SHIP=image=pygame.image.load("space_rs/blue ship.png")
BLUE_SHIP=image =pygame.transform.scale(BLUE_SHIP, (PIXEL, PIXEL))
#RED_SHIP=image=pygame.image.load("rs/red ship.png")
#RED_SHIP image =pygame.transform.scale(RED_SHIP, (PIXEL, PIXEL))

#Player
YELLOW_SHIP=image=pygame.image.load("space_rs/yellow ship.png")
YELLOW_SHIP=image =pygame.transform.scale(YELLOW_SHIP, (2*PIXEL,2*PIXEL))

#lazers
BLUE_LASER=image=pygame.image.load("space_rs/laze blue.png")
BLUE_LASER=image =pygame.transform.scale(BLUE_LASER, (PIXEL+15, PIXEL+15))
RED_LASER=image=pygame.image.load("space_rs/laze red.png")
RED_LASER=image =pygame.transform.scale(RED_LASER, (PIXEL+15, PIXEL+15))
YELLOW_LASER=image=pygame.image.load("space_rs/laze yellow.png")
YELLOW_LASER=image =pygame.transform.scale(YELLOW_LASER, (2*PIXEL,2*PIXEL))

class Player:
    
    def __init__(self,x,y,health=100):
        self.img=YELLOW_SHIP
        self.laze_img=YELLOW_LASER
        self.x=x
        self.y=y
        self.screen=WIN
        self.laze=[]
        self.timer=0
        self.mask = pygame.mask.from_surface(self.img)
        self.health=health
    def draw(self):
        self.screen.blit(self.img,(self.x,self.y))
        for laze in self.laze:
            if laze.off_screen(HEIGHT):
                self.laze.remove(laze)
            else:
                laze.draw()
        pygame.draw.rect(self.screen,(255,0,0),(self.x,self.y+100,100,10))
        pygame.draw.rect(self.screen,(0,255,0),(self.x,self.y+100,self.health,10))
    def shot(self):
        if self.timer==0:
            self.laze.append(Laze(self.x,self.y,self.laze_img,-10))
            self.timer=1
    def countdown(self):
        if self.timer >= COUNT:
            self.timer=0
        if self.timer > 0:
            self.timer+=1
                
class Laze:
    def __init__ (self,x,y,img,vel):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)
        self.screen=WIN
        self.vel=vel
    def draw(self):
        self.move()
        self.screen.blit(self.img,(self.x,self.y))
    def move(self):
        self.y += self.vel
    def off_screen(self,HEIGHT):
        if self.y<-10 or self.y>HEIGHT:
            return True
    def collision(self,obj):
        return colli(self, obj)

class Enemy:
    enemy_list={'red': (RED_SHIP,RED_LASER),
                'blue': (BLUE_SHIP,BLUE_LASER)}
    def __init__(self,x,y,color,health=10):
        self.x=x
        self.y=y
        self.screen=WIN
        self.laze=[]
        self.img,self.laze_img=self.enemy_list[color]
        self.mask=pygame.mask.from_surface(self.img)
        self.timer=0
    def move(self):
        self.y += vel
    def shoot(self):
        if random.randrange(1,50)==5 and pause==False and self.timer==0:
            self.laze.append(Laze(self.x,self.y+40,self.laze_img,laze_vel))
            self.timer=1
    def draw(self):
        self.move()
        self.screen.blit(self.img,(self.x,self.y))
        for laze in self.laze:
            if laze.off_screen(HEIGHT):
                self.laze.remove(laze)
            else:
                laze.draw()
    def countdown(self):
        if self.timer >= COUNT:
            self.timer=0
        if self.timer > 0:
            self.timer+=1

def highscore(score):
    global best
    font = pygame.font.SysFont("Time News Roman", 50,False,False)
    surface = font.render(f"SCORE:{score}",True, (255,255,255))
    WIN.blit(surface, (570,25))

    if score > int(best) and pause==True:
        file=open('scores.txt','w')
        file.write(str(score))
        file.close()
def lvl(level):
    font = pygame.font.SysFont("Time News Roman", 50,False,False)
    surface = font.render(f"LEVEL:{level}",True, (255,255,255))
    WIN.blit(surface, (25,25))

def colli(obj1,obj2):
    offset = (int(obj2.x - obj1.x), int(obj2.y - obj1.y))
    return obj1.mask.overlap(obj2.mask, offset)

def reset():
    player=Player(300,600)
    wave=5
    enemies=[]
    level=1

def text_gameover():
    font = pygame.font.SysFont("Time News Roman", 100,False,False)
    surface = font.render("GAMEOVER!",True, (255,255,255))
    WIN.blit(surface, (150,300))

def main():
    global running, offset, vel, pause
    player = Player(300,600)
    enemies=[]
    enemy=Enemy(300,100,'red')
    wave=5
    level=0
    score=0
    def control():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x-=3
        if keys[pygame.K_RIGHT]:
            player.x+=3
        if keys[pygame.K_UP]:
            player.y-=3
        if keys[pygame.K_DOWN]:
            player.y+=3
        if keys[pygame.K_SPACE]:
            player.shot()

    while running:
        WIN.blit(backgroundImg,(0,0))
        player.countdown()
        player.draw()
        if len(enemies)==0:
            for i in range(wave):
                enemies.append(Enemy(random.randrange(0,WIDTH-50),random.randrange(offset,-50),random.choice(['red','blue'])))
            wave+=5
            offset-=200
            level+=1
        lvl(level)
        highscore(score)
        for enemy in enemies:
            enemy.draw()
            enemy.countdown()
            if enemy.y >0:    
                enemy.shoot()

        time.sleep(0.007)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                quit()
        if pause==False:
            control()
        for laze in player.laze:
            for enemy in enemies:
                if colli(enemy,laze):
                    enemies.remove(enemy)
                    score+=1
                    try:
                        player.laze.remove(laze)
                    except:
                        pass
            
        for enemy in enemies:
            for laze in enemy.laze:
                if colli(player,laze):
                    player.health-=10
                    enemy.laze.remove(laze)

        for enemy in enemies:
            if enemy.y>HEIGHT:
                player.health-=10
                enemies.remove(enemy)
        
        for enemy in enemies:
            if colli(player,enemy):
                player.health-=10
                enemies.remove(enemy)
        
        if player.health==0:
            vel=0
            pause=True
        
        if pause == True:
            text_gameover()
        pygame.display.flip()
def main_menu():

    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(backgroundImg, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        title_high = title_font.render(f"HIGHSCORE: {best}", 1, (255,255,255))
        WIN.blit(title_high, (190, 450))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()