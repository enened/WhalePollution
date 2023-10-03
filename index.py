import pygame, random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Whale game")
clock = pygame.time.Clock()
speed = 0

# create image surfaces
background = pygame.transform.scale(pygame.image.load("images/background.png").convert(), (400, 500))

starting_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("To start click any key", True, "Black").convert_alpha()

test_surface = pygame.Surface((100,200))

krill = pygame.image.load("images/krill.png").convert_alpha()
krill_rect = krill.get_rect(midbottom = (random.randint(0,400), -10))

whale =  pygame.transform.scale(pygame.image.load("images/whaleNormal.png"), (100, 100)).convert_alpha()
whale_rect = whale.get_rect(midbottom = (50, 500))

pollution =  pygame.transform.scale(pygame.image.load("images/pollution.png"), (50, 50)).convert_alpha()
pollution_rect = pollution.get_rect(midbottom = (850, 290))


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

    if not starting_text:
        krill_rect.y += 1
        pollution_rect.x -= 1 * speed

    #Placing the surfaces
    screen.blit(background, (0, 0))
    screen.blit(whale, whale_rect)
    screen.blit(pollution, pollution_rect)
    screen.blit(pollution, pollution_rect)
    screen.blit(krill,krill_rect)


    if starting_text:
        screen.blit(starting_text, (100, 100))
    

    pygame.display.update()
    clock.tick(60)
