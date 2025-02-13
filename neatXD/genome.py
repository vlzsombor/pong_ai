from calendar import c
from operator import ge
import random
from typing import List, Self

from neatXD.gene import Gene

from .geneHistory import GeneHistory
from .node import Node


class Genome:
    def __init__(self, gh: GeneHistory):
        self.gh: GeneHistory = gh
        self.n_inputs: int = self.gh.n_inputs
        self.n_outputs: int = gh.n_outputs
        self.total_nodes = 0
        self.nodes: List[Node] = []
        self.genes: List[Gene] = []



        self.fitness = random.uniform(0,200)
        self.adjusted_fitness = 0

        for _ in range(self.n_inputs):
            self.nodes.append(Node(self.total_nodes, 0))
            self.total_nodes += 1

        for _ in range(self.n_outputs):
            self.nodes.append(Node(self.total_nodes, 1))
            self.total_nodes += 1
        pass

    def clone(self):
        clone = Genome(self.gh)
        clone.total_nodes = self.total_nodes
        clone.nodes.clear()
        clone.genes.clear()

        for i in range(len(self.nodes)):
            clone.nodes.append(self.nodes[i].clone())

        for i in range(len(self.genes)):
            clone.genes.append(self.genes[i].clone())

        clone.connect_genes()
        return clone
    
    def exists(self, inno: int):
        for g in self.genes:
            if g.innovation == inno:
                return True
        return False
    
    def connect_nodes(self, n1: Node, n2: Node):
        n1Layer= n1.layer if n1.layer != 1 else 1000000
        n2layer = n2.layer if n2.layer != 1 else 1000000

        if n1Layer > n2layer:
            n1, n2 = n2, n1

        c = self.gh.exists(n1, n2)
        x = Gene(n1, n2)

        if c:
            x.innovation = c.innovation
            if not self.exists(x.innovation):
                self.genes.append(x)
        else:
            x.innovation = self.gh.global_inno
            self.gh.global_inno += 1
            self.gh.all_genes.append(x.clone())
            self.genes.append(x)
        pass

    def add_gene(self):
        n1 = random.choice(self.nodes)
        n2 = random.choice(self.nodes)

        while n1.layer == n2.layer:
            n1 = random.choice(self.nodes)
            n2 = random.choice(self.nodes)
        self.connect_nodes(n1, n2)
        pass

    def mutate(self):
        if len(self.genes) == 0:
            self.add_gene()
        if random.random() < 0.8:
            for i in range(len(self.genes)):
                self.genes[i].mutate()
        if random.random() < 0.08:
            self.add_gene()
        if random.random() < 0.02:
            self.add_node()
        pass
    ####


    def crossover(self, partner: Self):
        child = Genome(self.gh)
        child.nodes.clear()
        
        try:
#            p1_highest_inno = max()
            p1_highest_inno = max([(a.innovation) for a in self.genes])
        except Exception:
            p1_highest_inno = 0

        try:
            p2_highest_inno = max([(a.innovation) for a in partner.genes])
        except Exception:
            p2_highest_inno = 0


        if self.total_nodes > partner.total_nodes:
            child.total_nodes = self.total_nodes
            for i in range(self.total_nodes):
                child.nodes.append(self.nodes[i].clone())
        else:
            child.total_nodes = partner.total_nodes
            for i in range(partner.total_nodes):
                child.nodes.append(partner.nodes[i].clone())

        highest_inno = (
            p1_highest_inno if self.fitness > partner.fitness else p2_highest_inno
        )


        for i in range(highest_inno + 1):
            selfGeneExists = self.exists(i)
            partnerGeneExists = partner.exists(i)

            v: Self | None = None
            if(selfGeneExists and partnerGeneExists):
                v = self if random.random() > 0.5 else partner
            elif(selfGeneExists):
                v = self
            elif(partnerGeneExists):
                v = partner
            
            if not v:
                continue

            if (gene := v.get_gene(i)):
                    child.genes.append(gene)
        child.connect_genes()
        return child

    def get_gene(self, inno: int):
        for g in self.genes:
            if g.innovation == inno:
                return g.clone()
        print('Gene not found')

    def add_node(self):
        if len(self.genes) == 0:
            self.add_gene()
        
        if random.random() < 0.9:
            self.gh.highest_hidden += 1

        n = Node(self.total_nodes, random.randint(2, self.gh.highest_hidden))

        g = random.choice(self.genes)
        l1 = g.in_node.layer
        l2 = g.out_node.layer

        if l2 == 1:
            l2 = 1000000 # $$$ wtf is this?
        
        while l1 > n.layer or l2 < n.layer:
            g = random.choice(self.genes)
            l1 = g.in_node.layer
            l2 = g.out_node.layer
            if l2 == 1:
                l2 = 1000000
        self.connect_nodes(g.in_node, n)
        self.connect_nodes(n, g.out_node)
        self.genes[-1].weight = 1.0
        self.genes[-2].weight = g.weight
        g.enabled = False
        self.nodes.append(n)
        self.total_nodes += 1

        pass

    def get_node(self, n: int):
        for i in range(len(self.nodes)):
            if self.nodes[i].number == n:
                return self.nodes[i]
        raise ValueError("Node not found : Something's Wrong")

    def connect_genes(self) -> None:
        for i in range(len(self.genes)):
            self.genes[i].in_node = self.get_node(self.genes[i].in_node.number)
            self.genes[i].out_node = self.get_node(self.genes[i].out_node.number)
        
        for i in range(len(self.nodes)):
            self.nodes[i].in_genes.clear()
        
        for i in range(len(self.genes)):
            self.genes[i].out_node.in_genes.append(self.genes[i])
        pass

    def get_outputs(self, inputs: List[float]):
        if len(inputs) != self.n_inputs:
            print("Wrong number of inputs")
            return [-1.0]
        

        for i in range(self.n_inputs):
            self.nodes[i].output = inputs[i]
        
        self.connect_genes()

        for layer in range(2, self.gh.highest_hidden + 1):
            nodes_in_layer: List[Node] = []
            for n in range(len(self.nodes)):
                if self.nodes[n].layer == layer:
                    nodes_in_layer.append(self.nodes[n])
            for n in range(len(nodes_in_layer)):
                nodes_in_layer[n].calculate()

        final_outputs: List[float] = []

        for n in range(self.n_inputs, self.n_inputs + self.n_outputs):
            self.nodes[n].calculate()
            final_outputs.append(self.nodes[n].output)

        return final_outputs