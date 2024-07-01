import pygame, math
#set clock
clock = pygame.time.Clock()

#define game variables
FULLSCREEN = False
screen_width = 400
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
class One(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = 20
        self.center_x = self.x + self.radius
        self.center_y = self.y + self.radius
        self.image = pygame.image.load('one.png')
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        self.vel = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        dx = 0
        dy = 0
        #gravity
        self.vel += gravity *dt
        if self.vel >= 15:
            self.vel = 15
        dy += self.vel
        


        #collision
        #check for collision with self
        for one in one_group:
            if not one == self:
                distance = math.sqrt((self.center_x - one.center_x+dx)**2+(self.center_y - one.center_y+dy)**2)
                if distance <= self.radius*2:
                    one_group.remove((self, one))
                    ball_group.remove((self, one))
                    two = Two(self.x, self.y)
                    two_group.add(two)
        for ball in ball_group:
            if not ball == self:
                if pygame.Rect.colliderect(self.rect, ball.rect):
                    if self.mask.overlap(ball.mask, ((self.center_x - ball.center_x+dx),(self.center_y - ball.center_y+ dy))):
                        distance = math.sqrt((self.center_x - ball.center_x)**2+(self.center_y - ball.center_y)**2)
                        hyp = distance - (self.radius + ball.radius)
                        if not distance == 0:
                            ang = math.asin((self.center_y - ball.center_y)/distance)
                            dy = math.sin(ang)*hyp
                            dx = math.cos(ang)*hyp
                            if self.center_y < ball.center_y:
                                dy *= -1
                            elif self.center_x < ball.center_x:
                                dx += -1
                        else:
                            dy = -100
        #floor
        if self.y + dy > floor- self.radius*2:
            dy = 0
            self.y = floor - self.radius*2
            #walls
        if self.x +dx > screen_width- self.radius*2:
            dx = 0
            self.x = screen_width - self.radius*2
        if self.x + dx <= 0:
            dx = 0
            self.x = 0
        
                            
        #update position
        self.x += dx
        self.y += dy
        self.center_x = self.x + self.radius
        self.center_y = self.y + self.radius
        screen.blit(self.image,(self.x,self.y))

class Two(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = 40
        self.center_x = self.x + self.radius
        self.center_y = self.y + self.radius
        self.image = pygame.image.load('two.png')
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        self.vel = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        dx = 0
        dy = 0
        #gravity
        self.vel += gravity *dt
        if self.vel >= 15:
            self.vel = 15
        dy += self.vel

        #collision
        for two in two_group:
            if not two == self:
                distance = math.sqrt((self.center_x - two.center_x)**2+(self.center_y - two.center_y)**2)
                if distance <= self.radius*2:
                    two_group.remove((self,two))
                    ball_group.remove((self, two))
                    four = Four(self.x, self.y)
                    four_group.add(four)
        for ball in ball_group:
            if not ball == self:
                if pygame.Rect.colliderect(self.rect, ball.rect):
                    if self.mask.overlap(ball.mask, ((self.center_x - ball.center_x+dx),(self.center_y - ball.center_y+ dy))):
                        distance = math.sqrt((self.center_x - ball.center_x)**2+(self.center_y - ball.center_y)**2)
                        hyp = distance - (self.radius + ball.radius)
                        if not distance == 0:
                            ang = math.asin((self.center_y - ball.center_y)/distance)
                            dy = math.sin(ang)*hyp
                            dx = math.cos(ang)*hyp
                            if self.center_y < ball.center_y:
                                dy *= -1
                            elif self.center_x < ball.center_x:
                                dx += -1
                        else:
                            dy = -100
        #floor
        if self.y + dy > floor- self.radius*2:
            dy = 0
            self.y = floor - self.radius*2
            #walls
        if self.x +dx > screen_width- self.radius*2:
            dx = 0
            self.x = screen_width - self.radius*2
        if self.x + dx <= 0:
            dx = 0
            self.x = 0
        
        self.x += dx
        self.y += dy
        self.center_x = self.x + self.radius
        self.center_y = self.y + self.radius
        screen.blit(self.image,(self.x,self.y))

class Four(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = 60
        self.center_x = self.x + self.radius
        self.center_y = self.y + self.radius
        self.image = pygame.image.load('four.png')
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        self.vel = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
            dy = 0
            dx = 0
            #gravity
            self.vel += gravity *dt
            if self.vel >= 15:
                self.vel = 15
            dy += self.vel
            #floor
            if self.y >= floor- self.radius*2:
                dy = 0
                self.y = floor- self.radius*2
        
            for four in four_group:
                if not four == self:
                    distance = math.sqrt((self.center_x - four.center_x)**2+(self.center_y - four.center_y)**2)
                    if distance <= self.radius*2:
                        four_group.remove(self)
                        four_group.remove(four)
                        #eight = Eight(self.x, self.y)
                        #eight_group.add(eight)
            for ball in ball_group:
                if not ball == self:
                    if pygame.Rect.colliderect(self.rect, ball.rect):
                        if self.mask.overlap(ball.mask, ((self.center_x - ball.center_x+dx),(self.center_y - ball.center_y+ dy))):
                            distance = math.sqrt((self.center_x - ball.center_x)**2+(self.center_y - ball.center_y)**2)
                            hyp = distance - (self.radius + ball.radius)
                            if not distance == 0:
                                ang = math.asin((self.center_y - ball.center_y)/distance)
                                dy = math.sin(ang)*hyp
                                dx = math.cos(ang)*hyp
                                if self.center_y < ball.center_y:
                                    dy *= -1
                                elif self.center_x < ball.center_x:
                                    dx += -1
                            else:
                                dy = -100
            #floor
            if self.y + dy > floor- self.radius*2:
                dy = 0
                self.y = floor - self.radius*2
                #walls
            if self.x +dx > screen_width- self.radius*2:
                dx = 0
                self.x = screen_width - self.radius*2
            if self.x + dx <= 0:
                dx = 0
                self.x = 0
            
            self.x += dx
            self.y += dy
            self.center_x = self.x + self.radius
            self.center_y = self.y + self.radius
            screen.blit(self.image,(self.x,self.y))

one_group = pygame.sprite.Group()
two_group = pygame.sprite.Group()
four_group = pygame.sprite.Group()
eight_group = pygame.sprite.Group()

ball_group = pygame.sprite.Group()

#main game loop
run = True
while run:
    clock.tick(FPS)
    #screen.blit((0,0),bg_img)
    screen.fill((0,100,100))

    #update balls
 
    ball_group.add(one_group)
    ball_group.add(two_group)
    ball_group.add(four_group)
    ball_group.add(eight_group)

    ball_group.update()



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
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            one = One(pos[0]-30, pos[1])
            one_group.add(one)
        #close window
        if ev.type == pygame.QUIT:
            run = False
    #update screen
    pygame.display.flip()
pygame.quit()