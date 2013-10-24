import pygame
import sys
import math
import random
from pygame.locals import *
#import numpy

import building as b

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

# REGION OF INTEREST : OMEGA in R^2
# OMEGA is connected to outside world through points PHI, at the edges of OMEGA
# functions over OMEGA: h(p), w(p) and v(p) for p in OMEGA
# respectively elevation, water height and vegetation density for a point p

# Village type V
# Growth scenario sets V over time, launches settlement seeds B_i (future location buildings)
# Roads R_j that serve them.
# Village Skeleton S = ({B_i}, {R_j})
# Settlement seed B_i = (BETA, p), BETA is building type (church, farm etc) and p position in OMEGA
# Road R_j is a set of nodes, positions {p_k} controlling its central curve.

# the building encyclopaedia stores all buildings and their parameters.
# it is a function of (V,BETA) returning the set of parameters for building BETA under V
# OMEGA can be divided in parcels P_i, footprint of building F_i

# Environment maps, one for each function on OMEGA
# User defined growth scenario: sequences of creating n buildings of type BETA followed by road creation
# During execution, creation of a new building seed is immediately followed by its connection to the road network
# Input is environment maps, growth scenario and OMEGA
# Grow village skeleton S, generate land parcels P_i, draw

PHI = [(0, 400), (1000,400)]
V = "FARMING"
growth_scenario = [(1,"First settler"),(5, "House"),(20, "House")] # ?

CENTERPOINT = (WINDOWWIDTH//2, WINDOWHEIGHT//2)
B = [] # buildings
R = [[PHI[0], PHI[1]]] # roads

# a general instance of a function representing interest criteria for the interest function
# Each f_i(B) returns output in [-1, 1] (so squash!)
def centerfocus(p, building_type):
    distance_to_corner = (euclidian_distance2D(CENTERPOINT, (0,0))//2)
    x =  distance_to_corner - euclidian_distance2D(p, CENTERPOINT)
    return x / distance_to_corner

# Two-part Gaussian function
def sociability(p1, beta1):
    s = 0
    for p2, beta2 in B:
        distance = euclidian_distance2D(p2, p1)
        (lmin, l0, lmax) = b.Sociability[(min(beta1, beta2), max(beta1, beta2))]
        score = two_part_gaussian(distance, lmin, l0, lmax)
        if score == -1:
            return -1
        s += score
    if B:
        s = (s / float(len(B)))
    return s

def two_part_gaussian(x, lmin, l0, lmax):
    mu = l0
    if x < lmin:
        return -1
    elif x <= l0:
        sigma = (mu - lmin) / 3.0
        return math.exp( (-1 * (x - mu)**2)/(2* sigma**2))
    else: # l0 < x:
        tau = (lmax - mu) / 3.0
        return math.exp( (-1 * (x - mu)**2)/(2* tau**2))

def euclidian_distance2D((p1, p2), (q1, q2)):
    return math.sqrt((q1 - p1)**2 + (q2 - p2)**2)

# Main identity function (input is building seed B_i: (BETA,p) )
def identity(building_type, p):
    s = 0
    for f,w in b.Building_encyclopaedia[building_type].functions:
        x = eval(f)(p, building_type)
        if x == -1:
            return 0
        else:
            s += w*x
    return max(0, s)

def seed(beta):
    p = None
    success = False
    # until a random p is successfully selected:
    while not success:
        # select a random p
        p = (random.randrange(WINDOWWIDTH), random.randrange(WINDOWHEIGHT))

        # check conditions for constructing beta at p

        # compute I(beta) and perform random choice (aggregation test)
        aggregation = 0.3 # ARBITRARY
        if identity(beta, p) > aggregation:
            success = True

    return p

def connect_roads(p):
    return None # TODO

def main():

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Game')

    mousex = 0
    mousey = 0

    while True:

        mouseClicked = False
        nextScenario = False
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
            # Next part of Growth Scenario by pressing Enter
            elif event.type == KEYUP and event.key == K_RETURN:
                nextScenario = True
                ## DEBUG ##
                #p = seed("House")
                #B.append((p,"House"))
                #connect_roads(p)
                ###########

        ### CONTENT ###

        if nextScenario and growth_scenario:
            (n, BETA) = growth_scenario.pop(0)
            for i in range(n):
                p = seed(BETA)
                B.append((p,BETA))
                connect_roads(p)

        ### DRAW ALL ##

        for (p,BETA) in B:
            pygame.draw.circle(DISPLAYSURF, BLUE, p, 5)

        for nodes in R:
            pygame.draw.lines(DISPLAYSURF, BLACK, False, nodes) 

        ###############

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()