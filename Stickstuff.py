import pygame, sys, random, os
from pygame.locals import *

# --- Variables needed in classes ---
frameTime = 0

resizer = 4

# --- Classes and functions ---

def distance(speed, time):
    distance = time * speed
    return distance

class Stickman(object):
    def __init__(self, position, head, hand):
        self.position = position
        self.head = head
        self.hand = hand
        self.stickmanRect = pygame.Rect(self.position[0], self.position[1], 16 * resizer, 32 * resizer)
        self.destination = [random.randint(0, 1200 - (16 * resizer)), random.randint(0, 700 - (32 * resizer))]
        self.reached = [False, False]
        self.lastMoveTime = pygame.time.get_ticks()
        self.waitTime = random.randint(3000, 20000)
    def render(self):
        self.stickmanRect = pygame.Rect(self.position[0], self.position[1], 16 * resizer, 32 * resizer)
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
            self.destination = [random.randint(0, 1200 - (16 * resizer)), random.randint(0, 700 - (32 * resizer))]
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
        if pygame.time.get_ticks() - self.lastFrameTime >= 40:
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

WINDOWWIDTH = 1200
WINDOWHEIGHT = 700

# --- Set up ---
pygame.init()

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32) #always 0 and 32
pygame.display.set_caption('Stickstuff')
basicFont = pygame.font.SysFont(None, 23)
mainClock = pygame.time.Clock()

# --- Other variables
showDebug = True

stickList = []
animationList = []
explosion = []
hatList = []
handList = []

lastDelete = pygame.time.get_ticks()
lastExplosion = pygame.time.get_ticks()
# --- Image loading ---
baseImg = pygame.transform.scale(pygame.image.load('baseman.png'), (16 * resizer, 32 * resizer))

path = os.path.abspath("")
for picture in os.listdir(path):
    if picture.endswith(".hat.png"):
        hatList.append(pygame.transform.scale(pygame.image.load(picture), (16 * resizer, 32 * resizer)))
        print "Loaded Hat: " + picture
    elif picture.endswith(".hand.png"):
        handList.append(pygame.transform.scale(pygame.image.load(picture), (16 * resizer, 32 * resizer)))
        print "Loaded Hand: " + picture

for i in range(0, 9):
    explosion.append(pygame.transform.scale(pygame.image.load('explosion' + str(i) + '.png'), (int(21 * resizer / 1.3), int(21 * resizer / 1.3))))
    print "Loaded explosion frame " + str(i)

    
bg = pygame.image.load('bg.png')



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
        debug = ""
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    if pygame.key.get_pressed()[127] == True and pygame.time.get_ticks() - lastDelete >= 100:
        try:
            animationList.append(Explosion([stickList[len(stickList) - 1].position[0] + 8, stickList[len(stickList) - 1].position[1] + 16]))
            del stickList[len(stickList) - 1]
        except IndexError:
            print "List empty"
        lastDelete = pygame.time.get_ticks()
        
    if pygame.mouse.get_pressed()[2] == True and pygame.time.get_ticks() - lastExplosion >= 30:
        animationList.append(Explosion([mousePosition[0] - (21 * resizer / 2), mousePosition[1] - (21 * resizer / 2)]))
        for stick in stickList:
            if mousePosition[0] > stick.stickmanRect.left and mousePosition[0] < stick.stickmanRect.right and mousePosition[1] > stick.stickmanRect.top and mousePosition[1] < stick.stickmanRect.bottom:
                stickList.remove(stick)
        lastExplosion = pygame.time.get_ticks()


    pygame.display.update()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                stickList.append(Stickman([mousePosition[0] - 7 * resizer, mousePosition[1] - 12 * resizer], hatList[random.randint(0, len(hatList) - 1)], handList[random.randint(0, len(handList) - 1)]))
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

