from Heuristics import Heuristics
from puzzleGenerator import moveGap
import copy

"""
    ==================
    author: Aisen Kim
    ==================

   state: array of board (8 or 15)
   action: movement of blank space
   transition function: state -> action -> result
   goal state: check -> result == goal state
"""


class TileProblem:
    def __init__(self, board, board_type, heuristic_type):
        """
        Initialize state, action, and size of graph
        :param board: puzzle in 2d array
        :param board_type:  3 -> 8-puzzle || 4 -> 15-puzzle
        :param heuristic_type: 1 -> manhattan || 2 -> hamming
        """
        self.state = board
        # moves = UP, RIGHT, DOWN, LEFT
        self.move = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.move_letter = ['U', 'R', 'D', 'L']
        self.moved_state = ''  # when first created through transition_func, which direction did it get altered
        self.board_type = board_type
        self.heuristic_type = heuristic_type
        self.parent = None # store the parent instance 
        self.f_value = 0
        self.g_value = 0
        if board_type == 3:
            self.puzzle_goal = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]
            ]
        else:
            self.puzzle_goal = [
                [1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 0]
            ]

    def transition_func(self, move_idx):
        """
        perform movement and produce child node
        :param: move_idx int value for -> [instructions using L, U, R, D]
        :return: altered board
        """
        child = copy.deepcopy(self.state)
        moveGap(child, self.move[move_idx])
        new_board = TileProblem(child, self.board_type, self.heuristic_type)
        new_board.moved_state = new_board.move_letter[move_idx]
        new_board.parent = self # store parent's TileProblem object

        return new_board

    def is_goal(self):
        """
        check if it's goal
        goal -> true || not goal -> false
        :return: -> bool
        """
        return self.state == self.puzzle_goal

    def f_func(self, g_val):
        heuristics = Heuristics()
        if self.heuristic_type == 1:  # manhattan
            if self.board_type == 3:  # 8-puzzle
                goal_state = {
                    1: [0, 0], 2: [0, 1], 3: [0, 2],
                    4: [1, 0], 5: [1, 1], 6: [1, 2],
                    7: [2, 0], 8: [2, 1], 0: [2, 2]
                }
            else:
                goal_state = {
                    1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3],
                    5: [1, 0], 6: [1, 1], 7: [1, 2], 8: [1, 3],
                    9: [2, 0], 10: [2, 1], 11: [2, 2], 12: [2, 3],
                    13: [3, 0], 14: [3, 1], 15: [3, 2], 0: [3, 3]
                }
            return g_val + heuristics.manhattan_d(self.state, goal_state)
        else:
            return g_val + heuristics.hamming_d(self.state, self.puzzle_goal)
