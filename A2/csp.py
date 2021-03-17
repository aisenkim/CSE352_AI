from queue import PriorityQueue
from Node import Node


class CSP:
    def __init__(self, constraints, unsigned_vars, constraint_num, color_num, arcs, color_domains):
        self.constraints = constraints
        self.variable_num = len(constraints)
        self.colors_domains = color_domains
        self.unsigned_vars = unsigned_vars  # list of nodes that contain available color, mcv priority, and lcv priorty
        self.constraint_num = constraint_num
        self.color_num = color_num
        self.arcs = arcs

    def set_MCV(self):
        most_constrained_idx = 0
        for i in range(len(self.constraints)):
            #  if already assigned ==> empty list set
            if len(self.constraints[i]) == 0:
                continue
            #  choosing most constrained variable by checking length of each variable constraints
            if len(self.constraints[i]) > len(self.constraints[most_constrained_idx]):
                most_constrained_idx = i
        #  most constrained variable (number)
        # ******* SET IT TO NONE BEFORE CALLING RECURSIV FUNCTION********
        # self.constraints[most_constrained_idx] = None
        return Node(most_constrained_idx, -1)  # color = -1 because color not set yet
