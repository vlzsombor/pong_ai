


import pygame
import math
from typing import List
from typing import Callable

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neatXD.gene import Gene


activation_function: Callable[[float], float] = lambda x : 1 / (1 + math.exp(-x))


class Node:
    def __init__(self, number: int, layer: int):
        self.number: int = number
        self.layer: int = layer
        self.output: float = 0
        self.in_genes: List[Gene]  = []

        # showing
        self.color = (255, 255, 255)
        self.bcolor = (0, 0, 0)

        self.radius = 5
        self.border_radius = 2
        self.pos = [0, 0]

        pass

    def clone(self):
        n = Node(self.number, self.layer)
        n.output = self.output
        n.pos = self.pos
        return n
    
    def calculate(self):
        if self.layer == 0:
            print("No calculations for first layer")
            return
        
        s = 0.0
        for g in self.in_genes:
            if g.enabled:
                s += g.in_node.output * g.weight
        if(s < -500):
            self.output = 0
            return
        self.output = activation_function(s)
        pass
    def show(self, ds: pygame.Surface):
        pygame.draw.circle(ds, self.bcolor, self.pos, self.radius + self.border_radius)
        pygame.draw.circle(ds, self.color, self.pos, self.radius)
        pass