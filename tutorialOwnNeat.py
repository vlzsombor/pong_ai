from typing import List
import pygame
from neatXD.geneHistory import GeneHistory
from neatXD.genome import Genome
from pong import Game
import os
import pickle

from population import PongPlayer, PopulationPong

filename = 'checkpoint/best_pickle.pkl2025-02-13T08:57:45.834273'

width, height = 700, 500
window = pygame.display.set_mode((width, height))


class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball
        self.gh = GeneHistory(3, 3)

    def test_ai(self):

        with open(filename, "rb") as file:
            genome: Genome = pickle.load(file)

        p = PongPlayer(self.gh, clone=True, brain = genome)
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.game.move_paddle(left=False, up = True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=False, up = False)

            # $$$ inputs, List[int] 3 elements
            output = p.think([self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)])
            # $$$ outputs List[int] 3 elements, 
            decision = output.index(max(output))
            # $$$ 0== do nothing
            if decision == 0:
                pass
            # $$$ 1 == up
            elif decision == 1:
                self.game.move_paddle(left=True, up=True)
            # $$$ 1 == down
            else:
                self.game.move_paddle(left=True, up=False)

            ############ left paddle


            game_info = self.game.loop()
            print(game_info.left_score, game_info.right_score)
            self.game.draw(True, False)
            pygame.display.update()



    
    def train_ai(self, genome1, genome2):
        #net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        #net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        #clock = pygame.time.Clock()

        run = True
        while run:
            #clock.tick(180)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()            
            game_info = self.game.loop()
            self.game.draw(draw_score=True, draw_hits=True)
            #pygame.display.update()

            output1 = genome1.think([self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)])
            decision1 = output1.index(max(output1))
            
            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            output2 = genome2.think([self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)])
            decision2 = output2.index(max(output2))
            
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            # print(output1)
            # print(output2)
            #58:15
            if (game_info.left_score >= 1 
                or game_info.right_score >= 1 
                or game_info.left_hits > 50):

                if game_info.left_hits + game_info.right_hits > 5:
                    print('Summary ' + str(game_info.left_hits + game_info.right_hits))
                self.calculate_fitness(genome1, genome2, game_info)
                break
            


    def calculate_fitness(self, genome1, genome2, game_info):
        genome1.fitness += game_info.left_hits
        genome2.fitness += game_info.right_hits

def eval_genomes(genomes, config):
    window = pygame.display.set_mode((width, height))



    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(window, width, height)
            game.train_ai(genome1, genome2)    


def run_neat():
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # #p = neat.Population(config)
    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(1))
    window = pygame.display.set_mode((width, height))

    gh = GeneHistory(3, 3)
    population = PopulationPong(gh)
    while True:
        for i, (genome) in enumerate(population.population):
            
            if i == len(population.population) - 1:
                break
            genome.fitness = 0
            for genome2 in population.population[i+1:]:
                genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
                game = PongGame(window, width, height)
                game.train_ai(genome, genome2)
        population.reset()

def test_neat():
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # #p = neat.Population(config)
    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(1))
    window = pygame.display.set_mode((width, height))

    gh = GeneHistory(3, 3)
    population = PopulationPong(gh, True)
    while True:
        game = PongGame(window, width, height)

        game.test_ai()


        # for i, (genome) in enumerate(population.population):
            
        #     if i == len(population.population) - 1:
        #         break
        #     genome.fitness = 0
        #     for genome2 in population.population[i+1:]:
        #         genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
        # population.reset()




    #winner = p.run(eval_genomes, 15)

    # with open('best.pickle', 'wb') as f:
    #     pickle.dump(winner, f)

    def test_ai(config):
        with open("best.pickle", "rb") as f:
            winner = pickle.load(f)

        game = PongGame(window, width, height)
        game.test_ai(winner, config)
    game = PongGame(window, width, height)
    game.test_ai()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    
    # config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
    #                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
    #                      config_path)


    #run_neat()
    test_neat()

    