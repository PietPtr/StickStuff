import pygame, sys, random
from pygame.locals import *

# --- Variables needed in classes ---
frameTime = 0

# --- Classes and functions ---

def distance(speed, time):
    distance = time * speed
    return distance

class Stickman(object):
    def __init__(self, position, head, hand):
        self.position = position
        self.head = head
        self.hand = hand
        self.destination = [random.randint(0, 1200), random.randint(0, 700)]
        self.reached = [False, False]
    def render(self):
        windowSurface.blit(baseImg, (self.position[0], self.position[1]))
        windowSurface.blit(self.head, (self.position[0], self.position[1]))
        windowSurface.blit(self.hand, (self.position[0], self.position[1]))
    def move(self):
        if int(self.position[0]) - int(self.destination[0]) > 0 and self.reached[0] == False:
            self.position[0] = self.position[0] - distance(0.1, frameTime)
        elif int(self.position[0]) - int(self.destination[0]) < 0 and self.reached[0] == False:
            self.position[0] = self.position[0] + distance(0.1, frameTime)
        elif int(self.position[0]) == int(self.destination[0]):
            self.position[0] = self.destination[0]
            self.reached[0] = True
        
        if int(self.position[1]) - int(self.destination[1]) > 0 and self.reached[0] == False:
            self.position[1] = self.position[1] - distance(0.1, frameTime)
        elif int(self.position[1]) - int(self.destination[1]) < 0 and self.reached[0] == False:
            self.position[1] = self.position[1] + distance(0.1, frameTime)
        elif int(self.position[1]) == int(self.destination[1]):
            self.position[1] = self.destination[1]
            self.reached[1] = True

        if self.reached == [True, True]:
            self.destination = [random.randint(0, 1200), random.randint(0, 700)]
            self.reached = [False, False]
        
# --- Constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

RESIZER = 4

WINDOWWIDTH = 1200
WINDOWHEIGHT = 700

# --- Set up ---
pygame.init()

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32) #always 0 and 32
pygame.display.set_caption('Stickstuff')
basicFont = pygame.font.SysFont(None, 23)
mainClock = pygame.time.Clock()

# --- Image loading ---
baseImg = pygame.transform.scale(pygame.image.load('baseman.png'), (16 * RESIZER, 32 * RESIZER))
emptyImg = pygame.transform.scale(pygame.image.load('empty.png'), (16 * RESIZER, 32 * RESIZER))

hatList =  [pygame.transform.scale(pygame.image.load('empty.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('cap.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('beard.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('beardGray.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('monocle.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('cowboy.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('hat.png'), (16 * RESIZER, 32 * RESIZER)),]

handList = [pygame.transform.scale(pygame.image.load('empty.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('stick.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('spear.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('beer.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('pokeball.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('hammer.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('pickaxe.png'), (16 * RESIZER, 32 * RESIZER)),
            pygame.transform.scale(pygame.image.load('sword.png'), (16 * RESIZER, 32 * RESIZER))]

bg = pygame.image.load('bg.png')

# --- Other variables
showDebug = True

stickList = [Stickman([100 - 7 * RESIZER, 100 - 12 * RESIZER], hatList[random.randint(0, len(hatList) - 1)], handList[random.randint(0, len(handList) - 1)])]

while True:
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()

    windowSurface.blit(bg, (0, 0))
    
    for stick in stickList:
        stick.render()
        stick.move()
    
    if showDebug == True:
        debug = stickList[0].reached
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                stickList.append(Stickman([mousePosition[0] - 7 * RESIZER, mousePosition[1] - 12 * RESIZER], hatList[random.randint(0, len(hatList) - 1)], handList[random.randint(0, len(handList) - 1)]))
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

