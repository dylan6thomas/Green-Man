
import pygame
import os
import random
pygame.init()

global windowHeight, windowWidth
windowHeight = 640
windowWidth=640
window = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Green Man")
clock=pygame.time.Clock()
windowBorder=10

score=0

class Player(object):
    def __init__(self, charX, charY ,width, height):
        self.charX=charX
        self.charY=charY
        self.width=width
        self.height=height
        self.moveVel=7
        self.lastPressed=0
        self.left=False
        self.right=False
        self.up=False
        self.down=False
        self.shoot=False
        self.walkCount=0
        self.hitbox=(self.charX+10,self.charY+5,45,50)

    def draw(self,window):
        if self.walkCount+1>=9:
            self.walkCount=0
        if GreenMan.left:
            window.blit(walkLeft[int(self.walkCount/3)],(GreenMan.charX,GreenMan.charY))
            self.walkCount+=1
        elif GreenMan.right:
            window.blit(walkRight[int(self.walkCount/3)],(GreenMan.charX,GreenMan.charY))
            self.walkCount+=1
        elif GreenMan.up:
            window.blit(walkUp[int(self.walkCount/3)],(GreenMan.charX,GreenMan.charY))
            self.walkCount+=1
        elif GreenMan.down:
            window.blit(walkDown[int(self.walkCount/3)],(GreenMan.charX,GreenMan.charY))
            self.walkCount+=1
        else:
            window.blit(standingChar[GreenMan.lastPressed],(GreenMan.charX,GreenMan.charY))
        self.hitbox=(self.charX+10,self.charY+5,45,50)
        #pygame.draw.rect(window,(255,0,0),self.hitbox,2)

class Projectile():
    def __init__(self, x ,y , size ,color, facing,direction):
        self.x=x
        self.y=y
        self.size=size
        self.color=color
        self.vel=15
        self.direction=direction
        self.facing=facing
    def draw(self,window):
        if self.direction<2:
            pygame.draw.rect(window,self.color,(self.x,self.y,self.size[0],self.size[1]))
        elif self.direction>=2:
            pygame.draw.rect(window,self.color,(self.x,self.y,self.size[1],self.size[0]))
    
