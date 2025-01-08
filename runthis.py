import pygame 
import math
import random
from pygame import mixer

pygame.init()

#creating screen 
screen = pygame.display.set_mode((800 , 600))
pygame.display.set_caption("lord vraxx shooter")

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

over_font = pygame.font.Font('freesansbold.ttf',64)


#defining

def show_score(x,y):
    score = font.render('score :' + str(score_value),True, (255,255,255))
    screen.blit(score , (x,y))

def game_over():
    over_text  = over_font.render('VRAXXED !!!!!!!',True,(255,255,255))
    screen.blit(over_text,(200,250))
    


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



#game loop


running = True 
while running:

    

    # rgb background

    screen.fill((2,0,0))
    screen.blit(bg,(0,0))


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

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



    

