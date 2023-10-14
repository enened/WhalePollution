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
max_krill = 10
max_pollution = 0
max_poacher = 0
num_pollution_despawned = 0
whale_stop = 0
whale_poisoned = 0
level = 0
cause_of_death = ""

#Level Placement 
information_txt_place = (110,180)
lvl_txt_place = (160,150)
label_place = (20, 200)
image_place = (20,250)

#Level Text 
level_3_text = pygame.transform.scale(pygame.image.load("images/lvl_3_txt.png"), (290, 210)).convert_alpha()
level_2_text = pygame.transform.scale(pygame.image.load("images/lvl_2_txt.png"), (290, 210)).convert_alpha()
level_1_text = pygame.transform.scale(pygame.image.load("images/lvl_1_txt.png"), (290, 190)).convert_alpha()
level_0_text = pygame.transform.scale(pygame.image.load("images/lvl_0_txt.png"), (290, 190)).convert_alpha()


# text
pollution_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Trash", True, "Black").convert_alpha()
krill_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Krill", True, "Black").convert_alpha()
bad_krill_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Bad Krill", True, "Black").convert_alpha()
poacher_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Poacher", True, "Black").convert_alpha()
continue_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Press S to continue", True, "Black").convert_alpha()
up_movement_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 15).render("Use W to move up", True, "Black").convert_alpha()
down_movement_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 15).render("S to move down", True, "Black").convert_alpha()
left_movement_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 15).render("A to move left", True, "Black").convert_alpha()
right_movement_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 15).render("D to move right", True, "Black").convert_alpha()
starting_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Press P to start", True, "Black").convert_alpha()
whale_frozen_text_1 = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("The whale was immobilized by poachers!", True, "Black").convert_alpha()
whale_frozen_text_2 = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Click WASD as fast to free yourself", True, "Black").convert_alpha()
title = pygame.transform.scale(pygame.image.load("images/title.png"), (200, 100)).convert_alpha()

# create image surfaces
background = pygame.transform.scale(pygame.image.load("images/background.png").convert(), (400, 500))
wasd = pygame.transform.scale(pygame.image.load("images/wasd_i.png").convert_alpha(), (300, 300))
display_wasd_image = True 

whale =  pygame.transform.scale(pygame.image.load("images/whaleNormal.png"), (70, 60)).convert_alpha()
whale_rect = whale.get_rect(midbottom = (50, 500))
pygame.display.set_icon(whale)

# pollution, krill, bad krill, and poacher
pollution =  pygame.transform.scale(pygame.image.load("images/pollution.png"), (70, 100)).convert_alpha()
krill = pygame.image.load("images/krill.png").convert_alpha()
badKrill =  pygame.transform.scale(pygame.image.load("images/badKrill.png"), (50, 50)).convert_alpha()
poacher =  pygame.transform.scale(pygame.image.load("images/poacher.png"), (100, 100)).convert_alpha()

play_again_button =  pygame.transform.scale(pygame.image.load("images/play_again_button.png"), (150, 50)).convert_alpha()
play_again_button_rect = play_again_button.get_rect(midbottom = (190, 400))


krills = []
pollutions = []
poachers = []
health_hearts = []


# have different number of hearts based on hp
def hp_bar(): 
    health_hearts.clear()
    heart = pygame.transform.scale(pygame.image.load("images/heart_bar.png"), (30, 27)).convert_alpha()
    hearts = round(hp/20)

    for _ in range(hearts):
        health_hearts.append(heart)

# show different whale image based on hp
def update_whale_type():
    global whale, whale_rect, gameOver
    if(hp > 110):
        whale =  pygame.transform.scale(pygame.image.load("images/whaleHappy.png"), (70, 60)).convert_alpha()
        whale_rect = whale.get_rect(midbottom = (whale_rect.midbottom[0], whale_rect.midbottom[1]))
    elif (hp < 70):
        if hp == 0:
            gameOver = True
        whale =  pygame.transform.scale(pygame.image.load("images/whaleSad.png"), (70, 60)).convert_alpha()
        whale_rect = whale.get_rect(midbottom = (whale_rect.midbottom[0], whale_rect.midbottom[1]))
    else:
        whale =  pygame.transform.scale(pygame.image.load("images/whaleNormal.png"), (70, 60)).convert_alpha()
        whale_rect = whale.get_rect(midbottom = (whale_rect.midbottom[0], whale_rect.midbottom[1]))

