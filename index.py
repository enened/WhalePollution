import pygame, random
from sys import exit

# initialize game
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Whale game")
clock = pygame.time.Clock()
hp = 100
pollution_speed = 1
krillSpeed = 1
maxKrill = 10
maxPollution = 5

# create image surfaces
background = pygame.transform.scale(pygame.image.load("images/background.png").convert(), (400, 500))

starting_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("To start click any key", True, "Black").convert_alpha()

test_surface = pygame.Surface((100,200))

krills = []
pollutions = []

whale =  pygame.transform.scale(pygame.image.load("images/whaleNormal.png"), (70, 60)).convert_alpha()
whale_rect = whale.get_rect(midbottom = (50, 500))


def moveWhale():
    keys = pygame.key.get_pressed()  # Checking pressed keys

    if keys[pygame.K_d] and whale_rect.x < 330:
        whale_rect.x += 2
    if keys[pygame.K_a]  and whale_rect.x > 1:
        whale_rect.x -= 2
    if keys[pygame.K_w] and whale_rect.y > 5:
        whale_rect.y -= 2
    if keys[pygame.K_s] and whale_rect.y < 440:
        whale_rect.y += 2
    
def checkCollisions():
    global hp
    
    if (len(pollutions) != 0):
        for pollutionIndex, pollution in enumerate(pollutions):
            for krillIndex, krill in enumerate(krills):
                whalePollutionCollision = pygame.Rect.colliderect(whale_rect, pollution["item_rect"])
                krillPollutionCollision = pygame.Rect.colliderect(krill["item_rect"],  pollution["item_rect"])
                whaleKrillCollision = pygame.Rect.colliderect(whale_rect, krill["item_rect"])

                if whalePollutionCollision:
                    pollutions[pollutionIndex] = 0
                    hp -= 1
                if whaleKrillCollision:
                    krills[krillIndex] = 0
                    hp += 1
                if krillPollutionCollision:
                    krill["item_rect"].bottom = pollution["item_rect"].top
            else:

                whalePollutionCollision = pygame.Rect.colliderect(whale_rect, pollution["item_rect"])

                if whalePollutionCollision:
                    pollutions[pollutionIndex] = 0
                    hp -= 1
            krills[:] = [i for i in krills if i != 0] 
        pollutions[:] = [i for i in pollutions if i != 0] 

    else:
        for krillIndex, krill in enumerate(krills):
            whaleKrillCollision = pygame.Rect.colliderect(whale_rect, krill["item_rect"])

            if whaleKrillCollision:
                krills[krillIndex] = 0
                hp += 1

        krills[:] = [i for i in krills if i != 0] 


def spawn_krill(amount):
    global krills
    if(len(krills) < maxKrill):
        for x in range(amount):
            krill = pygame.image.load("images/krill.png").convert_alpha()
            krill_rect = krill.get_rect(midbottom = (random.randint(0,400), random.randint(-500, 0)))
            krills.append({"item": krill, "item_rect": krill_rect, "speed": 1})
    
def spawn_pollution(amount):
    global pollution
    if (len(pollutions) < maxPollution):
        for x in range(amount):
            pollution =  pygame.transform.scale(pygame.image.load("images/pollution.png"), (70, 100)).convert_alpha()
            pollution_rect = pollution.get_rect(midbottom = (random.randint(0,400), random.randint(-500, 0)))
            pollutions.append({"item": pollution, "item_rect": pollution_rect, "speed": 1})

def display_multiple_items(itemArray):
    global maxKrill, maxPollution

    for index, item in enumerate(itemArray):

        item["item_rect"].y += item["speed"]
        screen.blit(item["item"], item["item_rect"])

        if (item["item_rect"].y > 500 and maxKrill > 1):
            maxKrill -= 0.01
            maxPollution += 0.01
            spawn_krill(random.randint(0, round(maxKrill)))
            spawn_pollution(random.randint(0, round(maxPollution)))
            itemArray[index] = 0
        elif(item["item_rect"].y > 500):
            spawn_krill(random.randint(0, round(maxKrill)))
            spawn_pollution(random.randint(0, round(maxPollution)))
            itemArray[index] = 0
            maxPollution += .01

    itemArray[:] = [i for i in itemArray if i != 0] 

while True:
    hp_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("HP = " + str(hp), True, "Black").convert_alpha()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and starting_text:
            starting_text = False
            spawn_krill(random.randint(0, round(maxKrill)))
            spawn_pollution(random.randint(0, round(maxPollution)))

    moveWhale()
    checkCollisions()


    #Placing the surfaces
    screen.blit(background, (0, 0))
    screen.blit(whale, whale_rect)
    display_multiple_items(krills)
    display_multiple_items(pollutions)
    screen.blit(hp_text, (310, 10))
    print(krills, pollutions)

    if (not len(krills) or not len(pollutions)):
        spawn_krill(random.randint(0, round(maxKrill)))
        spawn_pollution(random.randint(0, round(maxPollution)))
    # show starting screen and start game when a key is pressed. 
    if starting_text:
        screen.blit(starting_text, (100, 100))

    pygame.display.update()
    clock.tick(60)
