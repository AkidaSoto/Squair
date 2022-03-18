# Simple pygame program
# Check documentation - https://realpython.com/pygame-a-primer/

# Import and initialize the pygame library
import pygame

# Import random for random numbers
import random

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

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((Square_Size, Square_Size))
        self.surf.fill((0, 0, 255))
        self.rect =   pygame.Rect(Square_Size, Square_Size, Square_Size, Square_Size)

# Move the sprite based on user keypresses
    def update(self, pressed_keys):


        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -Square_Size)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, Square_Size)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-Square_Size, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(Square_Size, 0)

        if pygame.sprite.spritecollideany(player, collisions):     
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, Square_Size)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, -Square_Size)
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(Square_Size, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(-Square_Size, 0)


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Collision(pygame.sprite.Sprite):
    def __init__(self):
        super(Collision, self).__init__()
        self.surf = pygame.Surface((Square_Size, Square_Size))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()

pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
collisions = pygame.sprite.Group()
walkable = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Run until the user asks to quit
running = True

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create a map with boundaries

def drawGrid():
    for x in range(0, SCREEN_WIDTH, Square_Size):
        for y in range(0, SCREEN_HEIGHT, Square_Size):
            rect = pygame.Rect(x, y, Square_Size, Square_Size)

            new_collision = Collision()
            new_collision.rect = pygame.Rect(x, y, Square_Size, Square_Size)
            
            if x == 0 or y == 0 or x == SCREEN_WIDTH-Square_Size or y == SCREEN_WIDTH-Square_Size:
               new_collision.surf.fill((0,0,0))

               collisions.add(new_collision)
            else:
               new_collision.surf.fill((255,255,255))
               walkable.add(new_collision)
            
            all_sprites.add(new_collision)
                
drawGrid()
all_sprites.add(player)

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses    

    player.update(pressed_keys)
   # Update enemy position
    #enemies.update()

    # Draw a solid blue circle in the center
    #pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(30, 30, 60, 60))

    # Draw all sprites
    for entity in all_sprites:
     screen.blit(entity.surf, entity.rect)


    # Flip the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# Done! Time to quit.
pygame.quit()