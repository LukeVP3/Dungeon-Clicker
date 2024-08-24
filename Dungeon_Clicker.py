import pygame
import sys


# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Clicker")

cursor_img = pygame.image.load("monsters/Target.png").convert_alpha()

#Sound Channels
pygame.mixer.init()
background_music_channel = pygame.mixer.Channel(0)
sound_effects_channel = pygame.mixer.Channel(1)

# Load and play background music
background_music = "sound_and_music/dungeon_music.wav"
background_music_channel.play(pygame.mixer.Sound(background_music), loops=-1)

# Load sound effects
bunny_sound = "sound_and_music/bunny_audio.mp3"
bunny_sound_effect = pygame.mixer.Sound(bunny_sound)
bunny_sound_effect.set_volume(1.0)
cash_sound = "sound_and_music/cash_audio.mp3"
cash_sound_effect = pygame.mixer.Sound(cash_sound)
cash_sound_effect.set_volume(1.0)
loser_sound = "sound_and_music/loser.mp3"
loser_sound_effect = pygame.mixer.Sound(cash_sound)
loser_sound_effect.set_volume(1.0)

#Play Sounds
def play_sound(sound_file):
    sound_effects_channel.play(pygame.mixer.Sound(sound_file))



# Attempt to load the monster image
try:
    slime_frames = [pygame.image.load(f"slime_frames/slime{i}.png") for i in range(1, 10)]
    bat_frames = [pygame.image.load(f"bat_frames/bat{i}.gif") for i in range(1, 6)]
    bomb_frames = [pygame.image.load(f"bomb_frames/bomb{i}.png") for i in range(1, 20)]
    cash_frames = [pygame.image.load(f"cash_frames/cash{i}.png") for i in range(1, 8)]
    bunny_frames = [pygame.image.load(f"bunny_frames/bunny{i}.gif") for i in range(1, 10)]
    cash_still = pygame.image.load(f"cash_frames/cash1.png") 
    bunny_still = pygame.image.load(f"bunny_frames/bunny1.gif") 

    monster_images = [
        slime_frames,
        bat_frames,
        bomb_frames,
    ]
    check = pygame.image.load("monsters/check.png")
    monster_heart = pygame.image.load("monsters/Heart.png")
    monster_sword = pygame.image.load("monsters/Sword.png")
    monster_panel = pygame.image.load("monsters/panel.png")
    monster_panel1 = pygame.image.load("monsters/panel.png")
    monster_panel_mini = pygame.image.load("monsters/panel_mini.png")
    dungeon_background = pygame.image.load("monsters/dungeon.png")
    hero_frames = [pygame.image.load(f"hero_frames/hero{i}.png") for i in range(1, 14)]
    hero_frame_index = 0
    hero_animation_timer = pygame.time.get_ticks()
    hero_animation_interval = 75  # milliseconds between frame changes
    slime_animation_timer = pygame.time.get_ticks()
    slime_animation_interval = 200
    slime_frame_index = 0
    bat_animation_timer = pygame.time.get_ticks()
    bat_animation_interval = 100
    bat_frame_index = 0
    bomb_animation_timer = pygame.time.get_ticks()
    bomb_animation_interval = 50
    bomb_frame_index = 0
    cash_animation_timer = pygame.time.get_ticks()
    cash_animation_interval = 50
    cash_frame_index = 0
    cash_activated = False
    cash_cost = 1500    #How much the cash/money pet cost
    bunny_animation_timer = pygame.time.get_ticks()
    bunny_animation_interval = 50
    bunny_frame_index = 0
    bunny_activated = False
    bunny_cost = 750    #How much the bunny pet cost
    cash_owned = False
    bunny_owned = False



