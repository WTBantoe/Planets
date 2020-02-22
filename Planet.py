import pygame
import random
import Defult
import math

def cal_dis(planet_a, planet_b):
    return math.sqrt(pow(planet_a.position[0]-planet_b.position[0],2)+
                     pow(planet_a.position[1]-planet_b.position[1],2)+
                     pow(planet_a.position[2]-planet_b.position[2],2))

def collide(planets):
    fixed = planets.pop()
    for i in range(len(planets)):
        if not planets[i].is_collided:
            for j in range(i+1,len(planets)):
                if not planets[j].is_collided:
                    distance = cal_dis(planets[i],planets[j])
                    if planets[i].radius + planets[j].radius >= distance:
                        if planets[i].mass >= planets[j].mass:
                            planets[j].is_collided = True
                            planets[i].mass = planets[i].mass + planets[j].mass
                            planets[i].radius = pow((pow(planets[i].radius,3)+pow(planets[j].radius,3)),1/3)
                            planets[i].position[0] = (planets[i].position[0] * planets[i].mass + planets[j].position[0] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[i].position[1] = (planets[i].position[1] * planets[i].mass + planets[j].position[1] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[i].position[2] = (planets[i].position[2] * planets[i].mass + planets[j].position[2] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[i].velocity[0] = (planets[i].velocity[0] * planets[i].mass + planets[j].velocity[0] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[i].velocity[1] = (planets[i].velocity[1] * planets[i].mass + planets[j].velocity[1] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[i].velocity[2] = (planets[i].velocity[2] * planets[i].mass + planets[j].velocity[2] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                        else:
                            planets[i].is_collided = True
                            planets[j].mass = planets[i].mass + planets[j].mass
                            planets[j].radius = pow((pow(planets[i].radius,3)+pow(planets[j].radius,3)),1/3)
                            planets[j].position[0] = (planets[i].position[0] * planets[i].mass + planets[j].position[0] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[j].position[1] = (planets[i].position[1] * planets[i].mass + planets[j].position[1] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[j].position[2] = (planets[i].position[2] * planets[i].mass + planets[j].position[2] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[j].velocity[0] = (planets[i].velocity[0] * planets[i].mass + planets[j].velocity[0] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[j].velocity[1] = (planets[i].velocity[1] * planets[i].mass + planets[j].velocity[1] * planets[j].mass) / (planets[i].mass + planets[j].mass)
                            planets[j].velocity[2] = (planets[i].velocity[2] * planets[i].mass + planets[j].velocity[2] * planets[j].mass) / (planets[i].mass + planets[j].mass)
    for each in planets:
        if each.is_collided:
            planets.pop(planets.index(each))
    for each in planets:
        distance = cal_dis(each,fixed)
        if each.radius + fixed.radius >= distance:
            each.is_collided = True
            fixed.mass = each.mass + fixed.mass
            fixed.radius = pow((pow(each.radius,3)+pow(fixed.radius,3)),1/3)
            planets.pop(planets.index(each))
    planets.append(fixed)
    return (planets)

def move(planets):
    collide(planets)
    fixed = planets.pop()
    for each in planets:
        each.force = [0,0,0]
    for i in range(len(planets)-1):
        for j in range(i+1,len(planets)):
            distance = cal_dis(planets[i],planets[j])
            force_num = Defult.G * planets[i].mass * planets[j].mass / (pow(distance,2))
            planets[i].force[0] +=   force_num * (planets[j].position[0] - planets[i].position[0]) / distance
            planets[i].force[1] +=   force_num * (planets[j].position[1] - planets[i].position[1]) / distance
            planets[i].force[2] +=   force_num * (planets[j].position[2] - planets[i].position[2]) / distance
            planets[j].force[0] += (-force_num * (planets[j].position[0] - planets[i].position[0]) / distance)
            planets[j].force[1] += (-force_num * (planets[j].position[1] - planets[i].position[1]) / distance)
            planets[j].force[2] += (-force_num * (planets[j].position[2] - planets[i].position[2]) / distance)
    for each in planets:
        distance = cal_dis(each,fixed)
        force_num = Defult.G * each.mass * fixed.mass / (pow(distance,2))
        each.force[0] += force_num * (fixed.position[0] - each.position[0]) / distance
        each.force[1] += force_num * (fixed.position[1] - each.position[1]) / distance
        each.force[2] += force_num * (fixed.position[2] - each.position[2]) / distance
    for each in planets:
        each.position = [each.position[0] + each.velocity[0] * Defult.TIME_SPAN,
                         each.position[1] + each.velocity[1] * Defult.TIME_SPAN,
                         each.position[2] + each.velocity[2] * Defult.TIME_SPAN]
        each.velocity = [each.velocity[0] + each.force[0] / each.mass * Defult.TIME_SPAN,
                         each.velocity[1] + each.force[1] / each.mass * Defult.TIME_SPAN,
                         each.velocity[2] + each.force[2] / each.mass * Defult.TIME_SPAN]
    planets.append(fixed)
    return (planets)
         


class Planet():

    smallest_mass = 1 #星球的最小质量
    biggest_mass = 100 #星球的最大质量
    smallest_radius = 5 #星球最小半径
    biggest_radius = 10 #星球最大半径
    biggest_velocity = 10 #星球各方向的最大速度
    trail_length = 10 #星球保留的轨迹长度

    def __init__(self,boundry,fix=False,*args):
        if fix == False:
            self.mass = random.uniform(Planet.smallest_mass,Planet.biggest_mass)
            self.radius = random.uniform(Planet.smallest_radius,Planet.biggest_radius)
            self.position = [random.uniform(0,boundry[0]),random.uniform(0,boundry[1]),random.uniform(0,boundry[2])]
            self.velocity = [random.uniform(-Planet.biggest_velocity,Planet.biggest_velocity),
                             random.uniform(-Planet.biggest_velocity,Planet.biggest_velocity),0]
                             #random.uniform(-Planet.biggest_velocity,Planet.biggest_velocity)]
            self.force = [0,0,0]
            self.color = (random.randint(50,255),random.randint(50,255),random.randint(50,255))
            self.trail = []
            self.is_fixed = False
            self.is_collided = False
        else:
            self.mass = args[0]
            self.radius = args[1]
            self.position = [boundry[0]/2,boundry[1]/2,boundry[2]/2]
            self.velocity = [0,0,0]
            self.force = [0,0,0]
            self.color = (random.randint(50,255),random.randint(50,255),random.randint(50,255))
            self.trail = []
            self.is_fixed = True
            self.is_collided = False