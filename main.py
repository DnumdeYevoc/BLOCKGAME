import pygame, math
#set clock
clock = pygame.time.Clock()

#define game variables
FULLSCREEN = False
screen_width = 600
screen_height = 400
gravity = 1
floor= screen_height - 200
FPS = 60
dt = clock.tick(FPS)/25

#set screen
screen = pygame.display.set_mode((screen_width,screen_height), )

#set game window
shop_size = 200
game_window_width = screen_width - shop_size
game_window_height = screen_height

game_window = pygame.surface.Surface((game_window_width, game_window_height))

#load images

#define functions

def expand(screen_width, screen_height, screen, game_window_width, game_window_height, game_window, expand_amount):
    screen_width += expand_amount
    screen_height += expand_amount
    screen = pygame.display.set_mode((screen_width,screen_height))
    game_window_width = screen_width - shop_size
    game_window_height = screen_height
    game_window = pygame.surface.Surface((game_window_width, game_window_height))

    for square in square_group:
        square.x += expand_amount/2
        square.y += expand_amount/2

    return screen_width, screen_height, screen, game_window_width, game_window_height, game_window

#define classes
#class button to be created

#class shop where it creates buttons and gui

class point():
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.width = 10
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.width)
    def update(self):
        #pos = pygame.mouse.get_pos()
        #mouse = pygame.rect.Rect(pos[0], pos[1], 10 ,10)
        #if pygame.mouse.get_pressed()[0] == 1:
                
                #self.y = pos[1]
                #self.x = pos[0]
        self.x = game_window_width//2
        self.y = game_window_height//2
        pygame.draw.circle(game_window, (250,250,250), (self.x, self.y), self.width, 10)

class One(pygame.sprite.Sprite):
    def __init__(self, centerx, centery):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 60
        self.x = centerx - self.width/2
        self.y = centery - self.height/2
        self.centerx = centerx
        self.centery = centery
        self.image = pygame.image.load('block_1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation_count = 0
        
    
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
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

        for square in square_group:
            if not square == self:
                if self.mask.overlap(square.mask, (self.centerx - square.centerx ,self.centery - square.centery)):
                        xdistance = self.centerx - square.centerx 
                        dx = xdistance//(self.width /4)
                        ydistance = self.centery - square.centery 
                        dy = ydistance //(self.height /4)
                        break
                else:
                    if self.mask.overlap(square.mask, (self.centerx - square.centerx + dx, self.centery - square.centery +dy)):
                        dx = 0
                        dy = 0

        #update position
        self.x += dx
        self.y += dy
        self.centerx = self.x + self.width/2
        self.centery = self.y + self.height/2
        self.rect = self.image.get_rect( center = (self.centerx, self.centery))
        game_window.blit(self.image,self.rect)
        


    def rotate(self, degree):
        if self.rotation_count == 360 - degree:
            self.image = pygame.image.load('block_1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rotation_count = 0
            
        elif self.rotation_count == 180- degree:
            self.image = pygame.image.load('block_1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.image = pygame.transform.flip(self.image,True , True)
            self.rotation_count += degree

        else:
            self.image = pygame.transform.rotate(self.image, degree)
            self.rotation_count += degree
#create instances
square_group = pygame.sprite.Group()
p= point(game_window_width/2, game_window_height/2)

#create groups


#main game loop
run = True
while run:
    clock.tick(FPS)
    #screen.blit((0,0),bg_img)
    screen.fill((100,100,100))
    game_window.fill((0,0,30))
    
    #update classes
    square_group.update()
    p.update()

    for ev in pygame.event.get():
        #mousepresses
        if ev.type == pygame.MOUSEBUTTONDOWN:
            #rotate squares
            pos = pygame.mouse.get_pos() 
            if 0<pos[0] - shop_size < game_window_width//2:
                for square in square_group:
                    square.rotate(45)
                print('rotate left')
            elif pos[0] -shop_size >game_window_width//2:
                print ('rotate right')
            
        #keypresses
        #fullscreen
        if ev.type == pygame.KEYDOWN:
            #add blocks
            if ev.key == pygame.K_SPACE:
                pos = pygame.mouse.get_pos() 
                one = One(pos[0]- shop_size, pos[1])
                square_group.add(one)
            if ev.key == pygame.K_e:
                #expand the window on both axises
                screen_width, screen_height, screen, game_window_width, game_window_height, game_window =expand(screen_width, screen_height, screen, game_window_width, game_window_height, game_window, 50)
                #check for fullscreen
                if FULLSCREEN:
                    screen = pygame.display.set_mode((screen_width,screen_height), pygame.SCALED|pygame.FULLSCREEN)
                    
                else:
                    screen = pygame.display.set_mode((screen_width,screen_height))
                    
            #FULLSCREEN
            if ev.key == pygame.K_f:
                FULLSCREEN= not FULLSCREEN
                if FULLSCREEN:
                    screen = pygame.display.set_mode((screen_width,screen_height), pygame.SCALED|pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_width,screen_height))
        #close window
        if ev.type == pygame.QUIT:
            run = False
    #update screen
    screen.blit(game_window, (200,0))
    pygame.display.flip()
pygame.quit()