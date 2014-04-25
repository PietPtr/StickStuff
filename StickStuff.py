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
        self.stickmanRect = pygame.Rect(self.position[0], self.position[1], 16 * RESIZER, 32 * RESIZER)
        self.destination = [random.randint(0, 1200 - (16 * RESIZER)), random.randint(0, 700 - (32 * RESIZER))]
        self.reached = [False, False]
        self.lastMoveTime = pygame.time.get_ticks()
        self.waitTime = random.randint(3000, 20000)
    def render(self):
        self.stickmanRect = pygame.Rect(self.position[0], self.position[1], 16 * RESIZER, 32 * RESIZER)
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
        
        if int(self.position[1]) - int(self.destination[1]) > 0 and self.reached[1] == False:
            self.position[1] = self.position[1] - distance(0.1, frameTime)
        elif int(self.position[1]) - int(self.destination[1]) < 0 and self.reached[1] == False:
            self.position[1] = self.position[1] + distance(0.1, frameTime)
        elif int(self.position[1]) == int(self.destination[1]):
            self.position[1] = self.destination[1]
            self.reached[1] = True

        if self.reached == [True, True] and pygame.time.get_ticks() - self.lastMoveTime >= self.waitTime:
            self.destination = [random.randint(0, 1200 - (16 * RESIZER)), random.randint(0, 700 - (32 * RESIZER))]
            self.reached = [False, False]
            self.lastMoveTime = pygame.time.get_ticks()
            self.waitTime = random.randint(3000, 20000)

class Explosion(object):
    def __init__(self, position):
        self.position = position
        self.frame = 0
        self.lastFrameTime = pygame.time.get_ticks()
    def doTasks(self):
        try:
            windowSurface.blit(explosion[self.frame], (self.position[0], self.position[1]))
        except IndexError:
            return False
        print pygame.time.get_ticks() - self.lastFrameTime
        if pygame.time.get_ticks() - self.lastFrameTime >= 30:
            self.frame = self.frame + 1
            self.lastFrameTime = pygame.time.get_ticks()
        return True
      
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

explosion = [pygame.transform.scale(pygame.image.load('explosion0.png'), (int(21 * RESIZER / 1.3), int(21 * RESIZER / 1.3))),
             pygame.transform.scale(pygame.image.load('explosion1.png'), (int(21 * RESIZER / 1.3), int(21 * RESIZER / 1.3))),
             pygame.transform.scale(pygame.image.load('explosion2.png'), (int(21 * RESIZER / 1.3), int(21 * RESIZER / 1.3))),
             pygame.transform.scale(pygame.image.load('explosion3.png'), (int(21 * RESIZER / 1.3), int(21 * RESIZER / 1.3))),
             pygame.transform.scale(pygame.image.load('explosion4.png'), (int(21 * RESIZER / 1.3), int(21 * RESIZER / 1.3))),
             pygame.transform.scale(pygame.image.load('explosion5.png'), (int(21 * RESIZER / 1.3), int(21 * RESIZER / 1.3))),
             pygame.transform.scale(pygame.image.load('explosion6.png'), (int(21 * RESIZER / 1.3), int(21 * RESIZER / 1.3))),
             pygame.transform.scale(pygame.image.load('explosion7.png'), (int(21 * RESIZER / 1.3), int(21 * RESIZER / 1.3))),
             pygame.transform.scale(pygame.image.load('explosion8.png'), (int(21 * RESIZER / 1.3), int(21 * RESIZER / 1.3)))]
             

bg = pygame.image.load('bg.png')

# --- Other variables
showDebug = True

stickList = [Stickman([100 - 7 * RESIZER, 100 - 12 * RESIZER], hatList[random.randint(0, len(hatList) - 1)], handList[random.randint(0, len(handList) - 1)])]

animationList = []

while True:
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()

    windowSurface.blit(bg, (0, 0))
    
    for stick in stickList:
        stick.render()
        stick.move()

    for animation in animationList:
        if animation.doTasks() == False:
            animationList.remove(animation)
    
    if showDebug == True:
        debug = "Placeholder"
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                stickList.append(Stickman([mousePosition[0] - 7 * RESIZER, mousePosition[1] - 12 * RESIZER], hatList[random.randint(0, len(hatList) - 1)], handList[random.randint(0, len(handList) - 1)]))
            if event.button == 3:
                animationList.append(Explosion([mousePosition[0] - (21 * RESIZER / 2), mousePosition[1] - (21 * RESIZER / 2)]))
                for stick in stickList:
                    if mousePosition[0] > stick.stickmanRect.left and mousePosition[0] < stick.stickmanRect.right and mousePosition[1] > stick.stickmanRect.top and mousePosition[1] < stick.stickmanRect.bottom:
                        stickList.remove(stick)
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

