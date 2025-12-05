import pygame
def show_intro_screen(screen,clock,bg_c,black):
    intro=True
    font_1= pygame.font.SysFont(None,60)
    font_2= pygame.font.SysFont(None,36)
    title=font_1.render("🍹 Falling Fruits 🍎", True, black)
    subtitle=font_2.render()

