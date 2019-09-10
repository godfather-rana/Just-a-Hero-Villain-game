##Ameet Kumar Rana, Army Institute Of Technology, Pune
##handle : godfather_rana

import pygame
pygame.init()

win = pygame.display.set_mode((852,480))

pygame.display.set_caption("My game")

black = (0,0,0)

walkLeft=[pygame.image.load('assets/animation/hero/L1.png'),pygame.image.load('assets/animation/hero/L2.png'),pygame.image.load('assets/animation/hero/L3.png'),pygame.image.load('assets/animation/hero/L4.png'),pygame.image.load('assets/animation/hero/L5.png'),pygame.image.load('assets/animation/hero/L6.png'),pygame.image.load('assets/animation/hero/L7.png'),pygame.image.load('assets/animation/hero/L8.png'),pygame.image.load('assets/animation/hero/L9.png')]

walkRight=[pygame.image.load('assets/animation/hero/R1.png'),pygame.image.load('assets/animation/hero/R2.png'),pygame.image.load('assets/animation/hero/R3.png'),pygame.image.load('assets/animation/hero/R4.png'),pygame.image.load('assets/animation/hero/R5.png'),pygame.image.load('assets/animation/hero/R6.png'),pygame.image.load('assets/animation/hero/R7.png'),pygame.image.load('assets/animation/hero/R8.png'),pygame.image.load('assets/animation/hero/R9.png')]

walkLeftV=[pygame.image.load('assets/animation/villain/L1E.png'),pygame.image.load('assets/animation/villain/L2E.png'),pygame.image.load('assets/animation/villain/L3E.png'),pygame.image.load('assets/animation/villain/L4E.png'),pygame.image.load('assets/animation/villain/L5E.png'),pygame.image.load('assets/animation/villain/L6E.png'),pygame.image.load('assets/animation/villain/L7E.png'),pygame.image.load('assets/animation/villain/L8E.png'),pygame.image.load('assets/animation/villain/L9E.png'),pygame.image.load('assets/animation/villain/L10E.png'),pygame.image.load('assets/animation/villain/L11E.png')]
    
walkRightV=[pygame.image.load('assets/animation/villain/R1E.png'),pygame.image.load('assets/animation/villain/R2E.png'),pygame.image.load('assets/animation/villain/R3E.png'),pygame.image.load('assets/animation/villain/R4E.png'),pygame.image.load('assets/animation/villain/R5E.png'),pygame.image.load('assets/animation/villain/R6E.png'),pygame.image.load('assets/animation/villain/R7E.png'),pygame.image.load('assets/animation/villain/R8E.png'),pygame.image.load('assets/animation/villain/R9E.png'),pygame.image.load('assets/animation/villain/R10E.png'),pygame.image.load('assets/animation/villain/R11E.png')]

    
bg = pygame.image.load('assets/images/bg.jpg')
#char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('assets/music/effects/bullet.wav')
hitSound = pygame.mixer.Sound('assets/music/effects/hit.wav')

pygame.mixer.music.load('assets/music/sound/music.mp3')

pygame.mixer.music.play(-1)
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.jumpCount = 10
        self.vel = 5
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.box = (self.x + 20,self.y + 10,25,55)
        self.health = 10
        self.visible = True
        
    def draw(self):
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            
            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                    self.walkCount += 1 
                
                elif self.right:
                    win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                    self.walkCount += 1 
                            
            else:
                if self.left:
                    win.blit(walkLeft[0],(self.x,self.y))
                else:
                    win.blit(walkRight[0],(self.x,self.y))
            
            #pygame.draw.rect(win, (255,0,0), (self.x+10,self.y,50,5))          #red bar
            #pygame.draw.rect(win, (0,0,255), (self.x+10,self.y - 10,50 - score * 5,5))          #blue bar
            #pygame.draw.rect(win, black, (self.x+10,self.y,50,5),1)
            self.box = (self.x + 20,self.y + 10,25,55)
            #pygame.draw.rect(win, black, self.box,1)
    
    def hit(self):
        self.x = 150
        self.y = 200
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0
        font1 = pygame.font.SysFont('Arian',60,True)
        text = font1.render('-3',1,(200,100,25))
        win.blit(text,( 250 - (text.get_width()/2),250))
        pygame.display.update()
        
        i=0
        while i<100:
            pygame.time.delay(10)
            i += 1
        
    

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    
    def draw(self):
        pygame.draw.circle(win, self.color , (self.x,self.y), self.radius)
        
