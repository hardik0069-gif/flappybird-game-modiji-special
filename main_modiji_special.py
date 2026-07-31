import sys
import random
import pygame
from pygame.locals import *


FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
PIPE_INTERVAL = 180
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'assets/sprites2/bird.png'
BACKGROUND = 'assets/sprites2/background.png'
PIPE = 'assets/sprites2/pipe.png'

def welcomescreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENHEIGHT - GAME_SPRITES['message'].get_height()) / 2)
    messagey  = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        SCREEN.blit(GAME_SPRITES['message'], (0, 0))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

                    
    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()


    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[0]['y'] },
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newpipe2[0]['y'] }
    ]

    lowerPipes = [
    {'x': SCREENWIDTH + 200, 'y': newpipe1[1]['y']},
    {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newpipe2[1]['y']},
    ]

    pipeVelx = -4.5

    playerVely = -9
    playerMaxVely = 10
    playerMinVely = -8
    playerAccy = 1

    playerFlapAccv = -8 
    playerFlapped = False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                        playerVely = playerFlapAccv
                        playerFlapped = True
                        GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        
        if crashTest:
            return score
                                        
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos  + 4:
                score += 1
                print(f"Yscore is {score}")
                GAME_SOUNDS['point'].play()


        if playerVely <playerMaxVely and not playerFlapped:
            playerVely += playerAccy

        if playerFlapped:
           playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)

        
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx

        
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

       
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width())):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and \
           abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def gameover(score):
    font = pygame.font.SysFont('Arial', 32, bold=True)
    smallFont = pygame.font.SysFont('Arial', 22)

    gameOverText = font.render('GAME OVER', True, (255, 255, 255))
    scoreText = smallFont.render(f'Score : {score}', True, (255, 255, 255))
    hintText = smallFont.render('Press SPACE to continue', True, (255, 255, 255))

    overlay = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
    overlay.set_alpha(160)
    overlay.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(overlay, (0, 0))

        SCREEN.blit(gameOverText, (SCREENWIDTH/2 - gameOverText.get_width()/2, SCREENHEIGHT/2 - 60))
        SCREEN.blit(scoreText, (SCREENWIDTH/2 - scoreText.get_width()/2, SCREENHEIGHT/2))
        SCREEN.blit(hintText, (SCREENWIDTH/2 - hintText.get_width()/2, SCREENHEIGHT/2 + 40))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getRandomPipe():
    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3.7
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    pipe = [
        { 'x' : pipex, 'y': -y1},
        { 'x' : pipex, 'y': y2}
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
        
        pygame.image.load('assets/sprites2/0.png').convert_alpha(),
        pygame.image.load('assets/sprites2/1.png').convert_alpha(),
        pygame.image.load('assets/sprites2/2.png').convert_alpha(),
        pygame.image.load('assets/sprites2/3.png').convert_alpha(),
        pygame.image.load('assets/sprites2/4.png').convert_alpha(),
        pygame.image.load('assets/sprites2/5.png').convert_alpha(),
        pygame.image.load('assets/sprites2/6.png').convert_alpha(),
        pygame.image.load('assets/sprites2/7.png').convert_alpha(),
        pygame.image.load('assets/sprites2/8.png').convert_alpha(),
        pygame.image.load('assets/sprites2/9.png').convert_alpha()
    )

    GAME_SPRITES['message'] = pygame.image.load('assets/sprites2/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('assets/sprites2/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load('assets/sprites2/pipe.png').convert_alpha(), 180),
        pygame.image.load('assets/sprites2/pipe.png').convert_alpha()
    )
    GAME_SOUNDS['die'] = pygame.mixer.Sound('assets/audio2/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('assets/audio2/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('assets/audio2/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio2/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('assets/audio2/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomescreen()
        score =maingame()
        gameover(score)