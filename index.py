import pygame, random
from sys import exit

# initialize game
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Ocean Water Dangers")
clock = pygame.time.Clock()
gameOver = False
hp = 90
speed = 1
maxKrill = 10
maxPollution = 0

#Levels 
lvl = 0
level0 = True 
level1 = False
done1 = 0
level2 = False 
done2 = 0 

seconds = 0 

#Level Placement 
information_txt_place = (120,180)
lvl_txt_place = (160,160)
label_place = (40, 200)
image_place = (40,250)

#Level Text 
level_2_text = pygame.transform.scale(pygame.image.load("images/lvl_2_txt.png"), (250, 190)).convert_alpha()
level_1_text = pygame.transform.scale(pygame.image.load("images/lvl_1_txt.png"), (250, 150)).convert_alpha()
level_0_text = pygame.transform.scale(pygame.image.load("images/lvl_0_txt.png"), (250, 150)).convert_alpha()

p_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Trash", True, "Black").convert_alpha()
k_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Krill", True, "Black").convert_alpha()
b_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Bad Krill", True, "Black").convert_alpha()

# create image surfaces
background = pygame.transform.scale(pygame.image.load("images/background.png").convert(), (400, 500))

whale =  pygame.transform.scale(pygame.image.load("images/whaleNormal.png"), (70, 60)).convert_alpha()
whale_rect = whale.get_rect(midbottom = (50, 500))

starting_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("To start click any key", True, "Black").convert_alpha()
pollution =  pygame.transform.scale(pygame.image.load("images/pollution.png"), (70, 100)).convert_alpha()
krill = pygame.image.load("images/krill.png").convert_alpha()
bad_krill =  pygame.transform.scale(pygame.image.load("images/badKrill.png"), (50, 50)).convert_alpha()

krills = []
pollutions = []
l_hearts = []

def hp_bar(): 
    l_hearts.clear()
    heart = pygame.transform.scale(pygame.image.load("images/heart_bar.png"), (30, 27)).convert_alpha()
    hearts = int(hp/10)
    if (len(l_hearts) < hearts):
        for _ in range(hearts):
                    l_hearts.append(heart)

def update_whale_type():
    global whale, whale_rect, gameOver
    if(hp > 60 or hp == 60):
        whale =  pygame.transform.scale(pygame.image.load("images/whaleHappy.png"), (70, 60)).convert_alpha()
        whale_rect = whale.get_rect(midbottom = (whale_rect.midbottom[0], whale_rect.midbottom[1]))
    elif (hp < 60):
        if hp == 0:
            gameOver = True
        whale =  pygame.transform.scale(pygame.image.load("images/whaleSad.png"), (70, 60)).convert_alpha()
        whale_rect = whale.get_rect(midbottom = (whale_rect.midbottom[0], whale_rect.midbottom[1]))
    else:
        whale =  pygame.transform.scale(pygame.image.load("images/whaleNormal.png"), (70, 60)).convert_alpha()
        whale_rect = whale.get_rect(midbottom = (whale_rect.midbottom[0], whale_rect.midbottom[1]))

def move_whale():
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
                    update_whale_type()
                        
                if whaleKrillCollision:
                    krills[krillIndex] = 0

                    if (krill["type"] == "bad"):
                        hp -= 1
                    else:
                        hp += 1
                    update_whale_type()

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
                        update_whale_type()
            

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

        krills[:] = [i for i in krills if i != 0] 

def spawn_krill(amount, speed):
    global krills, lvl, level2
    if(len(krills) < maxKrill):
        if (random.randint(0, len(pollutions)) > 5):
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

def update_level_on():
    #Between each level talk about the different bad stuff   
    global maxPollution, level1, done1, lvl, level0
    if (hp == 100 and done1==0): 
        level1 = True 
        maxPollution += 10
        lvl += 1 
        done1 += 1





while True:
    hp_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("HP = " + str(hp), True, "Black").convert_alpha()
    lvl_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Level" + str(lvl), True, "Black").convert_alpha()
   
    move_whale()
    checkCollisions()
    update_level_on()
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and starting_text:
            starting_text = False


    #Placing the surfaces
    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()

    if (gameOver):
        end_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 50).render("GAME OVER!", True, "Black").convert_alpha()
        screen.blit(end_text, (80, 200))

    elif (level0): 
        if starting_text:
            screen.blit(starting_text, (100, 100))
            screen.blit(pygame.transform.scale(whale, (210,180)), (130,200))
        else:  
            screen.blit(level_0_text, information_txt_place)
            screen.blit(lvl_text, lvl_txt_place)
            screen.blit(k_text, label_place)
            screen.blit(krill, image_place)

        if keys[pygame.K_c]:
            level0 = False 

    elif (level1): 
        screen.blit(level_1_text, information_txt_place)
        screen.blit(lvl_text, lvl_txt_place)
        screen.blit(p_text, label_place)
        screen.blit(pollution, image_place)
        
        if keys[pygame.K_c]:
            level1 = False 

    elif (level2): 
        screen.blit(level_2_text, information_txt_place)
        screen.blit(lvl_text, lvl_txt_place)
        screen.blit(b_text, label_place)
        screen.blit(bad_krill, image_place)
        
        if keys[pygame.K_c]:
            level2 = False 
            done2 += 1 

    else:    
        screen.blit(whale, whale_rect)
        display_multiple_items(krills)
        display_multiple_items(pollutions)
        screen.blit(hp_text, (20, 10))

        hp_bar()
        place_hearts_x = 350
        for i,v in enumerate(l_hearts): 
            screen.blit(v, (place_hearts_x, 10))
            place_hearts_x -= 20
    




        if ((not len(krills) or not len(pollutions)) and not starting_text):
            spawn_krill(random.randint(0, round(maxKrill)), random.uniform(1, speed))
            spawn_pollution(random.randint(0, round(maxPollution)), random.uniform(1, speed))

    seconds += 1

    pygame.display.update()
    clock.tick(60)


