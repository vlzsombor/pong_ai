import random
import pickle 
import uuid

import datetime

from typing import List, Self

from neatXD.geneHistory import GeneHistory
from neatXD.genome import Genome

filename = 'checkpoint/best_pickle.pkl'

class PopulationPong:
    def __init__(self, gh: GeneHistory, pop_size: int = 50, testAi = False) -> None: 
        self.best_fitness = 0
        self.pop_size = pop_size  # Size of population
        self.population: List[PongPlayer] = []  # Population is sprite group
        self.gh = gh
        self.best_fitness = 0
        self.testAi = testAi
        if testAi:
            with open(filename, "rb") as file:
                genome: Genome = pickle.load(file)

            self.population.append(PongPlayer(gh, brain=genome))
            return

        for _ in range(self.pop_size):
            self.population.append(PongPlayer(gh))
        pass


    def reset(self):
        print('reset')
        if self.testAi:
            self.population.clear()
            with open(filename, "rb") as file:
                genome: Genome = pickle.load(file)

            self.population.append(PongPlayer(self.gh, brain=genome))
            return
        
        parents = self.population.copy()

        parents.sort(key = lambda x: x.fitness, reverse=True)
        self.population.clear()

        bestAutoplayer = parents[0]
        filehandler = open(filename + str(datetime.datetime.now().isoformat()), 'wb')   
        pickle.dump(bestAutoplayer.brain, filehandler)

        for _ in range(self.pop_size):
            parent1 = parents[random.randint(0,len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]
            
            
            childPlayer = parent1.mate(parent2)
            childPlayer.brain.mutate()
            
            self.population.append(childPlayer)        
        self.best_fitness = 0
        pass

class PongPlayer:
    def __init__(self, gh: GeneHistory, clone: bool = False, brain: Genome | None = None) -> None:
        self.gh = gh  # The genome history
        if brain is not None:
            self.brain = brain
        else:
            self.brain = Genome(gh)
        self.fitness = 0
        self.alive = True
        # Random mutations for brain at start
        if not clone:
            for _ in range(10):
                self.brain.mutate()
                pass
    def mate(self, partner: Self):
        child = PongPlayer(self.gh)
        child.brain = self.brain.crossover(partner.brain)
        return child
        
    # def get_inputs(self, pipes: Pipes, window: Window) -> List[float]:
    #     inputs: List[float] = []
    #     y_pos_ground = 512 # I guess thats the ground y height
    #     input0 = (y_pos_ground - self.rect.y) / window.height  # bird height
    #     input1 = (pipes.upper[0].x - self.rect.x) / window.width  # Dist from pipe

    #     input2 = (pipes.upper[0].y - self.y) / window.height
    #     input3 = (self.y - pipes.lower[0].y) / window.height
    #        # (self.rect.y - closest.bottomPos) / win_height
    #     inputs.append(input0)  # Dist from bird to top Pipe
    #     inputs.append(input1)  # Dist from bird to top Pipe
    #     inputs.append(input2)  # Dist from bird to top Pipe
    #     inputs.append(input3)  # Dist from bird to bottom Pipe
    #     return inputs

    def think(self, inputs: List[float]) -> List[float]:
        should_flap = False
        # Get outputs from brain
        outs = self.brain.get_outputs(inputs)
        #sigmoid: Callable[[float], float] = lambda x: 1 / (1 + math.exp(-x))
        #outs: List[float] =[0.89, sigmoid(inputs[2]*-0.922838921439954 + -inputs[2] * 1.8011388502959025)]
        #outs: List[float] =[0.89, sigmoid(-2.72397777 * inputs[2])]
        # with open("C:\\Users\\ZsomborVeres-Lakos\\Documents\\flappy_outputs.csv", 'a') as f:
        #     f.write(str(outs[1]) + '\n')
        # use outputs to flap or not
        return outs
    
    def clone(self):
        child = PongPlayer(self.gh, True)
        child.brain = self.brain.clone()
        return child
