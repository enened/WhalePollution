import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Whale game")
clock = pygame.time.Clock()


background = pygame.image.load("images/background.png").convert()
whale =  pygame.transform.scale(pygame.image.load("images/whale.png"), (100, 100)).convert_alpha()
whale_rect = whale.get_rect(midbottom = (50, 290))
pollution =  pygame.transform.scale(pygame.image.load("images/pollution.png"), (100, 100)).convert_alpha()
pollution_rect = pollution.get_rect(midbottom = (850, 290))
starting_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("To start click any key", True, "Black").convert_alpha()
speed = 0


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

    screen.blit(background, (0, 0))
    screen.blit(whale, whale_rect)
    screen.blit(pollution, pollution_rect)

    if starting_text:
        screen.blit(starting_text, (300, 50))

    

    pygame.display.update()
    clock.tick(60)
