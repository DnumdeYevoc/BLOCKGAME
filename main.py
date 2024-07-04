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
one_img =pygame.image.load('block_1.png').convert_alpha()
cen1_img =pygame.image.load('center_1.png').convert_alpha()
cen2_img =pygame.image.load('center_2.png').convert_alpha()

center_images = [cen1_img, cen2_img]

#define functions
def center_ang(origin, pivot):
    y = pivot[1] -origin[1]
    x = pivot[0] - origin[0]
    if not x == 0:
        ang= math.degrees(math.atan(-y/x))
    else:
        ang = 0
    if origin[0] > pivot[0]:
        ang += 180
    
    return ang
def rotate_on_pivot(image, angle, pivot, origin):
    surf = pygame.transform.rotate(image, angle)

    radius = math.hypot(origin[0]-pivot[0], origin[1]- pivot[1])

    offsetx = pivot[0]+ math.cos(math.radians(angle))*(radius)
    offsety = pivot[1] + math.sin(math.radians(-angle))*(radius)

    rect= surf.get_rect(center=(offsetx, offsety))

    return surf, rect


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

class center():
    def __init__(self, x,y):
        self.centerx = x
        self.centery = y
        self.width = 100
        self.height = 100
        self.x = self.centerx - self.width/2
        self.y = self.centery - self.width/2
        self.index = 0
        self.image_og = center_images[self.index]
        self.image_og = pygame.transform.scale(self.image_og, (self.width, self.height))
        self.center_ang = 0
        self.da = 0
        self.rect = self.image_og.get_rect(center= (self.centerx, self.centery))
        self.mask = pygame.mask.from_surface(self.image_og)
    def update(self):

        c.centerx = game_window_width/2
        c.centery = game_window_height/2
        self.image_og = center_images[self.index]
        self.image_og = pygame.transform.scale(self.image_og, (self.width, self.height))
        
        #set rotation
        self.image, self.rect = rotate_on_pivot(self.image_og, self.center_ang +self.da, (self.centerx, self.centery), (self.centerx, self.centery))

        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.x = self.rect.x
        self.y = self.rect.y
    
        self.mask = pygame.mask.from_surface(self.image)
        game_window.blit(self.image, self.rect)
    def add_side(self):
        if self.index +1 < len(center_images):
            self.index +=1
    def rotate(self,ang):
        for square in square_group:
            square.da += ang
        self.da += ang


class One(pygame.sprite.Sprite):
    def __init__(self, centerx, centery,):
        pygame.sprite.Sprite.__init__(self)
        self.width = 40
        self.height = 40
        self.mass = self.width*self.height/800
        self.x = centerx - self.width/2
        self.y = centery - self.height/2
        self.centerx = centerx
        self.centery = centery
        self.image_og = pygame.transform.scale(one_img, (self.width, self.height))
        self.image = self.image_og
        self.mask = pygame.mask.from_surface(self.image)
        self.center_ang = center_ang((c.centerx, c.centery),(self.centerx, self.centery))
        self.da = 0
        
        self.rect = self.image.get_rect(center = (self.centerx, self.centery))

    def expand(self,x_ratio, y_ratio):
        
        self.width *= x_ratio
        self.height *= y_ratio
        self.mass = self.width*self.height/800
        self.image_og = pygame.transform.scale(one_img, (self.width, self.height))
        self.image = self.image_og
        self.mask = pygame.mask.from_surface(self.image)

        
    def update(self):
        dx = 0
        dy = 0

        #gravity
        point = (c.centerx, c.centery)
        disx = self.centerx - point[0]
        disy = self.centery - point[1]

        if not disx == 0:
            angle = math.atan(disy/disx)
            dy = math.sin(angle)*self.mass
            dx = math.cos(angle)*self.mass
            
        if self.centerx> c.centerx:
            dx *= -1
            dy *= -1

        #collision
        for square in square_group:
            if not square == self:
                if square.mask.overlap(self.mask, (self.x - square.x ,self.y - square.y)):
                    if self.width == square.width and self.height == square.height:
                        self.expand(1.25,1.25)
                        self.x = (self.x+square.x)/2
                        self.y = (self.y+square.y)/2
                        square.kill()
                    else:
                        xdistance = self.centerx - square.centerx 
                        dx = xdistance//(self.width)
                        ydistance = self.centery - square.centery
                        dy = ydistance //(self.height)
                        break
                else:
                    if square.mask.overlap(self.mask, (self.x - square.x + dx, self.y - square.y +dy)):
                        if self.width == square.width and self.height == square.height:
                            self.expand(1.25,1.25)
                            self.x = (self.x+square.x)/2
                            self.y = (self.y+square.y)/2
                            square.kill()
                            self.mask = pygame.mask.from_surface(self.image)
                        else:
                            if -0.1 < self.x + self.width -square.x < 0.1 or -0.1 <square.x + square.width - self.x < 0.1:
                                dx = 0
                            elif -0.1<self.y + self.height -square.y < 0.1 or -0.1<square.y + square.height - self.y<0.1:
                                dy = 0
                            else:
                                dx *= 0.001/self.mass
                                dy *= 0.001/self.mass

        #collision with the center
        if c.mask.overlap(self.mask, (self.x - c.x ,self.y - c.y)):
            xdistance = self.centerx - c.centerx 
            dx = xdistance//(self.width)
            ydistance = self.centery - c.centery
            dy = ydistance //(self.height)
        else:
            if c.mask.overlap(self.mask,(self.x - c.x + dx, self.y - c.y +dy)):
                if -0.3 < self.x + self.width -c.x < 0.3 or -0.3 <c.x + c.width - self.x < 0.3:
                    dx = 0
                elif -0.3<self.y + self.height -c.y < 0.3 or -0.3<c.y + c.height - self.y<0.3:
                    dy = 0
                else:
                    dx *= 0.001/self.mass
                    dy *= 0.001/self.mass


        #update position
        self.x += dx
        self.y += dy

        #update size images
        
        width = self.image.get_width()
        height = self.image.get_height()
        self.centerx = self.x  + width/2 
        self.centery = self.y  + height/2 

        #set rotation
        self.image, self.rect = rotate_on_pivot(self.image_og, self.center_ang +self.da, (c.centerx, c.centery), (self.centerx, self.centery))

        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.x = self.rect.x
        self.y = self.rect.y
    
        self.mask = pygame.mask.from_surface(self.image)
        
        game_window.blit(self.image,self.rect)

    
        
#create instances
square_group = pygame.sprite.Group()
c= center(game_window_width/2, game_window_height/2)

#create groups


#main game loop
run = True
while run:
    clock.tick(FPS)
    #screen.blit((0,0),bg_img)
    screen.fill((100,100,100))
    game_window.fill((0,0,30))

    #planet rotation
    c.rotate(0.05)
    
    #update classes
    c.update()
    square_group.update()
    
    for ev in pygame.event.get():
        #mousepresses
        if ev.type == pygame.MOUSEBUTTONDOWN:
            #rotate squares
            pos = pygame.mouse.get_pos() 
            if 0<pos[0] - shop_size < game_window_width//2:
                
                c.rotate(30)
            elif pos[0] -shop_size >game_window_width//2:
                c.rotate(-30)
                
        
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
            if ev.key == pygame.K_a:
                c.add_side()
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