class enemy(object):
    def __init__(self,x,y,width,height,end):
        self.x = x     
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 40                                 # increasing value of this variable will increase the difficulty level
        #self.health = 10
        self.box = (self.x + 16,self.y + 8,33,50)
        self.visible = True
        
    def draw(self):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            
            if self.vel > 0:
                win.blit(walkRightV[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(walkLeftV[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            
            pygame.draw.rect(win, (255,0,0), (self.x+10,self.y - 10,50,5))          #red bar
            neg = score if score>0 else 0
            pygame.draw.rect(win, (0,0,255), (self.x+10,self.y - 10,50 - neg * 5,5))          #blue bar
            pygame.draw.rect(win, black, (self.x+10,self.y - 10,50,5),1)            #bar boundary
            self.box = (self.x + 16,self.y + 8,33,50)
            #pygame.draw.rect(win, black, self.box, 1)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]+35:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x + self.vel > 0 - self.width/2:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
               
    def hit(self):
        if score == 11:
            self.visible = False
        print('hit')
        
def drawGameWindow():                                   #drawing the whole game window
    #global walkCount
    win.blit(bg, (0,0) )
    
    text = font.render('Score:' + str(score),1, black)
    if villain.visible == False:
        font1 = pygame.font.SysFont('Arian',100,True,True)
        test = font1.render("You Won!!!",1,(255,0,0))
        win.blit(test,(250,350))
    
    fontName = pygame.font.SysFont('Algerian',25,True)
    t = fontName.render('Godfather_rana V/S Noob Players :)',1,(200,126,50))
    win.blit(t,(10,10))
    
    win.blit(text, (770,10))
    hero.draw()
    villain.draw()
    
    for bullet in bullets:
        bullet.draw()
    pygame.display.update()
    
score = 0 
hero = player(150,200,64,64)   
villain = enemy(200,400,64,64,800) 
bullets = []
run = True
shootLoop = 0
font = pygame.font.SysFont('Arian', 20, True, True)
while run:                                          #main loop
    clock.tick(27)
    
    #pygame.time.delay(150)
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 4:
        shootLoop = 0
    
    if villain.visible == True:
        if hero.box[1] + hero.box[3] > villain.box[1] and hero.box[1] < villain.box[1] + villain.box[3]:
            if hero.box[0] + hero.box[2] > villain.box[0] and hero.box[0] < villain.box[0] + villain.box[2]:    
                score -= 3
                hero.hit()
                        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for bullet in bullets:
        
        if villain.visible == True:
            if bullet.y + bullet.radius > villain.box[1] and bullet.y - bullet.radius < villain.box[1] + villain.box[3]:
                if bullet.x + bullet.radius > villain.box[0] and bullet.x - bullet.radius < villain.box[0] + villain.box[2]:
                    bullets.pop(bullets.index(bullet))
                    villain.hit()
                    hitSound.play()
                    score += 1
                
        if bullet.x < 852 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_x] and shootLoop == 0:
        bulletSound.play()
        if hero.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 2:            #for the number of bullets 
            bullets.append(projectile(round(hero.x + hero.width//2) , round(hero.y + hero.height//2) , 6, (40,0,0),facing))
        
        shootLoop = 1
        
    if keys[pygame.K_LEFT] and hero.x > hero.vel:
        hero.x -= hero.vel
        hero.left = True 
        hero.right = False
        hero.standing = False
        
    elif keys[pygame.K_RIGHT] and hero.x < 852 - hero.width - hero.vel:
        hero.x += hero.vel
        hero.right = True
        hero.left = False
        hero.standing = False
        
    else:
        #hero.right = False 
        #hero.left = False
        hero.standing = True
        hero.walkCount = 0
    if not(hero.isJump):
        if keys[pygame.K_UP] and hero.y > hero.vel:
            hero.y -= hero.vel
        if keys[pygame.K_DOWN] and hero.y < 480 - hero.height - hero.vel:
            hero.y += hero.vel
        if keys[pygame.K_SPACE]:    
            hero.isJump = True
            hero.right = False 
            hero.left = False
            hero.walkCount = 0
    else:
        if hero.jumpCount >= -10:
            sign = 1
            if hero.jumpCount < 0:
                sign = -1
            hero.y -= (hero.jumpCount ** 2) * 0.5 * sign
            hero.jumpCount -= 1
            
        else:
            hero.jumpCount = 10
            hero.isJump = False
            
    
    drawGameWindow()
    
pygame.quit()
            
