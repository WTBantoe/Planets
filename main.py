import pygame
import Planet
import sys
import os

os.chdir(r'C:\Users\92887\Desktop\Projects\Coding\Python\Pygame')

#初始化
pygame.init()
paused = False

#边界尺寸
size = width,height = 1280,800

#背景颜色
background_color = (0,0,0)

#定义帧率
clock = pygame.time.Clock()

#设置窗口
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Planet')
screen.fill(background_color)

#创建星球
planets = []
for i in range(60):
    planets.append(Planet.Planet((1280,800,0)))
planets.append(Planet.Planet((1280,800,0),True,50000,10))

while True:
    for event in pygame.event.get():
        #退出
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #键盘事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    screen.fill(background_color)

    for each in planets:
        pygame.draw.circle(screen, each.color, (int(each.position[0]),int(each.position[1])), int(each.radius), 0)
        if not paused:
            planets = Planet.move(planets)
    
    pygame.display.flip()
    clock.tick(100)