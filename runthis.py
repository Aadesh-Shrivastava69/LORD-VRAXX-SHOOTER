import pygame , sys
import math
import random
from pygame import mixer

pygame.init()

game_state = 'menu'



    



#creating screen 
screen = pygame.display.set_mode((800 , 600))
pygame.display.set_caption("lord vraxx shooter")



#load buttons

start_img = pygame.image.load("start_img.png").convert_alpha()
play_again = pygame.image.load("play_again.png").convert_alpha()
#quit = pygame.image.load("")


# button class

class Button():
    def __init__(self,x,y,image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale) , int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):

        action = False
        global game_state
        
        #position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                print('clicked')
                action = True
           

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False



        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action
        
         

#button instances 
start_button = Button(205,120,start_img , 0.1)
retry_button = Button(205,200,play_again , 0.1)



#background

bg= pygame.image.load('bgg.png')

#bgm
mixer.music.load('bgm.wav')
mixer.music.play(-1)

#player

playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 482
playerX_change = 0
playerY_change = 0

#enemy 

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enimies = 5

for i in range(num_enimies):

    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#bullet

bulletimg = pygame.image.load('bullet.png')
bulletX= 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.2

#cant see bullet 

bullet_state = 'ready'

#score

score_value = 0

#font

font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over

over_font = pygame.font.Font('freesansbold.ttf',56)


#defining

def show_score(x,y):
    score = font.render('score :' + str(score_value),True, (255,255,255))
    screen.blit(score , (x,y))

def game_over():
    global game_state
    

        

    


def player(x,y):
    screen.blit(playerimg,(x,y))
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
def firebullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
   dist =  math.sqrt((math.pow(enemyX - bulletX,2))+ (math.pow(enemyY - bulletY,2)))
  
   if dist <= 27:
    return True
   
   else :
    return False

def gameloop():
    global playerX
    global playerY
    global playerX_change
    global playerY_change
    global bulletX
    global bulletY
    global bulletX_change
    global bulletY_change
    global bullet_state
    global score_value
    global game_state

    running = True
    while running:

        if game_state == 'menu':


            screen.fill((0,0,0))

            if start_button.draw():
                game_state = 'play'
                print("play")
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = 'play'
                    
                

                    
            pygame.display.update()
            
        elif game_state == 'play':

            # rgb background

            screen.fill((2,0,0))
            screen.blit(bg,(0,0))


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -0.4   
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 0.4
                    if event.key == pygame.K_SPACE:
                        if bullet_state is 'ready':
                            bulletX = playerX
                            firebullet(bulletX,bulletY)   
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0  
                     
    # player boundary

            playerX += playerX_change
            if playerX <= 0:
                playerX = 0

            elif playerX >= 736:
                playerX = 736

    #enemy movement

            for i in range(num_enimies):

                #GAME OVER
                if enemyY[i] >= 440:
                    for j in range(num_enimies):
                        
                        enemyY[j] = 2000
                        playerX = 1000
                        playerY = 1000
                    game_over()
                        
                        
                    end = mixer.Sound('LORD.wav')
                    end.play()
                    break
                

                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 0.3
                    enemyY[i] += enemyY_change[i]

                elif enemyX[i] >= 700:
                    enemyX_change[i] = -0.3
                    enemyY[i] += enemyY_change[i]
#collision
                collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
                if collision:

                    exlpodesound= mixer.Sound('collision.wav')
                    exlpodesound.play()
                    bulletY = 480
                    bullet_state = 'ready'
                    score_value += 1
                    enemyX[i]= random.randint(0,736)
                    enemyY[i] = random.randint(0,150)
                enemy(enemyX[i],enemyY[i],i)    
            

#bullet movement
            if bullet_state is 'fire':
                firebullet(bulletX,bulletY)
                bulletY -= bulletY_change
            if bulletY <= 0:
                bulletY = 480
                bullet_state = 'ready'



            player(playerX,playerY)
            show_score(textX,textY)
            
            pygame.display.update()
            
        elif game_state == 'over':
            over_text  = over_font.render('VRAXXED !!!!!!!',True,(255,255,255))
            screen.blit(over_text,(200,250))
            if retry_button.draw():
                game_state = 'play'
                print("oops")
                    


            





    

        

gameloop()

    

