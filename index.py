import pygame, random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Whale game")
clock = pygame.time.Clock()

#Images 
background = pygame.image.load("images/background.png").convert()

#Krills 
krill_y_pos = 0 
krill = pygame.image.load("images/Krill.png").convert_alpha()
krill_rect = krill.get_rect(midtop = (random.randint(0,400), krill_y_pos))


bad_krill = pygame.image.load("images/BadKrill.png").convert_alpha()

whale =  pygame.transform.scale(pygame.image.load("images/WhaleNormal.png"), (100, 100)).convert_alpha()
whale_rect = whale.get_rect(midbottom = (200, 490))

pollution =  pygame.transform.scale(pygame.image.load("images/pollution.png"), (100, 100)).convert_alpha()
pollution_rect = pollution.get_rect(midbottom = (850, 290))

starting_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("To start click any key", True, "Black").convert_alpha()
speed = 0

test_surface = pygame.Surface((100,200))

while True:
    
    keys = pygame.key.get_pressed()  # Checking pressed keys

    if keys[pygame.K_d]:
        whale_rect.x += 2
    if keys[pygame.K_a]:
        whale_rect.x -= 2
    if keys[pygame.K_w]:
        whale_rect.y -= 2
    if keys[pygame.K_s]:
        whale_rect.y += 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and starting_text:
            speed = 1
            starting_text = False


    pollution_rect.x -= 1 * speed

    #Placing the surfaces
    screen.blit(background, (0, 0))
    screen.blit(whale, whale_rect)
    screen.blit(pollution, pollution_rect)
    krill_rect.y += 1 
    screen.blit(krill, krill_rect)

    if starting_text:
        screen.blit(starting_text, (100,200))

    

    pygame.display.update()
    clock.tick(60)
