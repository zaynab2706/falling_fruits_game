import pygame
import random
import os
import math
from intro import show_intro_screen  

pygame.init()

#Settings
width, height = 1000, 600

basket_w, basket_h = 120, 60
basket_Y_offset = 50
basket_speed = 8
basket_velocity = 0
basket_acceleration = 1
basket_max_speed = 10
basket_friction = 0.85


fruit_r = 20           
fruit_speed = 5
num_fruits = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (135, 206, 235)
BASKET_COLOR = (255, 75, 0)
YELLOW = (255, 215, 0)
PURPLE= (148,0,211)


def load_image(path, size=None):
    img = pygame.image.load(path)  
    if pygame.display.get_surface() is not None:
        try:
            img = img.convert_alpha()
        except Exception:
            try:
                img = img.convert()
            except Exception:
                pass
    else:
        pass

    if size:
        img = pygame.transform.smoothscale(img, size)
    return img

def draw_shadow(screen, x, y, r):
    shadow = pygame.Surface((r*2, r), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0,0,0,80), shadow.get_rect())
    screen.blit(shadow, (x-r, y-r//2 + 10))

def draw_score(screen, score, font):
    text = font.render(f"Score: {score}", True, (0,0,0))
    padding = 12
    box = pygame.Surface((text.get_width()+padding*2, text.get_height()+padding*2), pygame.SRCALPHA)

    pygame.draw.rect(box, (0,0,0,60), (4,4, box.get_width(), box.get_height()), border_radius=12)

    pygame.draw.rect(box, (255,255,255,230), (0,0,box.get_width(),box.get_height()), border_radius=12)
    box.blit(text, (padding, padding))

    screen.blit(box, (20, 20))


basket_img = load_image("C:/Users/DATA/Documents/Documents/f_f_game/basket.png", (basket_w, basket_h))

fruit_imgs = [
    load_image("C:/Users/DATA/Documents/Documents/f_f_game/apple.png", (fruit_r * 2, fruit_r * 2)),
    load_image("C:/Users/DATA/Documents/Documents/f_f_game/banana.png", (fruit_r * 2, fruit_r * 2)),
    load_image("C:/Users/DATA/Documents/Documents/f_f_game/orange.png", (fruit_r * 2, fruit_r * 2)),
]


screen = pygame.display.set_mode((width, height))

# Sound & Music setup 
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    print("Mixer initialized:", pygame.mixer.get_init())
except Exception as e:
    print("Warning: mixer failed to initialize:", e)

# volume control
SFX_VOLUME = 0.7   
MUSIC_VOLUME = 0.5 

# sound effects loading
def load_sound(path):
    if not os.path.exists(path):
        print("Sound file not found:", path)
        return None
    try:
        snd = pygame.mixer.Sound(path)
        return snd
    except Exception as e:
        print("Error loading sound", path, ":", e)
        return None

# Load SFX
catch_sfx = load_sound("catch.mp3")
miss_sfx  = load_sound("miss.mp3")
gameover_sfx=load_sound("game_over.mp3")

#volume settings
if catch_sfx:
    catch_sfx.set_volume(SFX_VOLUME)
if miss_sfx:
    miss_sfx.set_volume(SFX_VOLUME)

def play_bgm(path="bgm.ogg", loop=-1, fade_ms=800):
    if not os.path.exists(path):
        print("BGM not found:", path)
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(loop, 0.0)
        print("BGM playing:", path)
    except Exception as e:
        print("Error playing BGM", path, ":", e)

def stop_bgm(fade_ms=500):
    try:
        pygame.mixer.music.fadeout(fade_ms)
    except Exception as e:
        print("Error stopping BGM:", e)


play_bgm("bg_music.mp3")

muted = False
prev_sfx_vol = SFX_VOLUME
prev_mus_vol = MUSIC_VOLUME
game_over = False
fade_in = False
fade_start = 0
fade_alpha = 0

def format_time(seconds):
    s = max(0, int(round(seconds)))
    mins = s // 60
    secs = s % 60
    return f"{mins:02d}:{secs:02d}"

def draw_timer(surface, time_left, font, x=None, y=20):
    txt = format_time(time_left)
    if time_left <= TIMER_WARNING_SECONDS:
        color = (220, 50, 50) 
        pulse = (1 + 0.2 * math.sin(pygame.time.get_ticks() * 0.01))
    else:
        color = (0, 0, 0)
        pulse = 1.0

    timer_surf = font.render(txt, True, color)
    if pulse != 1.0:
        sw = pygame.transform.rotozoom(timer_surf, 0, pulse)
    else:
        sw = timer_surf

    if x is None:
        x = surface.get_width() - sw.get_width() - 20
    surface.blit(sw, (x, y))


pygame.display.set_caption("Falling Fruits")
clock = pygame.time.Clock()


basket_x = width // 2 - basket_w // 2
basket_y = height - basket_Y_offset


fruits = []
for _ in range(num_fruits):
    x = random.randint(fruit_r, width - fruit_r)
    y = random.randint(-300, -fruit_r)  
    img_index = random.randrange(len(fruit_imgs))
    fruits.append([x, y, img_index])

score = 0
font = pygame.font.SysFont("Comic Sans MS", 36)
title_font = pygame.font.SysFont("Comic Sans MS", 64, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 28)


try:
    show_intro_screen(screen, clock, "C:/Users/DATA/Documents/Documents/f_f_game/framesfolder", BLACK)
except Exception as e:
    
    print("show_intro_screen skipped / failed:", e)


def respawn_fruit(fruit):
    fruit[0] = random.randint(fruit_r, width - fruit_r)
    fruit[1] = random.randint(-300, -fruit_r)
    fruit[2] = random.randrange(len(fruit_imgs))

def draw_title():
    title = "Falling Fruits"
    subtitle = "Use ← → to move the basket — Catch the fruits!"
    txt = title_font.render(title, True, YELLOW)
    shadow = title_font.render(title, True, (0, 0, 0))
    tx_rect = txt.get_rect(center=(width // 2, 40))
    screen.blit(shadow, (tx_rect.x + 2, tx_rect.y + 2))
    screen.blit(txt, tx_rect)
    #subtitles
    sub = subtitle_font.render(subtitle, True, PURPLE)
    sub_rect = sub.get_rect(center=(width // 2, 90))
    screen.blit(sub, sub_rect)

# Timer config 
GAME_TIME_SECONDS = 60
time_left = GAME_TIME_SECONDS * 1.0 

# visual timer settings
timer_font = pygame.font.SysFont("Comic sans Ms", 36, bold=True)
TIMER_WARNING_SECONDS = 10  

#essential loop
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input 
    keys = pygame.key.get_pressed()
    if not game_over:
        # basket input 
        if keys[pygame.K_LEFT]:
            basket_velocity -= basket_acceleration
        if keys[pygame.K_RIGHT]:
            basket_velocity += basket_acceleration

        basket_velocity = max(-basket_max_speed, min(basket_max_speed, basket_velocity))
        basket_x += basket_velocity
        basket_velocity *= basket_friction
        basket_x = max(0, min(width - basket_w, basket_x))

        # UPDATE fruits & collisions 
        basket_rect = pygame.Rect(basket_x, basket_y, basket_w, basket_h)
        for fruit in fruits:
            fruit[1] += fruit_speed
            fruit_rect = pygame.Rect(fruit[0] - fruit_r, fruit[1] - fruit_r, fruit_r * 2, fruit_r * 2)

            if basket_rect.colliderect(fruit_rect):
                score += 1
                if catch_sfx and not muted:
                    try:
                        catch_sfx.play()
                    except Exception as e:
                        print("Failed to play catch_sfx:", e)
                respawn_fruit(fruit)

            elif fruit[1] - fruit_r > height:
                if miss_sfx and not muted:
                    try:
                        miss_sfx.play()
                    except Exception as e:
                        print("Failed to play miss_sfx:", e)
                respawn_fruit(fruit)

    # TIMER update 
    dt_seconds = dt / 1000.0
    if not game_over:
        time_left -= dt_seconds
        if time_left <= 0:
            time_left = 0
            game_over = True

            # fade music
            try:
                if pygame.mixer.get_init():
                    pygame.mixer.music.fadeout(800)
            except Exception as e:
                print("Warning music fadeout:", e)

            # play gameover sfx 
            try:
                if gameover_sfx and not muted:
                    gameover_sfx.play()
            except Exception as e:
                print("Warning playing gameover_sfx:", e)


            
            fade_in = True
            fade_start = pygame.time.get_ticks()
            fade_alpha = 0

    #drawing
    screen.fill(BG_COLOR)
    draw_title()
    screen.blit(basket_img, (basket_x, basket_y))

    for idx, fruit in enumerate(fruits):
        offset_x = math.sin(fruit[1] * 0.05) * 3
        draw_shadow(screen, fruit[0], fruit[1], fruit_r)
        img = fruit_imgs[fruit[2]]
        screen.blit(img, (fruit[0] - fruit_r + offset_x, fruit[1] - fruit_r))

    draw_score(screen, score, font)
    draw_timer(screen, time_left, timer_font)


    if game_over:
        # calcul du alpha du fade
        if fade_in:
            elapsed = pygame.time.get_ticks() - fade_start
            fade_alpha = min(255, int((elapsed / 700) * 255))
            if fade_alpha >= 255:
                fade_in = False

        # overlay sombre
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(180 * (fade_alpha/255))))
        screen.blit(overlay, (0,0))

        # texte Game Over
        go_font = pygame.font.SysFont("Arial", 64, bold=True)
        go_surf = go_font.render("Time's up!", True, (255,255,255))
        screen.blit(go_surf, go_surf.get_rect(center=(width//2, height//2 - 40)))

        sub = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(sub, sub.get_rect(center=(width//2, height//2 + 20)))

        hint = subtitle_font.render("Press R to restart or Q to quit", True, (255,255,255))
        screen.blit(hint, hint.get_rect(center=(width//2, height//2 + 70)))

        if keys[pygame.K_r]:
            score = 0
            time_left = GAME_TIME_SECONDS
            game_over = False
            fade_in = False
            fade_alpha = 0
            for f in fruits:
                respawn_fruit(f)
            play_bgm("bg_music.mp3")
        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()

pygame.quit()


