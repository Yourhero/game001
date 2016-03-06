import pygame, sys
from classes import *
from processes import *

pygame.init()

SCREENWIDTH, SCREENHEIGHT = 1280,720
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
img_player = pygame.image.load("Dome2.png")
background = pygame.image.load("space-stars-background.jpg")
clock = pygame.time.Clock()
FPS = 30
totalframes = 0

player = Player(0, SCREENHEIGHT - 50, "Dome2.png")


while True:
    process(player, FPS, totalframes, SCREENWIDTH, SCREENHEIGHT)
    player.motion(SCREENWIDTH, SCREENHEIGHT)
    NPC.update_all(SCREENWIDTH, SCREENHEIGHT)
    PlayerProjectile.movement(SCREENWIDTH, SCREENHEIGHT)
    screen.blit(background, (0,0))
    BaseClass.allsprites.draw(screen)
    PlayerProjectile.List.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
    totalframes += 1