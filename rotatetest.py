import pygame, math

screen = pygame.display.set_mode((800,800))

clock = pygame.time.Clock()
FPS = 60
def center_ang(origin, pivot):
    y = pivot[1] -origin[1]
    x = pivot[0] - origin[0]
    ang= math.degrees(math.atan(-y/x))
    if origin[0] < pivot[0]:
        ang += 180
    
    return ang
def rotate_on_pivot(image, angle, pivot, origin):
    surf = pygame.transform.rotate(image, angle)

    radius = math.hypot(origin[0]-pivot[0], origin[1]- pivot[1])

    offsetx = pivot[0]+ math.cos(math.radians(angle))*(radius)
    offsety = pivot[1] + math.sin(math.radians(-angle))*(radius)

    rect= surf.get_rect(center=(offsetx, offsety))

    return surf, rect

class spinnn(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.centerx = x
        self.centery = y
        self.width = 50
        self.image = pygame.image.load('Man.png')
        self.image_og = pygame.transform.scale(self.image,(self.width, self.width))
        self.dangle = 0

        self.rect = self.image.get_rect(center = (self.centerx, self.centery))
    def update(self):
        self.angle = center_ang((self.centerx, self.centery),(400,400))
        self.dangle +=2
        self.image, rect =rotate_on_pivot(self.image_og, self.angle + self.dangle, (400,400),(self.centerx,self.centery))
        screen.blit(self.image,rect )
        if self.dangle >= 360:
            self.dangle -=360
    
dude_group = pygame.sprite.Group()

run = True
while run:
    clock.tick(FPS)
    screen.fill((250,250,0))

    dude_group.update()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            dude = spinnn(pos[0], pos[1])
            dude_group.add(dude)
    pygame.display.flip()
pygame.quit()