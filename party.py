import pygame, random, os
pygame.init()
FULLSCREEN = False
screen = pygame.display.set_mode((400,400))
man = pygame.image.load('Man.png').convert_alpha()
man = pygame.transform.scale(man, (400,400))
current_color = (0,250,250)
run = True
while run:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_f:
                if FULLSCREEN:
                    screen = pygame.display.set_mode((400,400), pygame.SCALED|pygame.FULLSCREEN)
                    FULLSCREEN = False
                else:
                    screen = pygame.display.set_mode((400,400))
                    FULLSCREEN = True
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            pygame.FULLSCREEN = True
            current_color = random.sample(range(0,256),3)
    screen.fill(current_color)
    screen.blit(man, (0,0))
    pygame.display.flip()
pygame.quit()