class Enemy():
   leftSlime=[pygame.image.load("LSlime.png"),pygame.image.load("LSlime2.png"),pygame.image.load("LSlime3.png")]
   rightSlime=[pygame.image.load("RSlime.png"),pygame.image.load("RSlime2.png"),pygame.image.load("RSlime2.png")] 
   i=0
   for sprites in leftSlime:
       leftSlime[i]=pygame.transform.rotozoom(sprites,0,0.1)
       i+=1
   i = 0
   for sprites in rightSlime:
       rightSlime[i]=pygame.transform.rotozoom(sprites,0,0.1)
       i+=1
   def __init__(self,width,height,end):
       self.end=end
       self.x=random.randint(0,windowWidth)
       self.y=random.randint(0,windowHeight)
       while self.x in range(self.end[0]-150,self.end[0]+200) and self.y in range(self.end[1]-150,self.end[1]+200):
           self.x=random.randint(0,windowWidth)
           self.y=random.randint(0,windowHeight)
       self.width=width
       self.height=height
       self.walkCount=0
       self.xvel=5
       self.yvel=5
       self.path=[(self.x,self.y),(self.end[0],self.end[1])]
       self.hitbox=(self.x+5,self.y+10,54,45)
       self.health=5
       self.visible=True
       if self.x>self.end[0]:
           self.xpath=-1
       else:
            self.xpath=1
       if self.y>self.end[1]:
           self.ypath=-1
       else:
           self.ypath=1



   def draw(self,win):
        if self.visible:
            self.move()
            if self.walkCount>=9:
                self.walkCount=0
            if self.xvel>0:
                window.blit(self.rightSlime[int(self.walkCount//3)],(self.x,self.y))
                self.walkCount+=1
            else:
                window.blit(self.leftSlime[int(self.walkCount//3)],(self.x,self.y))
                self.walkCount+=1
        
            pygame.draw.rect(window,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(window,(0,255,0),(self.hitbox[0],self.hitbox[1]-20,50-(10*(5-self.health)),10))
        

   def move(self):
              
            if self.xvel>0 and self.xpath==1:
                if self.x+self.xvel<self.path[1][0]:
                    self.x+=self.xvel
                else:
                    self.xvel*=-1
                    self.walkCount=0
            elif self.xvel<0 and self.xpath==1:
                if self.x+self.xvel>self.path[0][0]:
                    self.x+=self.xvel
                else:
                    self.xvel*=-1
                    self.walkCount=0
            elif self.xvel>0 and self.xpath==-1:
                if self.x-self.xvel>self.path[1][0]:
                    self.x-=self.xvel
                else:
                    self.xvel*=-1
                    self.walkCount=0
            else:
                if self.x-self.xvel<self.path[0][0]:
                    self.x-=self.xvel
                else:
                    self.xvel*=-1
                    self.walkCount=0
            if self.yvel>0 and self.ypath==1:
                if self.y+self.yvel<self.path[1][1]:
                    self.y+=self.yvel
                else:
                    self.yvel*=-1
                    self.walkCount=0
            elif self.yvel<0 and self.ypath==1:
                if self.y+self.yvel>self.path[0][1]:
                    self.y+=self.yvel
                else:
                    self.yvel*=-1
                    self.walkCount=0
            elif self.yvel>0 and self.ypath==-1:
                if self.y-self.yvel>self.path[1][1]:
                    self.y-=self.yvel
                else:
                    self.yvel*=-1
                    self.walkCount=0
            else:
                if self.y-self.yvel<self.path[0][1]:
                    self.y-=self.yvel
                else:
                    self.yvel*=-1
                    self.walkCount=0
            self.hitbox=(self.x+5,self.y+10,54,45)
        #pygame.draw.rect(window,(255,0,0),self.hitbox,2)
   def hit(self):
        self.visible=True
        if self.health>0:
            self.health-=1
        else:
            self.visible=False
        
       
 
#CHECK NAME OF PNG (MAY HAVE TO SAY .png.png!!!!!!!!!)
walkRight=[pygame.image.load("New Piskel-7.png.png"),pygame.image.load("New Piskel-8.png.png"),pygame.image.load("New Piskel-9.png.png"),pygame.image.load("New Piskel-8.png.png")]
walkLeft=[pygame.image.load("New Piskel-4.png.png"),pygame.image.load("New Piskel-5.png.png"),pygame.image.load("New Piskel-6.png.png"),pygame.image.load("New Piskel-5.png.png")]
walkDown=[pygame.image.load("New Piskel-1.png.png"),pygame.image.load("New Piskel-2.png.png"),pygame.image.load("New Piskel-3.png.png"),pygame.image.load("New Piskel-2.png.png")]
walkUp=[pygame.image.load("New Piskel-10.png.png"),pygame.image.load("New Piskel-11.png.png"),pygame.image.load("New Piskel-12.png.png"),pygame.image.load("New Piskel-11.png.png")]
standingChar=[pygame.image.load("New Piskel-8.png.png"),pygame.image.load("New Piskel-5.png.png"),pygame.image.load("New Piskel-2.png.png"),pygame.image.load("New Piskel-11.png.png")]
bg=pygame.image.load("BG.png")

killSound=pygame.mixer.Sound('SlimeDead.wav')
bulletSound=pygame.mixer.Sound('Laser.wav')
hitSound=pygame.mixer.Sound('SlimeHit.wav')
music=pygame.mixer.music.load('Automation.mp3')
pygame.mixer.music.play(-1)
oofSound=pygame.mixer.Sound('Oof.wav')

font=pygame.font.SysFont('comicsans',30,True)
GreenMan=Player(300,320,25,25)
bullets=[]
slime=[]
slime_count=0
shootLoop=0
lifeLoop=0
hit=False
lives=3
def redrawWin():
    window.blit(bg,(0,0)) 
    text=font.render('Score: '+ str(score)+"   Lives: "+ str(lives),1,((255,255,255)))
    window.blit(text,(windowHeight-300,20 ))
    for bullet in bullets:
        bullet.draw(window)
    GreenMan.draw(window)
    for slimes in slime:
        slimes.draw(window)
    if lives<=0:
        font1=pygame.font.SysFont('comicsans',60,True)
        text=font1.render("You Died!   Score:  "+ str(score),1,((255,255,255)))
        window.blit(text,(int(windowWidth/2-300),int(windowHeight/2) ))
        
    pygame.display.update()

gameOver=False
while not gameOver:
    clock.tick(15)
    if shootLoop>0:
        shootLoop+=1
    if shootLoop>4:
        shootLoop=0
    if lifeLoop>0:
        lifeLoop+=1
    if lifeLoop>50:
        lifeLoop=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            gameOver=True
    for bullet in bullets:
        for slimes in slime:
            if bullet.y-bullet.size[1]<slimes.hitbox[1]+slimes.hitbox[3] and bullet.y+bullet.size[1]>slimes.hitbox[1]:
                if bullet.x-bullet.size[0]>slimes.hitbox[0] and bullet.x-bullet.size[0] < slimes.hitbox[0]+slimes.hitbox[2]:
                    slimes.hit()
                    slimes.health-=1
                    hitSound.play()
                    if not slimes.visible:
                        slime.pop(slime.index(slimes))
                        killSound.play()
                    bullets.pop(bullets.index(bullet))
                    score+=100
                    break
                    hit=True
                else:
                    hit==False
        if bullet.x<640 and bullet.x>0 and bullet.direction<2:
            bullet.x+=bullet.vel*bullet.facing
        elif bullet.x>=640 or bullet.x<=0 and hit==False:
            bullets.pop(bullets.index(bullet))
        if bullet.y<640 and bullet.y>0 and bullet.direction>=2:
            bullet.y+=bullet.vel*bullet.facing
        elif bullet.y>=640 or bullet.y<=0 and hit==False:
            bullets.pop(bullets.index(bullet))
    for slimes in slime:
        if slimes.x+54>GreenMan.charX and slimes.x<GreenMan.charX+45 and lifeLoop==0:
            if slimes.y+45>GreenMan.charY and slimes.y<GreenMan.charY+50:
                lives-=1
                lifeLoop=1
                oofSound.play()
    pygame.display.update()
    keys=pygame.key.get_pressed()
    if keys[pygame.K_a] and GreenMan.charX>=windowBorder:
        GreenMan.charX-=GreenMan.moveVel
        GreenMan.left=True
        GreenMan.right=False
        GreenMan.lastPressed=1
    elif keys[pygame.K_d] and GreenMan.charX<=windowWidth-(windowBorder+2*GreenMan.width):
        GreenMan.charX+=GreenMan.moveVel
        GreenMan.right=True
        GreenMan.left=False
        GreenMan.lastPressed=0
        pygame.display.update()
    else:
        GreenMan.left=False
        GreenMan.right=False
        
    if keys[pygame.K_w] and GreenMan.charY>=windowBorder+GreenMan.height:
        GreenMan.charY-=GreenMan.moveVel
        GreenMan.up=True
        GreenMan.down=False
        GreenMan.lastPressed=3
        pygame.display.update()
    elif keys[pygame.K_s] and GreenMan.charY<=windowHeight-(windowBorder+2*GreenMan.height):
        GreenMan.charY+=GreenMan.moveVel
        GreenMan.down=True
        GreenMan.up=False
        GreenMan.lastPressed=2
    else:
        GreenMan.down=False
        GreenMan.up=False
    if GreenMan.up==False and GreenMan.down==False and GreenMan.left==False and GreenMan.right==False:
        walkCount=0
    if keys[pygame.K_p] and shootLoop==0:
        bulletSound.play()
        if GreenMan.lastPressed==1:
            facing=-1
        elif GreenMan.lastPressed==0:
            facing=1
        elif GreenMan.lastPressed==3:
            facing=-1
        elif GreenMan.lastPressed==2:
            facing=1
        if len(bullets)<10:
            bullets.append(Projectile(round(GreenMan.charX+GreenMan.width+8),round(GreenMan.charY+GreenMan.height+10),(10,5),(255,0,0),facing,GreenMan.lastPressed))
        shootLoop=1
    
    if len(slime)<8:
        if slime_count>20:
            slime.append(Enemy(28,18,(GreenMan.charX,GreenMan.charY)))
            slime_count=0
    slime_count+=1
    redrawWin()  
    if lives<=0:
        pygame.time.delay(5000)
        gameOver=True



