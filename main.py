import pygame, math
#set clock
clock = pygame.time.Clock()

#define game variables
FULLSCREEN = False
screen_width = 800
screen_height = 800
gravity = 1
floor= screen_height - 200
FPS = 60
dt = clock.tick(FPS)/25
#set screen
screen = pygame.display.set_mode((screen_width,screen_height), )


#load images

#define functions

#define classes
class point():
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.width = 10
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.width)
    def update(self):
        pos = pygame.mouse.get_pos()
        mouse = pygame.rect.Rect(pos[0], pos[1], 10 ,10)
        if pygame.mouse.get_pressed()[0] == 1:
                
                self.y = pos[1]
                self.x = pos[0]
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), self.width, 10)

class One(pygame.sprite.Sprite):
    def __init__(self, centerx, centery):
        pygame.sprite.Sprite.__init__(self)
        self.width = 40
        self.height = 40
        self.x = centerx - self.width/2
        self.y = centery - self.height/2
        self.centerx = centerx
        self.centery = centery
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load('square_one.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
    
    def update(self):
        dx = 0
        dy = 0

        #gravity
        point = (p.x, p.y)
        disx = self.centerx - point[0]
        disy = self.centery - point[1]

        if not disx == 0:
            ang = math.atan(disy/disx)
            dy = math.sin(ang)
            dx = math.cos(ang)
            
        if self.centerx> p.x:
            dx *= -1
            dy *= -1

        #collision
        for square in square_group:
            if not square == self:
                drect = pygame.rect.Rect(self.x +dx, self.y+ dy, self.width, self.height)
                if pygame.Rect.colliderect(drect, square.rect):
                    dx = 0
                    dy = 0
        
        self.x += dx
        self.y += dy
        self.centerx = self.x + self.width/2
        self.centery = self.y + self.height/2
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.image, self.rect)

square_group = pygame.sprite.Group()
p= point(screen_width/2, screen_height/2)

#main game loop
run = True
while run:
    clock.tick(FPS)
    #screen.blit((0,0),bg_img)
    screen.fill((250,250,250))

    
    #update squares
    square_group.update()
    p.update()

    for ev in pygame.event.get():
        #fullscreen
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_f:
                if FULLSCREEN:
                    screen = pygame.display.set_mode((screen_width,screen_height), pygame.SCALED|pygame.FULLSCREEN)
                    FULLSCREEN = False
                else:
                    screen = pygame.display.set_mode((screen_width,screen_height))
                    FULLSCREEN = True
            if ev.key == pygame.K_SPACE:
                pos = pygame.mouse.get_pos()
                one = One(pos[0], pos[1])
                square_group.add(one)
        #close window
        if ev.type == pygame.QUIT:
            run = False
    #update screen
    pygame.display.flip()
pygame.quit()