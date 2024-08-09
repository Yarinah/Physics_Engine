"""
This module contains the Physics Simulator class,
which is responsible for simulating the physics.

Author: Yarin Aharonson
Date: 28/07/2024
"""
import pygame

from Utils.vector import Vector
from Physics.physics_object import PhysicsObject

class PhysicsSimulator:
    def __init__(self, window: pygame.Surface,
                 gravity: Vector = Vector(x=0, y=0), time_step: float = 1, objects: list[PhysicsObject] = [],
                 gravity_constant: float = 1e-3, drag_constant: float = 1e-8) -> None:
        self.window = window
        self.gravity = gravity
        self.time_step = time_step
        self.objects = objects

        # Constants
        # self.gravity_constant = 6.67430e-11
        self.gravity_constant = gravity_constant
        self.drag_constant = drag_constant
        
        self.__apply_gravity()

    def __apply_gravity(self) -> None:
        for obj in self.objects:
            obj.apply_force(self.gravity * obj.mass, self.time_step)

    def __draw_objects(self) -> None:
        for obj in self.objects:
            pygame.draw.circle(self.window, obj.color, (int(obj.position.x), int(obj.position.y)), obj.radius)

    def __check_collision(self, obj1: PhysicsObject, obj2: PhysicsObject) -> bool:
        distance = (obj2.position - obj1.position).magnitude()
        return distance < obj1.radius + obj2.radius
    
    def __resolve_collision(self, obj1: PhysicsObject, obj2: PhysicsObject) -> None:
        collision_normal = (obj2.position - obj1.position).normalize()
        relative_velocity = obj2.velocity - obj1.velocity
        velocity_along_normal = relative_velocity.dot(collision_normal)

        if velocity_along_normal > 0:
            return
        
        impulse_strength = -(1 + obj1.elasticity) * velocity_along_normal
        impulse_strength /= (1 / obj1.mass + 1 / obj2.mass)

        impulse = collision_normal * impulse_strength
        obj1.velocity -= impulse / obj1.mass
        obj2.velocity += impulse / obj2.mass


    # TODO: fix this function, give force instead of changing velocity
    def __resolve_wall_collision(self) -> None:
        for obj in self.objects:
            # x-axis
            if obj.position.x - obj.radius < 0:
                obj.velocity.x *= -obj.elasticity
                obj.position.x = obj.radius
            if obj.position.x + obj.radius > self.window.get_width():
                obj.velocity.x *= -obj.elasticity
                obj.position.x = self.window.get_width() - obj.radius
            # y-axis
            if obj.position.y - obj.radius < 0:
                obj.velocity.y *= -obj.elasticity
                obj.position.y = obj.radius
            if obj.position.y + obj.radius > self.window.get_height():
                obj.velocity.y *= -obj.elasticity
                obj.position.y = self.window.get_height() - obj.radius


    def __gravity_between_objects(self) -> None:
        for idx, obj1 in enumerate(self.objects):
            for obj_idx in range(idx + 1, len(self.objects)):
                obj2 = self.objects[obj_idx]
                normalize_force = (obj2.position - obj1.position).normalize() * (obj1.mass * obj2.mass) / (obj2.position - obj1.position).magnitude() ** 2
                force = normalize_force * self.gravity_constant
                obj1.apply_force(force, self.time_step)
                obj2.apply_force(-force, self.time_step)

    # TODO: fix this function
    def __apply_drag(self) -> None:
        for obj in self.objects:
            if obj.velocity.magnitude() == 0:
                continue
            drag_vec = (-obj.velocity.normalize())*(obj.velocity.magnitude()**2)
            # drag_vec = (-obj.velocity.normalize())*(obj.velocity.magnitude())
            drag = drag_vec * obj.surface_area() * self.drag_constant
            obj.apply_force(drag, self.time_step)

        

    def update(self) -> None:
        """
        Update the physics simulation.
        """
        # Check for collisions
        for idx, obj1 in enumerate(self.objects):
            for obj_idx in range(idx + 1, len(self.objects)):
                obj2 = self.objects[obj_idx]
                if self.__check_collision(obj1, obj2):
                    self.__resolve_collision(obj1, obj2)
        self.__resolve_wall_collision()

        self.__gravity_between_objects()
        self.__apply_drag()


        # Update objects
        for obj in self.objects:
            obj.update(self.time_step)

        self.__draw_objects()  

