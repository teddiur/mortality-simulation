import pygame
import random
import math
import numpy as np
import os

class Vector(object):
    def __init__(self, x1, x2):
        self.vector = [x1, x2]
        self._x = x1
        self._y = x2

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, x):
        self._x = x
        self.vector[0] = x

    @y.setter
    def y(self, y):
        self._y = y
        self.vector[1] = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def dot(self, other):
        ans = 0
        for i in range(len(self.vector)):
            ans += self.vector[i]*other.vector[i]
        return ans

    def __str__(self):
        ans = '['
        for i in (self.vector):
            ans += f'{i}, '
        ans = ans[:-2] + ']'
        return ans

    def distance(self, other):
        dist = self - other
        ans = math.sqrt(dist.x**2 + dist.y**2)
        return ans
    
    def mult(self, scalar):
        x = self.x * scalar
        y = self.y * scalar
        return Vector(x, y)


class Particle(object):
    """Atributes: position (x, y) -> Vector
    size -> int, default 7
    thickness -> int, default 1
    speed (vx, vy)-> Vector 
    """
    color = {'ok': (0,0,255), 'ill': (255,0,0), 'recovered': (0,255,0), 'dead': (0, 0, 0)}
    def __init__(self, position, speed, size=7, state='ok'):
        self.pos = position
        self.speed = speed
        self.size = size
        self.color = Particle.color[state]
        self.state = state

    def update_color(self, state):
        #iniate a timer if the person wasn't infected but it's now
        self.infected(state)
        self.state = state
        self.color = Particle.color[state]
        
    def infected(self, state):
        if self.state != 'ill' and state == 'ill':
            self.time_infected = 0

    def timer(self):
        if self.state == 'ill':
            self.time_infected += 1
            self.death()

    def death(self):
        if self.time_infected > TIME_TILL_DEAD:
            self.update_color('dead')
            self.speed.x = self.speed.y = 0

    def display(self):
        #creates a circle with its color, position, size and thickness
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.size, 0)
        
    def update(self):
        if self.state == 'dead':
            return
        
        #right boundary
        if self.pos.x + self.size > simulation_x1:
            self.speed.x *= -1
            self.pos.x = 2 * simulation_x1 - self.pos.x
        #left boundary
        elif self.pos.x - self.size < simulation_x0:
            self.speed.x *= -1
            self.pos.x = simulation_x0 + self.size - self.pos.x
        #bottom boundary
        if self.pos.y + self.size > simulation_y1:
            self.speed.y *= -1
            self.pos.y = 2 * simulation_y1 - self.pos.y
        #top boundary
        elif self.pos.y - self.size < simulation_y0:
            self.speed.y *= -1
            self.pos.y = simulation_y0 + self.size - self.pos.y
        self.pos = self.pos + self.speed

    def overlaps(self, other):
        distance = self.pos.distance(other.pos)
        return distance < self.size + other.size

    def colision(self, other):        
        pos11 = self.pos
        # pos12 = self.pos
        vel11 = self.speed
        # vel12 = self.speed
        pos_dif = self.pos - other.pos
        vel_dif = self.speed - other.speed

        factor = vel_dif.dot(pos_dif)
        factor /= pos_dif.distance(ORIGIN) ** 2
        self.speed = self.speed - pos_dif.mult(factor)

        pos_dif = other.pos - pos11
        vel_dif = other.speed - vel11

        factor = pos_dif.dot(vel_dif)
        factor /= pos_dif.distance(ORIGIN) ** 2
        other.vel = other.speed - pos_dif.mult(factor)
        
        while self.overlaps(other):
            self.update()
            other.update()
                
        #contamination
        if all([(self.state == 'ill' or other.state == 'ill'), (self.state != 'dead' and other.state != 'dead')]):
            self.update_color('ill')
            other.update_color('ill')


def count(particles):
    dict = {}
    for element in particles:
        dict[element.state] = dict.get(element.state, 0) + 1
    return [dict.get('ok', 0), dict.get('ill', 0), dict.get('recovered', 0), dict.get('dead', 0)]

(window_width, window_heigth) = (615, 815)
(width_simulation, heigth_simulation) = (600, 600)
simulation_x0 = 7
simulation_x1 = simulation_x0 + width_simulation
simulation_y0 = 207
simulation_y1 = simulation_y0 + heigth_simulation
BG_COLOR = (255, 255, 255)
TIME_TILL_DEAD = 3000
ORIGIN = Vector(simulation_x0, simulation_y0)

#creates a Surface and color it
screen = pygame.display.set_mode((window_width, window_heigth))

number_particles = 20
particles = []

#creates the particles in random locations and infects one of them
for i in range(number_particles):
    #a good pratice would be checking if there's already a Particle in this (x,y)
    size = 7
    x = random.randint(simulation_x0 + size, simulation_x1 - size)
    y = random.randint(simulation_y0 + size, simulation_y1 - size)
    vx = random.uniform(0, 0.3)
    vy = math.sqrt(0.3**2-vx**2)*(-1)**x

    pos = Vector(x, y)
    speed = Vector(vx, vy)
    
    particle = Particle(pos, speed)
    particles.append(particle)
    
    if i == number_particles-1:
        particles[-1].update_color('ill')

#set a name
pygame.display.set_caption('Infection Simulation')


#makes so the program runs indefinitely but quits when it's asked to close
limit = 1*1
j = 0
#counter: time, suscetible, infectious, recovered, dead
counter = np.array([j] + count(particles))
# while running:
while j < limit:
    #display the particles
    screen.fill(BG_COLOR)

    #quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            j = limit + 1

    pygame.draw.rect(screen, (0,0,0), (simulation_x0, simulation_y0, width_simulation, heigth_simulation), 1)
    #the most time consuming part 
    for i, particle in enumerate(particles):
        if particle.state == 'dead':
            particle.display()
            continue
        for particle2 in particles[i+1:]:
            if particle.overlaps(particle2):
                particle.colision(particle2)
        particle.update()
        particle.timer()
        particle.display()
    # pygame.display.flip()
    counter = np.append(counter, [j] + count(particles), axis = 0)
    if j == 0:
        counter = np.reshape(counter, (2,5))
    print(counter)

    name = 'simulation' + '0'*(10-len(str(j))) + str(j) + '.jpeg'
    pygame.image.save(screen, name)
    j += 1

# print('simulation done')
# os.system('python3 gif_maker.py')
# print('done')