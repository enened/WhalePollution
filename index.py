import pygame, random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Whale game")
clock = pygame.time.Clock()

#Scores 
krill_count = 0 

#Images-------------------------------------
background = pygame.transform.scale(pygame.image.load("images/background.png").convert_alpha(),(400,500))
#Krills
krill = pygame.image.load("images/Krill.png").convert_alpha()
bad_krill = pygame.transform.scale(pygame.image.load("images/BadKrill.png"),(100,50)).convert_alpha()
#Whales 
whale =  pygame.transform.scale(pygame.image.load("images/WhaleNormal.png"), (100, 100)).convert_alpha()
whale_happy = pygame.transform.scale(pygame.image.load("images/WhaleHappy.png"), (100,100)).convert_alpha()
whale_sad = pygame.transform.scale(pygame.image.load("images/WhaleSad.png"),(100,100)).convert_alpha()
#Bad stuff 
pollution = pygame.transform.scale(pygame.image.load("images/pollution.png"),(100,100)).convert_alpha()

#Text 
starting_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Whale Pollution", True, "Black").convert_alpha()
start_1 = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("click anywhere to start", True, "Black").convert_alpha()

#Rectangles--------------------------------------------
krill_rect = krill.get_rect(midtop = (random.randint(0,400), -100))
whale_rect = whale.get_rect(midbottom = (200, 490))
pollution_rect = pollution.get_rect(midtop= (random.randint(0,400), -200))

start_1_rect = start_1.get_rect(midtop = (200,250))

#Functionality
speed = 0

#Body
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
            start_1 = False

    #How fast each thing moves 
    pollution_rect.y += 1 * speed
    krill_rect.y += 1 * speed

    if krill_rect.y > 500: krill_rect.y = -50
    if pollution_rect.y > 500: pollution_rect.y = -200 

    #Placing the surfaces
    screen.blit(background, (0, 0))
    screen.blit(whale, whale_rect)
    screen.blit(pollution, pollution_rect)
    screen.blit(krill, krill_rect)

    #Check for Collisions 
    if whale_rect.colliderect(krill_rect):
        krill_count += 1 

    #Starting Screen 
    if starting_text:
        screen.blit(starting_text, (100,200))
    if start_1:
        pygame.draw.rect(screen, 'Pink', start_1_rect)
        screen.blit(start_1, start_1_rect)

    

    pygame.display.update()
    clock.tick(60)