except pygame.error as e:
    print("Error loading image:", e)
    sys.exit()

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 160, 40)
BLUE = (0, 0, 255)
PURPLE = (200, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Variables
monster_width, monster_height = 350, 200
monster_x = ((WIDTH - monster_width) // 2) + 250
monster_y = (HEIGHT - monster_height) // 2 + 50
heart_x = 800
heart_y = 75
hero_x = 200
hero_y = 200
damage_per_click = 10
monster_health = 300 # set to 1 for testing (og # was 300)
pause_duration = 0
score = 0
money = 0
nmh = 0 # New Monster's Health
health = 50 # Player's Health
max_health = 50 #used to reset/upgrade health
upgrade_cost_dmg = 100
upgrade_cost_hp = 100
upgrade_level_dmg = 0
upgrade_level_hp = 0
enemy_level = 1
damage_timer = 0
damage_interval = 1000 #Damage in millieseconds
current_monster_index = 0 #Used to switch monster after killed
countdown_texts = ["3", "2", "1", "Go!"]
countdown_index = 0
countdown_timer = pygame.time.get_ticks()
countdown_interval = 700  # Countdown interval in milliseconds
click_enabled = False
monster_switching = False
cursor_hotspot = (0, 0)

# Fonts
font_new = "monsters/monster_font.ttf"
font = pygame.font.Font(font_new, 11)
font_lar = pygame.font.Font(font_new, 15)
font_gg = pygame.font.Font(font_new, 30)
font_countdown = pygame.font.Font(font_new, 150)

# Functions
# Functions
def draw_text(text, font_lar, color, x, y):
    surface = font_lar.render(text, True, color)
    screen.blit(surface, (x, y))

def switch_monster_image():
    global current_monster_index
    current_monster_index = (current_monster_index + 1) % len(monster_images)
    if current_monster_index > 2:
        current_monster_index = 0

def deal_damage():
    global health, enemy_level
    if click_enabled == False:
        health -= 0
    elif click_enabled == True:
        health -= enemy_level  # Adjust damage amount as needed
def cash_pet():
    global money
    money += 100
def bunny_pet(): #monty is the name of the bunny
    global monster_health, score, money
    monster_health -= int(damage_per_click * 1.5)
    score += int(damage_per_click * 1.5)
    money += int(damage_per_click * 0.5)



# Set up timer event for monster's damage
pygame.time.set_timer(pygame.USEREVENT, damage_interval)

def upgrade_damage():
    global damage_per_click, money, upgrade_level_dmg, upgrade_cost_dmg
    upgrade_cost_dmg = 100 * (upgrade_level_dmg + 1)  # Cost to upgrade damage per click increases with each upgrade
    if money >= upgrade_cost_dmg:
        damage_per_click += 5  # Increase damage per click by 10
        money -= upgrade_cost_dmg  # Deduct upgrade cost from money
        upgrade_level_dmg += 1  # Increment upgrade level
        print("Damage per click upgraded to:", damage_per_click)
        print("Upgrade level:", upgrade_level_dmg)
        print("Upgrade cost:", upgrade_cost_dmg)
    else:
        print("Insufficient funds to upgrade damage per click!")

def upgrade_health():
    global upgrade_level_hp, money, health, max_health, upgrade_cost_hp
    upgrade_cost_hp = 100 * (upgrade_level_hp + 1)  # Cost to upgrade damage per click increases with each upgrade
    if money >= upgrade_cost_hp:
        max_health += 10  # Increase damage per click by 10
        health = max_health
        money -= upgrade_cost_hp  # Deduct upgrade cost from money
        upgrade_level_hp += 1  # Increment upgrade level
        print("Health Upgraded to:", max_health)
        print("Upgrade level:", upgrade_level_hp)
        print("Upgrade cost:", upgrade_cost_hp)
    else:
        print("Insufficient funds to upgrade damage per click!")
        

heart_button_rect = pygame.Rect(heart_x+20, heart_y, monster_heart.get_width()+50, monster_heart.get_height()+50) #Button used to upgrade health
sword_button_rect = pygame.Rect(heart_x-480, heart_y+20, monster_sword.get_width(), monster_sword.get_height()) #Button used to upgrade attack
bunny_button_rect = pygame.Rect(30, 200, bunny_frames[1].get_width(), bunny_frames[0].get_height())
cash_button_rect = pygame.Rect(30, 325, cash_frames[1].get_width(), cash_frames[0].get_height())

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
             if event.button == 1 and click_enabled and not monster_switching:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if monster_x <= mouse_x <= monster_x + monster_width and monster_y <= mouse_y <= monster_y + monster_height:
                    monster_health -= damage_per_click
                    score += damage_per_click
                    money += damage_per_click

                elif heart_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Button clicked!")  # For demonstration purposes
                    upgrade_health()
                elif sword_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Button clicked!")  # For demonstration purposes
                    upgrade_damage()
                elif cash_button_rect.collidepoint(mouse_x, mouse_y) and not cash_activated and money >= cash_cost:
                    print("Bought cash!")  # For demonstration purposes
                    bunny_activated = False
                    cash_activated = True
                    play_sound(cash_sound)
                    if cash_owned == False:
                        money -= cash_cost
                        cash_owned = True
                        
                    elif cash_owned == True:
                        cash_activated = True
                elif bunny_button_rect.collidepoint(mouse_x, mouse_y) and not bunny_activated and money >= bunny_cost:
                    print("Bought bunny!")  # For demonstration purposes
                    cash_activated = False
                    bunny_activated = True
                    if bunny_owned == False:
                        money -= bunny_cost
                        bunny_owned = True
                        play_sound(bunny_sound)
                    elif bunny_owned == True:
                        bunny_activated = True

    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Calculate the elapsed time minus the pause duration
    elapsed_time = current_time - pause_duration

    if countdown_index < len(countdown_texts):
        if current_time - countdown_timer >= countdown_interval:
            countdown_timer = current_time
            countdown_index += 1
            if countdown_index == len(countdown_texts):
                click_enabled = True

    if elapsed_time - damage_timer >= damage_interval:
        deal_damage()
        damage_timer = elapsed_time
        if cash_activated:
            cash_pet()
        if bunny_activated:
            damage_timer = elapsed_time + 500
            bunny_pet()
        if monster_switching:
            monster_switching = False

    #if elapsed_time - damage_timer >= damage_interval:
        #damage_timer = elapsed_time + 500
  
    # Clear the screen
    screen.fill(BLACK) 

    # Draw game elements
    screen.blit(dungeon_background, (0, 0))
    screen.blit(monster_sword, ((heart_x-460), heart_y+20))
    screen.blit(monster_heart, (heart_x+25, heart_y+25))
    screen.blit(monster_panel, ((heart_x-480), heart_y))
    screen.blit(monster_panel1, (heart_x, heart_y))
    screen.blit(cash_still, (30, 325))
    screen.blit(bunny_still, (30, 200))
    screen.blit(monster_panel_mini, (30, 200))
    screen.blit(monster_panel_mini, (30, 325))
    if cash_activated:
        screen.blit(check, (40, 325))
    if bunny_activated:
        screen.blit(check, (40, 200))
    
    #animate the hero
    if current_time - hero_animation_timer >= hero_animation_interval:
        hero_frame_index = (hero_frame_index + 1) % len(hero_frames)
        hero_animation_timer = current_time
    screen.blit(hero_frames[hero_frame_index], (hero_x, hero_y))

    #animate cash pet
    if cash_activated:
        if current_time - cash_animation_timer >= cash_animation_interval:
            cash_frame_index = (cash_frame_index + 1) % len(cash_frames)
            cash_animation_timer = current_time
        screen.blit(cash_frames[cash_frame_index], (hero_x, hero_y+100))

    #animate da bunny
    if bunny_activated:
        if current_time - bunny_animation_timer >= bunny_animation_interval:
            bunny_frame_index = (bunny_frame_index + 1) % len(bunny_frames)
            bunny_animation_timer = current_time
        screen.blit(bunny_frames[bunny_frame_index], (hero_x, hero_y+250))

    # Animate the slime
    if current_monster_index == 0:  # Slime
        if current_time - slime_animation_timer >= slime_animation_interval:
            slime_frame_index = (slime_frame_index + 1) % len(slime_frames)
            slime_animation_timer = current_time
        screen.blit(slime_frames[slime_frame_index], (monster_x, monster_y))
    # Animate the bat
    elif current_monster_index == 1:  # Bat
        if current_time - bat_animation_timer >= bat_animation_interval:
            bat_frame_index = (bat_frame_index + 1) % len(bat_frames)
            bat_animation_timer = current_time
        screen.blit(bat_frames[bat_frame_index], (monster_x, monster_y))
    # Animate the bomb
    elif current_monster_index == 2: # Bomb
        if current_time - bomb_animation_timer >= bomb_animation_interval:
            bomb_frame_index = (bomb_frame_index + 1) % len(bomb_frames)
            bomb_animation_timer = current_time
        screen.blit(bomb_frames[bomb_frame_index], (monster_x+30, monster_y-30))
    #Starting countdown
    if countdown_index < len(countdown_texts):
        countdown_surface = font_countdown.render(countdown_texts[countdown_index], True, RED)
        countdown_rect = countdown_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(countdown_surface, countdown_rect)
    
    draw_text("Monster Health: " + str(max(0, monster_health)), font_lar, PURPLE, 10, 10)
    draw_text("Score: " + str(score), font_lar, BLUE, 10, 60)
    draw_text("Money: " + str(money), font_lar, GREEN, 10, 110)
    draw_text("Player Health: " + str(health), font_lar, RED, 900, 10)

    # Update upgrade cost
    upgrade_cost_hp = 100 * (upgrade_level_hp + 1)
    draw_text("Upgrade Cost: " + str(upgrade_cost_hp), font_lar, YELLOW, heart_x-70, heart_y+100)
    upgrade_cost_dmg = 100 * (upgrade_level_dmg + 1)
    draw_text("Upgrade Cost: " + str(upgrade_cost_dmg), font_lar, YELLOW, heart_x-540, heart_y+100)

    if bunny_owned == False:
        draw_text("Pet Cost: " + str(bunny_cost), font, YELLOW, 15, 280)
    elif bunny_owned == True:
        draw_text("Bought!", font, YELLOW, 30, 280)
    if cash_owned == False:
        draw_text("Pet Cost: " + str(cash_cost), font, YELLOW, 15, 410)
    elif cash_owned == True:
        draw_text("Bought!", font, YELLOW, 30, 410)

    screen.blit(cursor_img, (mouse_x - cursor_hotspot[0], mouse_y - cursor_hotspot[0]))

    if monster_health <= 0:
        draw_text("You defeated the monster!", font_lar, GREEN, 700, 250)
        score += 100
        pause_start_time = pygame.time.get_ticks()
        pygame.display.update()
        pygame.time.wait(1500)
        pause_end_time = pygame.time.get_ticks()
        pause_duration += pause_end_time - pause_start_time
        enemy_level += 2
        nmh += 100 # for testing (og # was 100)
        monster_health = 300 + nmh #for testing (og # was 300)
        money += int(nmh / 2)
        monster_switching = True
        switch_monster_image()
        if current_monster_index == 1:
            monster_y = monster_y-20
            monster_x = monster_x+30
        if current_monster_index == 2:
            monster_y = monster_y+60
            monster_x = monster_x+30
        if current_monster_index == 0:
            monster_x = ((WIDTH - monster_width) // 2) + 250
            monster_y = (HEIGHT - monster_height) // 2 + 50

    if health <= 0:
        screen.fill(BLACK)
        background_music_channel.stop()
        play_sound(loser_sound)
        draw_text("Game Over!", font_gg, RED, 450, 300)
        pause_start_time = pygame.time.get_ticks()
        pygame.display.update()
        pygame.time.wait(5000)
        pause_end_time = pygame.time.get_ticks()
        pause_duration += pause_end_time - pause_start_time
        running = False

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
