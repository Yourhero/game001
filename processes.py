import pygame, sys, classes
from random import randint

def process(player,FPS, total_frames, SCREENWIDTH, SCREENHEIGHT):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                classes.PlayerProjectile.fire = not classes.PlayerProjectile.fire
            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        classes.Player.right_face = True
        player.vel_x = 8
    elif keys[pygame.K_a]:
        classes.Player.right_face = False
        player.vel_x = -8
    else:
        player.vel_x = 0
        
    if keys[pygame.K_w]:
        player.jumping = True
        
    if keys[pygame.K_SPACE]:
        
        def direction():
            if player.right_face:
                p.vel_x = 15
            else:
                p.image = pygame.transform.flip(p.image, True, False)
                p.vel_x = -15
                
        if classes.PlayerProjectile.fire:
            p = classes.PlayerProjectile(player.rect.x, player.rect.y, "laser_red.png")
            direction()
        else:
            p = classes.PlayerProjectile(player.rect.x, player.rect.y, "laser_blue.png")
            direction()
            
    spawn(FPS, total_frames, SCREENWIDTH, SCREENHEIGHT)
    collisions()
        
def spawn(FPS, total_frames, SCREENWIDTH, SCREENHEIGHT):
    four_seconds = FPS * 1
    if total_frames % four_seconds == 0:
        r = randint(1,2)
        x = 1
        if r == 2:
            x = SCREENWIDTH - 22
        Enemy = classes.NPC(x, randint(0,SCREENHEIGHT), "ufok.png")
    
def collisions():
    
    for npc in classes.NPC.List:
        hits = pygame.sprite.spritecollide(npc, classes.PlayerProjectile.List,True)
        if len(hits) > 0:
            for hit in hits:
                if classes.PlayerProjectile.fire == True:
                    npc.health -= npc.half_health
                else:
                    npc.vel_x = 0
                hit.destroy()