from queue import PriorityQueue
from Node import Node


class CSP:
    def __init__(self, constraints, unsigned_vars, constraint_num, color_num):
        self.constraints = constraints
        self.unsigned_vars = unsigned_vars
        self.constraint_num = constraint_num
        self.color_num = color_num

    def set_MCV(self):
        """
        Set unsigned variable as priority queue
        pop most constrained variable
        for DFSB++
        :return: None
        """
        self.unsigned_vars = PriorityQueue()
        for i in range(len(self.constraints)):
            # put the - length of constraints for each variable and Node(value, color)
            # set the list of valid colors as 1 (since none has been constrained yet)
            self.unsigned_vars.put((-len(self.constraints[i]), Node(i, -1, [1 for x in range(self.color_num)])))

    def set_LCV(self, assignment: dict) -> list:
        """
        set the least constrained variable
        go through assignment list and
        insert color in order of least used
        :param assignment: list containing assigned nodes
        :return: None
        """
        #  init color_count
        color_count = [0 for x in range(self.color_num)]
        for variable in assignment: # gets key value of dict
            node = assignment[variable] # gets node corresponding to value
            color_count[node.color] += 1
        return color_count
