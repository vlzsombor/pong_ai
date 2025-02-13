import random
import pygame

from neatXD.node import Node


class Gene:
    def __init__(self, in_node: Node, out_node: Node):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = default_weight() 
        self.enabled = True
        self.innovation = 0
        self.color = (0, 255, 0)
 
    def clone(self):
        clone = Gene(self.in_node, self.out_node)
        clone.weight = self.weight
        clone.enabled = self.enabled
        clone.innovation = self.innovation
        return clone
    
    def mutate(self):
        if random.random() < 0.1:
            self.weight = default_weight()
        else:
            self.weight += random.uniform(-0.02, 0.02)
 
            self.weight = self.weight if self.weight < 2 else 2
            self.weight = self.weight if self.weight > -2 else -2
 
    def get_info(self):
        s = str(self.innovation) + "] "
        s += str(self.in_node.number) + "(" + str(self.in_node.layer) + ") -> "
        s += str(self.out_node.number) + "(" + str(self.out_node.layer) + ") "
        s += str(self.weight) + " "
        s += str(self.enabled) + "\n"
        return s
 
    def __str__(self) -> str:
        return self.get_info()
 
    def show(self, ds: pygame.Surface):
        self.color = (255, 0, 0) if self.weight > 0 else (0, 0, 255)
        if not self.enabled:
            self.color = (0, 255, 0)
        pygame.draw.line(ds, self.color, self.in_node.pos, self.out_node.pos, 2)
        pass
    
def default_weight():
    return random.random() * 4 - 2