# move whale position based on user input
def move_whale():
    global hp, gameOver, cause_of_death, whale_stop

    keys = pygame.key.get_pressed()  # Checking pressed keys

    if keys[pygame.K_d] and whale_rect.x < 330 and whale_stop == 0: 
        whale_rect.x += 2

    if keys[pygame.K_a]  and whale_rect.x > 1 and whale_stop == 0: 
        whale_rect.x -= 2
        
    if keys[pygame.K_w] and whale_rect.y > 5 and whale_stop == 0:
        whale_rect.y -= 2

    if keys[pygame.K_s] and whale_rect.y < 440 and whale_stop == 0:
        whale_rect.y += 2

    if whale_poisoned and hp > 0 and not gameOver:
        hp -= whale_poisoned

        if (hp < 1):
            gameOver = True
            cause_of_death = "Consumption of contaminated prey"

# check for collisions between whale, krill, and pollution and change hp and item position based on collisions. 
def checkCollisions():
    global hp, whale_poisoned, gameOver, num_pollution_despawned, cause_of_death, whale_stop
    
    for pollution_index, pollution in enumerate(pollutions):
        whale_pollution_collision = pygame.Rect.colliderect(whale_rect, pollution["item_rect"])

        if whale_pollution_collision:
            pollutions[pollution_index] = 0
            hp -= 1
            if (hp <= 0):
                gameOver = True
                cause_of_death = "Pollution"                    

    for poacher_index, poacher in enumerate(poachers):
        whale_poacher_collision = pygame.Rect.colliderect(whale_rect, poacher["item_rect"])

        if whale_poacher_collision:
            if (not poacher["first_hit"] and whale_stop == 0):
                poachers[poacher_index] = 0
                
            if (poacher["first_hit"]):
                whale_stop += 20
                poacher["first_hit"] = False
            hp -= 0.01

            if (hp <= 0):
                gameOver = True
                cause_of_death = "Poaching" 
        else:
            poacher["first_hit"] = True
                         

    for krill_index, krill in enumerate(krills):
        whaleKrillCollision = pygame.Rect.colliderect(whale_rect, krill["item_rect"])

        if whaleKrillCollision:
            krills[krill_index] = 0
            if (krill["type"] == "bad_krill"):
                hp -= 1
                whale_poisoned += 0.01

                if (hp <= 0):
                    gameOver = True
                    cause_of_death = "Consumption of contaminated prey"                   

            else:
                if (hp < 200):
                    hp += 1

    krills[:] = [i for i in krills if i != 0]
    pollutions[:] = [i for i in pollutions if i != 0] 
    poachers[:] = [i for i in poachers if i != 0] 

    update_whale_type()

# spawn random amount of krill with random speed
def spawn_krill(amount, speed):
    global krills, level
    if(len(krills) < max_krill):
        if (random.randint(0, len(pollutions) + 1) > 6) and level >= 2:

            badKrill =  pygame.transform.scale(pygame.image.load("images/badKrill.png"), (50, 50)).convert_alpha()
            badKrill_rect = badKrill.get_rect(midbottom = (random.randint(0,400), random.randint(-500, 0)))
            krills.append({"item": badKrill, "item_rect": badKrill_rect, "speed": speed, "type": "bad_krill"})
        else:
            for _ in range(amount):
                krill = pygame.image.load("images/krill.png").convert_alpha()
                krill_rect = krill.get_rect(midbottom = (random.randint(0,400), random.randint(-500, 0)))
                krills.append({"item": krill, "item_rect": krill_rect, "speed": speed, "type": "good_krill"})

# spawn random amounts of pollution with random speed
def spawn_pollution(amount, speed):
    global pollution
    if (len(pollutions) < max_pollution):
        for _ in range(amount):
            pollution =  pygame.transform.scale(pygame.image.load("images/pollution.png"), (70, 100)).convert_alpha()
            pollution_rect = pollution.get_rect(midbottom = (random.randint(0,400), random.randint(-500, 0)))
            pollutions.append({"item": pollution, "item_rect": pollution_rect, "speed": speed, "type": "pollution"})

# spawn random amounts of pollution with random speed
def spawn_poachers(amount, speed):
    global poachers
    if (len(poachers) < max_poacher):
        for _ in range(amount):
            poacher =  pygame.transform.scale(pygame.image.load("images/poacher.png"), (100, 100)).convert_alpha()
            poacher_rect = poacher.get_rect(midbottom = (random.randint(0,400), random.randint(-500, 0)))
            poachers.append({"item": poacher, "item_rect": poacher_rect, "speed": speed, "type": "poacher", "first_hit": True})

