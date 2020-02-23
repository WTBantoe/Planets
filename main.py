import pygame
import Planet
import sys
import os
import copy
import Defult

os.chdir(r'C:\Users\92887\Desktop\Projects\Coding\Python\Pygame')

#初始化
pygame.init()
paused = False

#边界尺寸
size = x,y,z = 1280,800,0

#背景颜色
background_color = (0,0,0)

#定义帧率
clock = pygame.time.Clock()

#设置窗口
screen = pygame.display.set_mode(size[:2])
pygame.display.set_caption('Planet')
screen.fill(background_color)

#创建星球
planets = []
for i in range(50):
    planets.append(Planet.Planet(size))
planets.append(Planet.Planet(size,True,50000,10))

#星球的副本，用于绘制
planets_copy = copy.deepcopy(planets)

#指定视角
angle = 'z'
if z == 0:
    portion_x = 1
    portion_y = y/x
else:
    portion_x = min(1,x/z)
    portion_y = min(y/x,x/z)

#定义排序函数
def sort_by_direction(item):
    if angle == 'x':
        return item.position[0]
    elif angle == 'y':
        return (-item.position[1])
    elif angle == 'z':
        return (-item.position[2])

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
            elif event.key == pygame.K_x:
                angle = 'x'
            elif event.key == pygame.K_y:
                angle = 'y'
            elif event.key == pygame.K_z:
                angle = 'z'

    screen.fill(background_color)
    planets_copy.sort(key=sort_by_direction)

    for each in planets_copy:
        if angle == 'x':
            pygame.draw.circle(screen, each.color, (int(each.position[2]*portion_x),int(each.position[1]*portion_x)), int(each.radius*portion_x), 0)
            pygame.draw.lines(screen, each.color, 0, list(map(lambda item:(item[2]*portion_x,item[1]*portion_x),each.trail)), 1)
        elif angle == 'y':
            pygame.draw.circle(screen, each.color, (int(each.position[2]*portion_y),int(each.position[0]*portion_y)), int(each.radius*portion_y), 0)
            pygame.draw.lines(screen, each.color, 0, list(map(lambda item:(item[2]*portion_y,item[0]*portion_y),each.trail)), 1)
        elif angle == 'z':
            pygame.draw.circle(screen, each.color, (int(each.position[0]),int(each.position[1])), int(each.radius), 0)
            pygame.draw.lines(screen, each.color, 0, list(map(lambda item:(item[0],item[1]),each.trail)), 1)
        if not paused:
            planets = Planet.move(planets)
            planets_copy = copy.deepcopy(planets)
            
    
    pygame.display.flip()
    clock.tick(int(1/Defult.TIME_SPAN))