import pygame, math
from random import randint

class BaseClass(pygame.sprite.Sprite):
  
    allsprites = pygame.sprite.Group()
  
    def __init__(self, x, y, image_string):
        pygame.sprite.Sprite.__init__(self)
        BaseClass.allsprites.add(self)  
        self.image  = pygame.image.load(image_string)
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def destroy(self, ClassName):
        ClassName.List.remove(self)
        BaseClass.allsprites.remove(self)
        del self

class Player(BaseClass):
    List = pygame.sprite.Group()
    right_face = True
    def __init__(self, x, y, image_string):
        BaseClass.__init__(self, x, y, image_string)
        Player.List.add(self)
        self.vel_x = 0
        self.vel_y = 15
        self.jumping, self.falling = False, False

    def motion(self, SCREENWIDTH, SCREENHEIGHT, vel_x=None, vel_y=None):
            
        predicted_x = self.rect.x + self.vel_x
        predicted_y = self.rect.y + self.vel_y
        
        if predicted_x < 0:
          self.vel_x = 0
        elif predicted_x + self.rect.width > SCREENWIDTH:
          self.vel_x = 0
        
        if vel_x is not None:
            self.rect.x += vel_x 
        elif vel_y is not None:
            self.rect.y += vel_y 
        else:
            self.rect.x += self.vel_x 
        
        self.__jump(SCREENHEIGHT)

    def __jump(self, SCREENHEIGHT):
        max_jump = 100
    
        if self.jumping:
            if self.rect.y < max_jump:
                self.falling = True
            if self.falling:
                self.rect.y += self.vel_y
                predicted_y = self.rect.y + self.vel_y
                if predicted_y + self.rect.height > SCREENHEIGHT - self.rect.height:
                    self.jumping, self.falling = False, False
            else:
                self.rect.y -= self.vel_y
                
class NPC(BaseClass):
    List = pygame.sprite.Group()
    def __init__(self, x, y, image_string):
        BaseClass.__init__(self, x, y, image_string)
        NPC.List.add(self)
        self.health = 100
        self.half_health = self.health /2.0
        self.vel_x = randint(1,9)
        self.offset = randint(140,400)
        self.amplitude, self.period = randint(20,140), randint(4,5) / 100.0
        
    def motion(self, SCREENWIDTH, SCREENHEIGHT):    
        if self.rect.x + self.rect.width > SCREENWIDTH or self.rect.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.vel_x = -self.vel_x
        self.rect.x += self.vel_x
        self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + self.offset
        
    @staticmethod        
    def update_all(SCREENWIDTH, SCREENHEIGHT):
        for npc in NPC.List:
            npc.motion(SCREENWIDTH,SCREENHEIGHT)
            if npc.health <=0:
                npc.destroy(NPC)
            
class PlayerProjectile(pygame.sprite.Sprite):
    List = pygame.sprite.Group()
    normal_list = []
    fire = True
    
    def __init__(self, x, y, image_string):
        pygame.sprite.Sprite.__init__(self)
        self.image  = pygame.image.load(image_string)
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        if len(PlayerProjectile.normal_list) > 0:
            last_element = PlayerProjectile.normal_list[-1]
            difference = abs((self.rect.x - last_element.rect.x))
            if difference < self.rect.width:
                return
        PlayerProjectile.normal_list.append(self)
        PlayerProjectile.List.add(self)
        self.vel_x = None
    
    @staticmethod    
    def movement(SCREENWIDTH, SCREENHEIGHT):
        for projectile in PlayerProjectile.List:
            projectile.rect.x += projectile.vel_x
    
    def destroy(self):
        PlayerProjectile.normal_list.remove(self)
        del self
        