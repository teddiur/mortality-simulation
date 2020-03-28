import pygame
import random
import math
import numpy

class Vector(object):
    def __init__(self, x, y):
        self.vector = [x, y]

    def __add__(self, other):
        ans = []
        for i in range(len(self.vector)):
            ans.append(self.vector[i]+other.vector[i])
        return ans

    def __sub__(self, other):
        ans = []
        for i in range(len(self.vector)):
            ans.append(self.vector[i]-other.vector[i])
        return ans
        
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
class Particle(object):
    """Atributes: position (x, y) -> int
    size -> int or float
    color -> tuple, default (0, 0, 255)
    thickness -> int, default 1
    speed -> int or float
    angle -> int or float
    """
    color = {'ok': (0,0,255), 'ill': (255,0,0), 'recovered': (0,255,0), 'dead': (0, 0, 0)}
    def __init__(self, x, y, size, state='ok'):
        self.x = x
        self.y = y
        self.size = size
        self.color = Particle.color[state]
        self.speed = 0.1
        self.angle = 0
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
            self.speed = 0

    def display(self):
        #creates a circle with its color, position, size and thickness
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, 0)
        
    def move(self):
        self.old_x = self.x
        self.old_y = self.y
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def bounce(self):
        #right boundary
        if self.x > WIDTH - self.size:
            self.x = 2 * (WIDTH - self.size) - self.x
            dy = self.y - self.old_y
            dx = self.x - (WIDTH - self.size)
            self.angle = math.atan2(dy, dx)
        #left boundary
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            dy = self.y - self.old_y
            dx = self.x - self.size
            self.angle = math.atan2(dy, dx)
        #bottom boundary
        elif self.y > HEIGTH - self.size:
            self.y = 2 * (HEIGTH - self.size) - self.y
            dy = self.y - (HEIGTH - self.size)
            dx = self.x - self.old_x
            self.angle = math.atan2(dy, dx)
        #top boundary
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            dy = self.y - self.size
            dx = self.x - self.old_x
            self.angle = math.atan2(dy, dx)

    def collide(self, p):        
        dx = self.x - p.x
        dy = self.y - p.y
        distance = math.hypot(dx, dy)
                
        if distance <= self.size + p.size:
            tangent = math.atan2(dy, dx)

            #changing the angle of particles after collision
            self.angle = 2 * tangent - self.angle
            p.angle = 2 * tangent - p.angle

            #exchanging speed/angle after collision
            if p.state != 'dead':
                (self.speed, p.speed) = (p.speed, self.speed)
                (self.angle, p.angle) = (p.angle, self.angle)
                p.x -= math.sin(tangent)
                p.y += math.cos(tangent)
                self.x += math.sin(tangent)
                self.y -= math.cos(tangent)
            
            #contamination
            if all([(self.state == 'ill' or p.state == 'ill'), (self.state != 'dead' and p.state != 'dead')]):
                self.update_color('ill')
                p.update_color('ill')

(WIDTH, HEIGTH) = (400, 400)
BG_COLOR = (255, 255, 255)
TIME_TILL_DEAD = 3000

#creates a Surface and color it
screen = pygame.display.set_mode((WIDTH, HEIGTH))

number_particles = 20
particles = []

#creates the particles in random locations and infects one of them
for i in range(number_particles):
    size = random.randint(10, 20)
    x = random.randint(size, WIDTH - size)
    y = random.randint(size, HEIGTH - size)

    particle = Particle(x, y, 7)
    particle.speed = random.uniform(0.1, 0.3)
    particle.angle = random.uniform(0, math.pi*2)

    particles.append(particle)
    if i == number_particles-1:
        particles[-1].update_color('ill')

#set a name
pygame.display.set_caption('Tutorial 1')

#makes so the program runs indefinitely but quits when it's asked to close
running = True
while running:
    #display the particles
    screen.fill(BG_COLOR)

    #quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #the most time consuming part 
    for i, particle in enumerate(particles):
        if particle.state == 'dead':
            continue
        particle.move()
        particle.bounce()
        for particle2 in particles[i+1:]:
            particle.collide(particle2)
        particle.timer()
        particle.display()
    pygame.display.flip()
