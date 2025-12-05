import pygame
import os
import sys


def load_gif_frames(folder):
    frames = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, filename))
            frames.append(img)
    return frames

def show_intro_screen(screen,clock,bg_c,black):
    yellow = (255, 215, 0)
    purple= (148,0,211)
    width, height = screen.get_size()
    frames = load_gif_frames("C:/Users/DATA/Documents/Documents/f_f_game/framesfolder")
    if not frames:
        raise RuntimeError("Aucune frame trouvée ! Vérifie le dossier et les fichiers PNG")

    # Fonts
    font_title = pygame.font.SysFont("Comic Sans MS", 70, bold=True)
    font_sub = font_sub = pygame.font.SysFont("Comic Sans MS", 36)

    # Text surfaces
    title_shadow = font_title.render("Falling Fruits" , True, black)
    title_surf = font_title.render("Falling Fruits ", True, yellow)
    subtitle1_surf = font_sub.render("Let's make some juice!", True, purple)
    subtitle2_surf = font_sub.render("Press any key to begin...", True, purple)

    # Rects for centering
    title_rect = title_surf.get_rect(center=(width//2, 150))
    subtitle1_rect = subtitle1_surf.get_rect(center=(width//2, 250))
    subtitle2_rect = subtitle2_surf.get_rect(center=(width//2, 350))

    frame_index = 0
    frame_timer = 0
    frame_interval = 1/12

    blink_timer = 0
    intro = True

    while intro:
        dt = clock.tick(60) / 1000.0
        frame_timer += dt
        blink_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                intro = False

        # gif 
        if frame_timer >= frame_interval:
            frame_timer -= frame_interval
            frame_index = (frame_index + 1) % len(frames)

        # frame drawing
        frame = frames[frame_index]
        frame_rect = frame.get_rect(center=(width//2, height//2))
        screen.blit(frame, frame_rect)
        screen.blit(title_shadow, title_rect.move(3, 3))
        screen.blit(title_surf, title_rect)
        screen.blit(subtitle1_surf, subtitle1_rect)

        # clignotement 
        if (blink_timer % 1.2) < 0.8:
            screen.blit(subtitle2_surf, subtitle2_rect)

        pygame.display.flip()
