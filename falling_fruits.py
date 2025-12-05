import pygame
import random
import os
from intro import show_intro_screen  

pygame.init()

#Settings
width, height = 1000, 600

basket_w, basket_h = 120, 30
basket_Y_offset = 50
basket_speed = 8

fruit_r = 20           
fruit_speed = 5
num_fruits = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (135, 206, 235)
BASKET_COLOR = (255, 75, 0)


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


basket_img = load_image("C:/Users/DATA/Documents/Documents/f_f_game/basket.png", (basket_w, basket_h))

fruit_imgs = [
    load_image("C:/Users/DATA/Documents/Documents/f_f_game/apple.png", (fruit_r * 2, fruit_r * 2)),
    load_image("C:/Users/DATA/Documents/Documents/f_f_game/banana.png", (fruit_r * 2, fruit_r * 2)),
    load_image("C:/Users/DATA/Documents/Documents/f_f_game/orange.png", (fruit_r * 2, fruit_r * 2)),
]


screen = pygame.display.set_mode((width, height))
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
font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 64, bold=True)
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
    txt = title_font.render(title, True, WHITE)
    shadow = title_font.render(title, True, (0, 0, 0))
    tx_rect = txt.get_rect(center=(width // 2, 40))
    screen.blit(shadow, (tx_rect.x + 2, tx_rect.y + 2))
    screen.blit(txt, tx_rect)
    #subtitles
    sub = subtitle_font.render(subtitle, True, BLACK)
    sub_rect = sub.get_rect(center=(width // 2, 90))
    screen.blit(sub, sub_rect)

#essential loop
running = True
while running:
    dt = clock.tick(60) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT]:
        basket_x += basket_speed

    
    basket_x = max(0, min(width - basket_w, basket_x))

    
    basket_rect = pygame.Rect(basket_x, basket_y, basket_w, basket_h)
    for fruit in fruits:
        fruit[1] += fruit_speed
        fruit_rect = pygame.Rect(fruit[0] - fruit_r, fruit[1] - fruit_r, fruit_r * 2, fruit_r * 2)

        
        if basket_rect.colliderect(fruit_rect):
            score += 1
            respawn_fruit(fruit)

        
        if fruit[1] - fruit_r > height:
            respawn_fruit(fruit)

    
    screen.fill(BG_COLOR)

    draw_title()

    screen.blit(basket_img, (basket_x, basket_y))

    for fruit in fruits:
        img = fruit_imgs[fruit[2]]
        screen.blit(img, (fruit[0] - fruit_r, fruit[1] - fruit_r))

    score_surf = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_surf, (10, 10))

    pygame.display.flip()

pygame.quit()

