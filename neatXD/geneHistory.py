from typing import List

from neatXD.gene import Gene

from .node import Node

class GeneHistory:
    def __init__(self, n_inputs: int, n_outputs: int):
        self.n_inputs: int = n_inputs
        self.n_outputs: int = n_outputs
        self.all_genes: List[Gene] = []
        # Global highest innovation
        self.global_inno = 0
        self.highest_hidden = 2
        pass

    def exists(self, input_node: Node, output_node: Node):
        for g in self.all_genes:
            if g.in_node.number == input_node.number and g.out_node.number == output_node.number:
                return g.clone()
        return None
