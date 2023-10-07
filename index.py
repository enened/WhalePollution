import pygame, random
from sys import exit

# initialize game
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Whale game")
clock = pygame.time.Clock()
hp = 100
speed = 1
maxKrill = 10
maxPollution = 5

# create image surfaces
background = pygame.transform.scale(pygame.image.load("images/background.png").convert(), (400, 500))

whale =  pygame.transform.scale(pygame.image.load("images/whaleNormal.png"), (70, 60)).convert_alpha()
whale_rect = whale.get_rect(midbottom = (50, 500))

starting_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("To start click any key", True, "Black").convert_alpha()

krills = []
pollutions = []


def updateWhaleType():
    global whale, whale_rect
    if(hp > 130):
        whale =  pygame.transform.scale(pygame.image.load("images/whaleHappy.png"), (70, 60)).convert_alpha()
        whale_rect = whale.get_rect(midbottom = (whale_rect.midbottom[0], whale_rect.midbottom[1]))
    elif (hp < 70):
        whale =  pygame.transform.scale(pygame.image.load("images/whaleSad.png"), (70, 60)).convert_alpha()
        whale_rect = whale.get_rect(midbottom = (whale_rect.midbottom[0], whale_rect.midbottom[1]))
    else:
        whale =  pygame.transform.scale(pygame.image.load("images/whaleNormal.png"), (70, 60)).convert_alpha()
        whale_rect = whale.get_rect(midbottom = (whale_rect.midbottom[0], whale_rect.midbottom[1]))

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
                    if (hp > 0):
                        hp -= 1
                    updateWhaleType()
                        
                if whaleKrillCollision:
                    krills[krillIndex] = 0

                    if (krill["type"] == "bad"):
                        hp -= 1
                    else:
                        hp += 1
                    updateWhaleType()
                if krillPollutionCollision:
                    if krill["item_rect"].bottom >  pollution["item_rect"].top:
                        krill["item_rect"].bottom = pollution["item_rect"].top
                    else:
                        krill["item_rect"].top = pollution["item_rect"].bottom
            else:

                whalePollutionCollision = pygame.Rect.colliderect(whale_rect, pollution["item_rect"])

                if whalePollutionCollision:
                    pollutions[pollutionIndex] = 0
                    if (hp > 0):
                        hp -= 1
                        updateWhaleType()

            krills[:] = [i for i in krills if i != 0] 
        pollutions[:] = [i for i in pollutions if i != 0] 

    else:
        for krillIndex, krill in enumerate(krills):
            whaleKrillCollision = pygame.Rect.colliderect(whale_rect, krill["item_rect"])

            if whaleKrillCollision:
                krills[krillIndex] = 0
                if (krill["type"] == "bad"):
                    hp -= 1
                else:
                    hp += 1

                updateWhaleType()

        krills[:] = [i for i in krills if i != 0] 

def spawn_krill(amount, speed):
    global krills
    if(len(krills) < maxKrill):
        if (random.randint(0, len(pollutions)) > 3):
            badKrill =  pygame.transform.scale(pygame.image.load("images/badKrill.png"), (50, 50)).convert_alpha()
            badKrill_rect = badKrill.get_rect(midbottom = (random.randint(0,400), random.randint(-500, 0)))
            krills.append({"item": badKrill, "item_rect": badKrill_rect, "speed": speed, "type": "bad"})
        else:
            for _ in range(amount):
                krill = pygame.image.load("images/krill.png").convert_alpha()
                krill_rect = krill.get_rect(midbottom = (random.randint(0,400), random.randint(-500, 0)))
                krills.append({"item": krill, "item_rect": krill_rect, "speed": speed, "type": "good"})
    
def spawn_pollution(amount, speed):
    global pollution
    if (len(pollutions) < maxPollution):
        for x in range(amount):
            pollution =  pygame.transform.scale(pygame.image.load("images/pollution.png"), (70, 100)).convert_alpha()
            pollution_rect = pollution.get_rect(midbottom = (random.randint(0,400), random.randint(-500, 0)))
            pollutions.append({"item": pollution, "item_rect": pollution_rect, "speed": speed})

def display_multiple_items(itemArray):
    global maxKrill, maxPollution, speed

    for index, item in enumerate(itemArray):
        item["item_rect"].y += item["speed"] 
        screen.blit(item["item"], item["item_rect"])

        if (item["item_rect"].y > 500 and maxKrill > 1):
            maxKrill -= 0.01
            maxPollution += 0.01
            spawn_krill(random.randint(0, round(maxKrill)), random.uniform(1, speed))
            spawn_pollution(random.randint(0, round(maxPollution)), random.uniform(1, speed))
            itemArray[index] = 0
            speed += 0.01
        elif(item["item_rect"].y > 500):
            spawn_krill(random.randint(0, round(maxKrill)), random.uniform(1, speed))
            spawn_pollution(random.randint(0, round(maxPollution)), random.uniform(1, speed))
            itemArray[index] = 0
            speed += 0.01
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
            spawn_krill(random.randint(0, round(maxKrill)), random.uniform(1, speed))
            spawn_pollution(random.randint(0, round(maxPollution)), random.uniform(1, speed))

    moveWhale()
    checkCollisions()


    #Placing the surfaces
    screen.blit(background, (0, 0))
    screen.blit(whale, whale_rect)
    display_multiple_items(krills)
    display_multiple_items(pollutions)
    screen.blit(hp_text, (310, 10))

    if ((not len(krills) or not len(pollutions)) and not starting_text):
        spawn_krill(random.randint(0, round(maxKrill)), random.uniform(1, speed))
        spawn_pollution(random.randint(0, round(maxPollution)), random.uniform(1, speed))
    # show starting screen and start game when a key is pressed. 
    if starting_text:
        screen.blit(starting_text, (100, 100))

    pygame.display.update()
    clock.tick(60)
