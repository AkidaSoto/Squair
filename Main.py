# Simple pygame program
# Check documentation - https://realpython.com/pygame-a-primer/

# Import and initialize the pygame library
from distutils.log import error
#from operator import truediv
import pygame

# Import random for random numbers
import math 
import copy

# Import RL stuff
import RL

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEWHEEL
)

Square_Size = 75

# Define constants for the screen width and height
Multiplier = 10
SCREEN_WIDTH = Square_Size*Multiplier 
SCREEN_HEIGHT = Square_Size*Multiplier 


all_sprites = pygame.sprite.Group()


class RectSprite(pygame.sprite.Sprite):
    def __init__(self, color, x, y, w, h,o):
        super().__init__() 
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, w, h)
        self.value = o

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((Square_Size, Square_Size))
        self.surf.fill((0, 0, 255))
        self.rect =   pygame.Rect(Square_Size*2, Square_Size*2, Square_Size, Square_Size)

        self.Center = []
        #self.detectCenter()

        self.Surround=[]
        #self.detectSurround()

        self.RL = RL.TraditionalRL()
        self.RL._init_()

# Move the sprite based on user keypresses
    def update(self):

        #Where is it?
        self.detectCenter()
        self.detectSurround()
    
        #Make a movement
        previousStateidx, actiontype, action = self.RL.makeAction(self)
        self.rect.move_ip(action['x']*Square_Size, action['y']*Square_Size)

        #Where is it now?
        self.detectCenter()

        #What are the consequences?
        if self.Center.type == 'collision':     
                self.rect.move_ip(action['x']*-1*Square_Size, action['y']*-1*Square_Size)
        elif self.Center.type == 'reward': 
            reward = pygame.sprite.spritecollide(self, all_sprites,False)
            reward[0].type = 'none'
            reward[0].surf.fill((255,255,255))
        
        #Update expectation
        self.RL.updateExpectation(previousStateidx,actiontype, self.Center.outcome)
        
        # Consequences may have change it's position
        self.detectCenter()
        self.detectSurround()

        
    def detectCenter(self):
        
         for sprite in all_sprites:
                if self.rect.colliderect(sprite.rect):
                    self.Center = sprite
        
        

    def detectSurround(self):

        
        self.Surround = []
        for loc in range(0,8):
            Location = copy.copy(self.rect)
            Location.move_ip(round(math.sin(math.radians(loc*45)))*Square_Size,round(math.cos(math.radians(loc*45)))*Square_Size)
            ident = False
            for sprite in all_sprites:
                if Location.colliderect(sprite.rect):
                        self.Surround.append(sprite) 
                        ident = True
            if ident == False:
                    error('No Neighbors were identified?')
            

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Object(pygame.sprite.Sprite):
    def __init__(self):
        super(Object, self).__init__()
        self.surf = pygame.Surface((Square_Size, Square_Size))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        self.type = None

# Create a map with boundaries
def drawGrid():
    for x in range(0, SCREEN_WIDTH, Square_Size):
        for y in range(0, SCREEN_HEIGHT, Square_Size):
            rect = pygame.Rect(x, y, Square_Size, Square_Size)

            new_object = Object()
            new_object.rect = pygame.Rect(x, y, Square_Size, Square_Size)
            
            if x == 0 or y == 0 or x == SCREEN_WIDTH-Square_Size or y == SCREEN_WIDTH-Square_Size:
               new_object.surf.fill((0,0,0))
               new_object.type = 'collision'
               new_object.outcome = -1
               
            else:
               new_object.surf.fill((255,255,255))
               new_object.type = 'none'
               new_object.outcome = 0
            
            all_sprites.add(new_object)

mouse = RectSprite((0, 0, 0), Square_Size, Square_Size, Square_Size, Square_Size, 1)
color = [(0,0,0), (255, 0, 0), (0,255,0),(0,0,255), (255,255,0), (255,0,255),(0,255,255), (255,255,255)]
value = [1,1,1,1,1,1,1,1]
coloridx = 0
convert = False

def Converter():
    replacer = pygame.sprite.spritecollide(mouse, all_sprites,False)
    replacer[0].surf.fill(mouse.image.unmap_rgb(mouse.image.get_at_mapped((1,1))))
    replacer[0].outcome = mouse.value
    replacer[0].type = 'reward'   


foodbar = RectSprite((255, 0, 0), Square_Size*9.5, Square_Size*8, Square_Size/4, Square_Size, 0)
foodbar.value = 1

def changeFood(value):
    value = round(sorted((0, foodbar.rect[3]+(value*Square_Size),Square_Size))[1])
    foodbar.rect.update((Square_Size*9.5, Square_Size*8, Square_Size/4, value))
    foodbar.image = pygame.transform.scale(foodbar.image,(Square_Size/4, value))


pygame.init()

# Instantiate player. Right now, this is just a rectangle.
player = Player()
#all_sprites.add(player)
drawGrid()


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Run until the user asks to quit
running = True
# Setup the clock for a decent framerate
clock = pygame.time.Clock()
ticker = 1
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
                
        elif event.type == MOUSEWHEEL:
            coloridx += event.y
            coloridx = coloridx % len(color)
            mouse.image.fill(color[coloridx])
            mouse.value = value[coloridx]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            convert = True
        elif event.type == pygame.MOUSEBUTTONUP:
            convert = False
            
        elif event.type == QUIT:
            running = False


    # Update the player sprite 
    ticker += 1
    
    if ticker == 20:
        changeFood(-.01)
        player.update()
        ticker = 1
        
    mousepos = pygame.mouse.get_pos()
    mousepos = (round((mousepos[0]-(.5*Square_Size))/Square_Size)*Square_Size, round((mousepos[1]-(.5*Square_Size))/Square_Size)*Square_Size)
    mouse.rect = pygame.Rect(mousepos[0], mousepos[1],Square_Size, Square_Size)

    # Draw all sprites
    
    if convert:
        Converter()
    
    for entity in all_sprites:
     screen.blit(entity.surf, entity.rect)
    screen.blit(mouse.image, mouse.rect)
    screen.blit(foodbar.image, foodbar.rect)
    screen.blit(player.surf, player.rect)
    

    
    # Flip the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# Done! Time to quit.
pygame.quit()


