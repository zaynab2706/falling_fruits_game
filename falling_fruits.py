import pygame
import random
pygame.init()


width, height=800,600
basket_w, basket_h=120,30
basket_Y_offset, basket_speed, basket_color =50,8,(255,75,0)
fruit_y,fruit_c, fruit_r,fruit_speed = 0,(255,0,0),20,5
white, black, bg_color=(255,255,255), (0,0,0) ,(135,206,235)
num_fruits=5

screen= pygame.display.set_mode((width,height))
pygame.display.set_caption("Falling Fruits")
clock=pygame.time.Clock()

basket_x= width//2 -basket_w//2
basket_y= height - basket_Y_offset

fruits=[]
for _ in range(num_fruits):
    x=random.randint(fruit_r, width -fruit_r)
    y=random.randint(-300,0)
    fruits.append([x,y])

score =0
font=pygame.font.SysFont("Arial",36)


running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket_x -= basket_speed
    
    if keys[pygame.K_RIGHT]:
        basket_x += basket_speed
    
    basket_x = max(0,min(width-basket_w,basket_x))
    for fruit in fruits:
        fruit[1]+=fruit_speed
        basket_rect=pygame.Rect(basket_x,basket_y,basket_w,basket_h)
        fruit_rect=pygame.Rect(fruit[0]-fruit_r,fruit[1]-fruit_r,fruit_r*2,fruit_r*2)
        
        if basket_rect.colliderect(fruit_rect):
            score+=1
            fruit[1]=0
            fruit[0]=random.randint(fruit_r,width-fruit_r)
        if fruit[1] -fruit_r > height:
            fruit[1]=0
            fruit[0]=random.randint(fruit_r,width-fruit_r)

    screen.fill(bg_color)
    pygame.draw.rect(screen, basket_color, (basket_x, basket_y, basket_w, basket_h) )
    for fruit in fruits:
        pygame.draw.circle(screen,fruit_c,(fruit[0],fruit[1]),fruit_r)

    score_test=font.render(f"Score={score}",True,black)
    screen.blit(score_test,(10,10))
    pygame.display.flip()
pygame.quit()
