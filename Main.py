# Simple pygame program
# Check documentation - https://realpython.com/pygame-a-primer/

# Import and initialize the pygame library
import pygame

# Import random for random numbers
import random
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
)

Square_Size = 75

# Define constants for the screen width and height
Multiplier = 10
SCREEN_WIDTH = Square_Size*Multiplier 
SCREEN_HEIGHT = Square_Size*Multiplier 


all_sprites = pygame.sprite.Group()

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((Square_Size, Square_Size))
        self.surf.fill((0, 0, 255))
        self.rect =   pygame.Rect(Square_Size*2, Square_Size*2, Square_Size, Square_Size)

        self.Center = []
        self.CenterOutcome = []
        #self.detectCenter()

        self.Surround=[]
        #self.detectSurround()

        self.RL = RL.TraditionalRL()
        self.RL._init_()

# Move the sprite based on user keypresses
    def update(self):

        self.detectCenter()
        
    
        previousStateidx, actionidx, action = self.RL.makeAction(self)
        self.rect.move_ip(action['x']*Square_Size, action['y']*Square_Size)

        self.detectCenter()

        if self.Center == 'collision':     
                self.rect.move_ip(action['x']*-1*Square_Size, action['y']*-1*Square_Size)
        
        self.RL.updateExpectation(previousStateidx,actionidx, self.CenterOutcome)
    
        self.detectCenter()
        self.detectSurround()

        
    def detectCenter(self):

        type = []
        type = pygame.sprite.spritecollide(self, all_sprites,False)
        self.Center = type[0].type
        self.CenterOutcome = type[0].outcome

    def detectSurround(self):

        Location = copy.copy(self.rect)
        self.Surround = []
        for loc in range(0,7):
            Location.move_ip(math.sin(math.radians(loc*45))*Square_Size,math.cos(math.radians(loc*45))*Square_Size)
            for sprite in all_sprites:
                if Location.colliderect(sprite.rect):
                        self.Surround.append(sprite.type) 
            

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


while running:

    # Did the user click the window close button?
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False


    # Update the player sprite 
    player.update()

    # Draw all sprites
    for entity in all_sprites:
     screen.blit(entity.surf, entity.rect)

    screen.blit(player.surf, player.rect)
    # Flip the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# Done! Time to quit.
pygame.quit()