# display krill and pollution and show their movements
def display_multiple_items(itemArray):
    global max_krill, max_pollution, max_poacher, speed, level, num_pollution_despawned

    for index, item in enumerate(itemArray):
        if (item["type"] != "poacher" or item["first_hit"]):
            item["item_rect"].y += item["speed"] 
        screen.blit(item["item"], item["item_rect"])

        if(item["item_rect"].y > 500):
            max_pollution += .01
            itemArray[index] = 0
            speed += 0.01

            spawn_krill(random.randint(0, round(max_krill)), random.uniform(1, speed))
            spawn_pollution(random.randint(0, round(max_pollution)), random.uniform(1, speed))
            spawn_poachers(random.randint(0, round(max_poacher)), random.uniform(1, speed))

            if(item["type"] == "pollution"):
                num_pollution_despawned += 1

            if (max_krill > 1):
                max_krill -= 0.01
            
            if (max_poacher):
                max_poacher += 0.01

    itemArray[:] = [i for i in itemArray if i != 0] 

# update level 
def update_level_on():
    #Between each level talk about the different bad stuff   
    global max_pollution, level

    if (hp > 100 and level < 1):
        max_pollution += 7
        level = 1
    if (num_pollution_despawned > 14 and level < 2):
        level = 2
    if (num_pollution_despawned > 34 and level < 3):
        level = 3

# play again
def play_again():

    global gameOver, hp, speed, max_krill, max_pollution, max_poacher, num_pollution_despawned, whale_stop, whale_poisoned, level, cause_of_death, information_txt_place
    global lvl_txt_place, label_place, image_place, level_3_text, level_2_text, level_1_text, level_0_text, pollution_text, krill_text, bad_krill_text, poacher_text
    global continue_text, up_movement_text, down_movement_text, left_movement_text, right_movement_text, starting_text, whale_frozen_text_1, whale_frozen_text_2, title
    global background, wasd, display_wasd_image, whale, whale_rect, pollution, krill, badKrill, poacher, play_again_button_rect, krills, pollutions, poachers, health_hearts


    # reset all variables
    gameOver = False
    hp = 90
    speed = 1
    max_krill = 10
    max_pollution = 0
    max_poacher = 0
    num_pollution_despawned = 0
    whale_stop = 0
    whale_poisoned = 0
    level = 0
    cause_of_death = ""

    #Level Placement 
    information_txt_place = (110,180)
    lvl_txt_place = (160,150)
    label_place = (20, 200)
    image_place = (20,250)

    #Level Text 
    level_3_text = pygame.transform.scale(pygame.image.load("images/lvl_3_txt.png"), (290, 210)).convert_alpha()
    level_2_text = pygame.transform.scale(pygame.image.load("images/lvl_2_txt.png"), (290, 210)).convert_alpha()
    level_1_text = pygame.transform.scale(pygame.image.load("images/lvl_1_txt.png"), (290, 190)).convert_alpha()
    level_0_text = pygame.transform.scale(pygame.image.load("images/lvl_0_txt.png"), (290, 190)).convert_alpha()


    # text
    pollution_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Trash", True, "Black").convert_alpha()
    krill_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Krill", True, "Black").convert_alpha()
    bad_krill_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Bad Krill", True, "Black").convert_alpha()
    poacher_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Poacher", True, "Black").convert_alpha()
    continue_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Press S to continue", True, "Black").convert_alpha()
    up_movement_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 15).render("Use W to move up", True, "Black").convert_alpha()
    down_movement_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 15).render("S to move down", True, "Black").convert_alpha()
    left_movement_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 15).render("A to move left", True, "Black").convert_alpha()
    right_movement_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 15).render("D to move right", True, "Black").convert_alpha()
    starting_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Press P to start", True, "Black").convert_alpha()
    whale_frozen_text_1 = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("The whale was immobilized by poachers!", True, "Black").convert_alpha()
    whale_frozen_text_2 = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Click WASD as fast to free yourself", True, "Black").convert_alpha()
    title = pygame.transform.scale(pygame.image.load("images/title.png"), (200, 100)).convert_alpha()

    # create image surfaces
    background = pygame.transform.scale(pygame.image.load("images/background.png").convert(), (400, 500))
    wasd = pygame.transform.scale(pygame.image.load("images/wasd_i.png").convert_alpha(), (300, 300))
    display_wasd_image = True 

    whale =  pygame.transform.scale(pygame.image.load("images/whaleNormal.png"), (70, 60)).convert_alpha()
    whale_rect = whale.get_rect(midbottom = (50, 500))
    pygame.display.set_icon(whale)

    # pollution, krill, bad krill, and poacher
    pollution =  pygame.transform.scale(pygame.image.load("images/pollution.png"), (70, 100)).convert_alpha()
    krill = pygame.image.load("images/krill.png").convert_alpha()
    badKrill =  pygame.transform.scale(pygame.image.load("images/badKrill.png"), (50, 50)).convert_alpha()
    poacher =  pygame.transform.scale(pygame.image.load("images/poacher.png"), (100, 100)).convert_alpha()

    play_again_button =  pygame.transform.scale(pygame.image.load("images/play_again_button.png"), (150, 50)).convert_alpha()
    play_again_button_rect = play_again_button.get_rect(midbottom = (190, 400))


    krills = []
    pollutions = []
    poachers = []
    health_hearts = []

