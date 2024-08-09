"""
This module contains a class for 2D vectors.

Author: Yarin Aharonson
Date: 28/07/2024
"""

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other_vector: 'Vector') -> 'Vector':
        return Vector(self.x + other_vector.x, self.y + other_vector.y)
    
    def __sub__(self, other_vector: 'Vector') -> 'Vector':
        return Vector(self.x - other_vector.x, self.y - other_vector.y)
    
    def __mul__(self, scalar: float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector':
        return Vector(self.x / scalar, self.y / scalar)
    
    def __neg__(self) -> 'Vector':
        return Vector(-self.x, -self.y)
    
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def normalize(self) -> 'Vector':
        mag = self.magnitude()
        return Vector(self.x / mag, self.y / mag)
    
    def dot(self, other_vector: 'Vector') -> float:
        return self.x * other_vector.x + self.y * other_vector.y
    
    def __repr__(self) -> str:
        return f'Vector({self.x}, {self.y})'
    