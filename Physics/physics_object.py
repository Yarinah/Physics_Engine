"""
This module contains the Physics Object class, 
which represents a physical object in the simulation.

Author: Yarin Aharonson
Date: 28/07/2024
"""
import pygame

from Utils.vector import Vector


class PhysicsObject:
    def __init__(self, radius: int,
                 position: Vector, velocity: Vector = Vector(0, 0), acceleration: Vector = Vector(0, 0), 
                 density: float = 1, elasticity: float = 1.0, color: tuple = (0, 100, 0)):
        try:
            if not isinstance(position.x or position.y, int):
                raise ValueError("Position must be integer")
            # State
            self.position = position
            self.velocity = velocity
            self.acceleration = acceleration
            
            # Properties
            self.mass = self.calc_mass(density=density)
            self.radius = radius
            self.color = color

            # Coefficients
            self.elasticity = elasticity

        except ValueError as e:
            print(e)
            exit(1)

    def __update_position(self, dt: float) -> None:
        self.position += self.velocity * dt
        int(self.position.x)
        int(self.position.y)

    def __update_velocity(self, dt: float) -> None:
        self.velocity += self.acceleration * dt

    def update(self, dt: float) -> None:
        self.__update_velocity(dt)
        self.__update_position(dt)

    def apply_force(self, force: Vector, dt: float) -> None:
        self.acceleration += force / self.mass

    def calc_mass(self, density: float) -> None:
        """
        Returns the mass of the object from the density and radius.
        assuming the object is a ball.
        """
        self.mass = density * ( 4 / 3 ) * 3.1415 * self.radius ** 3

    def surface_area(self) -> float:
        """
        Returns the surface area of the object,
        assuming the object is a ball.
        """
        return 3.1415 * self.radius ** 2
    
    def __repr__(self) -> str:
        return f'PhysicsObject(position={self.position}, velocity={self.velocity}, acceleration={self.acceleration}, mass={self.mass}, radius={self.radius}, elasticity={self.elasticity})'

     

    # def draw(self, window: pygame.Surface) -> None:
    #     pygame.draw.circle(window, self.color, (self.position.x, self.position.y), self.radius)