while True:
    hp_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("HP = " + str(round(hp)), True, "Black").convert_alpha()
    lvl_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 20).render("Level" + str(level), True, "Black").convert_alpha()


    update_level_on()

    # exit game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and whale_stop > 0: 
  

            if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d: 
                whale_stop -= 1 
  

    #Placing the surfaces
    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()

    #Different Stages of Game 
    if (gameOver):
        end_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 50).render("GAME OVER!", True, "Black").convert_alpha()
        cause_of_death_text = pygame.font.Font("fonts\ARCADECLASSIC.TTF", 16).render("Cause of death:  " + cause_of_death, True, "Black").convert_alpha()
        
        if len(cause_of_death) > 20:
            cause_of_death_text_x_coord = 5
        else:
            cause_of_death_text_x_coord = 110

        screen.blit(end_text, (80, 200))
        screen.blit(cause_of_death_text, (cause_of_death_text_x_coord, 300))
        screen.blit(play_again_button, play_again_button_rect)

        mouse_position = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()[0]

        if play_again_button_rect.collidepoint(mouse_position) and mouse_press:
            play_again()

    # tutorial level
    elif (level == 0): 
        if starting_text:
            screen.blit(starting_text, (120, 150))
            screen.blit(title, (110, 10))
            screen.blit(pygame.transform.scale(whale, (210, 180)), (110, 200))

            if keys[pygame.K_p]:
                starting_text = False
        elif display_wasd_image:
            screen.blit(up_movement_text, (150, 150))
            screen.blit(down_movement_text, (150, 450))
            screen.blit(left_movement_text, (10, 300))
            screen.blit(right_movement_text, (300, 300))
            screen.blit(wasd, (60, 150))
            screen.blit(continue_text, (110, 70))
            if keys[pygame.K_s]:
                display_wasd_image = False 
        else: 
            screen.blit(level_0_text, information_txt_place)
            screen.blit(lvl_text, lvl_txt_place)
            screen.blit(krill_text, label_place)
            screen.blit(krill, image_place)

            if keys[pygame.K_c]:
                level = 0.5


    #Information About Trash/Plastic
    elif (level == 1): 
        screen.blit(level_1_text, information_txt_place)
        screen.blit(lvl_text, lvl_txt_place)
        screen.blit(pollution_text, label_place)
        screen.blit(pollution, image_place)
        
        if keys[pygame.K_c]:
            level = 1.5 

    #Information About Oil Pollution 
    elif (level == 2): 
        screen.blit(level_2_text, information_txt_place)
        screen.blit(lvl_text, lvl_txt_place)
        screen.blit(bad_krill_text, label_place)
        screen.blit(badKrill, image_place)
        
        if keys[pygame.K_c]:
            level = 2.5

    #Information About Poaching 
    elif (level == 3): 
        screen.blit(level_3_text, information_txt_place)
        screen.blit(lvl_text, lvl_txt_place)
        screen.blit(poacher_text, label_place)
        screen.blit(poacher, image_place)
        
        if keys[pygame.K_c]:
            level = 3.5
            max_poacher = 1

    # game
    else: 

        display_multiple_items(krills)
        display_multiple_items(pollutions) 
        display_multiple_items(poachers)

        hp_bar()
        move_whale()
        checkCollisions()

        screen.blit(whale, whale_rect)
        screen.blit(hp_text, (20, 10))

        if(whale_stop):
            screen.blit(whale_frozen_text_1, (15, 50))
            screen.blit(whale_frozen_text_2, (30, 70))

        place_hearts_x = 350
        for i, heart in enumerate(health_hearts): 
            screen.blit(heart, (place_hearts_x, 10))
            place_hearts_x -= 20

        if ((not len(krills) or not len(pollutions)) and not starting_text):
            spawn_krill(random.randint(0, round(max_krill)), random.uniform(1, speed))
            spawn_pollution(random.randint(0, round(max_pollution)), random.uniform(1, speed))
            spawn_poachers(random.randint(0, round(max_poacher)), random.uniform(1, speed))

    pygame.display.update()
    clock.tick(60)


