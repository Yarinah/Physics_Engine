import pygame
import time
import random

from Utils.vector import Vector
from Physics.physics_object import PhysicsObject
from Physics.physics_simulator import PhysicsSimulator

pygame.init()

#abc
# Set up the display
width = 400
height = 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics Engine')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

objects = []

# Create objects
obj1 = PhysicsObject(radius=10, position=Vector(100, 100), velocity=Vector(0, 2))
obj2 = PhysicsObject(radius=10, position=Vector(150, 300), velocity=Vector(0, 0))
# objects.extend([obj1, obj2])


# Add objects with random values
for i in range(20):
    # mass = random.uniform(0.5, 5)
    radius = random.randint(5, 15)
    position = Vector(random.randint(0, width), random.randint(0, height))
    velocity = Vector(random.uniform(-2, 2), random.uniform(-2, 2))
    objects.append(PhysicsObject(mass=mass, radius=radius, position=position, velocity=velocity))

simulator = PhysicsSimulator(window, objects=objects)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(WHITE)
    simulator.update()

    
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()