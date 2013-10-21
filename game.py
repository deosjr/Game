import pygame, sys
from pygame.locals import *

WINDOWWIDTH = 1000
WINDOWHEIGHT = 800
FPS = 30

WHITE = (255, 255, 255) 
GREEN = ( 0, 255, 0) 
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0) 
RED = (255, 0, 0) 
BLACK = (0, 0, 0)

BGCOLOR = WHITE

def main():

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Game')

    mousex = 0
    mousey = 0

    while True:

        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        ### CONTENT ###

        pygame.draw.line(DISPLAYSURF, BLACK, (0, 400), (1000,400)) 

        ###############

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()