import sys
from queue import PriorityQueue
from puzzleGenerator import canMove
from TileProblem import TileProblem


def a_star(puzzle, board_type, heuristics_type):
    frontier = PriorityQueue()  # start with initial puzzle and expand
    explored = []  # put the explored nodes
    solution = []  # return in terms of L U R D
    g_value = 0
    init_puzzle = TileProblem(puzzle, board_type, heuristics_type)
    f_value = init_puzzle.f_func(g_value)
    frontier.put((f_value, id(init_puzzle), init_puzzle))

    while not frontier.empty():
        current = frontier.get()[2]
        if current.is_goal():
            solution.append(current.moved_state)
            # track back to parent nodes 
            parent = current.parent
            while parent.parent != None:
                solution.append(parent.moved_state)
                parent = parent.parent
            solution.reverse()
            return solution  # Success 
        if not is_explored(current, explored):
            g_value += 1
            explored.append(current)
            """
            if current.moved_state:
                solution.append(current.moved_state) """
            for move in range(len(current.move)):
                if canMove(current.state, move):
                    # new_child -> instance of TileProblem
                    new_child = current.transition_func(move)
                    # calculate f_value
                    f_value = new_child.f_func(g_value)
                    frontier.put((f_value, id(new_child), new_child))

    return []  # indicates failure

    # create node -> TileProblem instance
    # insert it in frontier


def RBFS(puzzle, board_type, heuristics_type, f_limit):
    problem  = TileProblem(puzzle, board_type, heuristics_type)
    if problem.is_goal():
        





def is_explored(current, explored):
    if len(explored) == 0:
        return False
    for i in range(len(explored)):
        if current.state == explored[i].state:
            return True
    return False


# def convert_to_board(puzzle_type):
#     for i i

if __name__ == '__main__':
    if len(sys.argv) == 6:
        a = int(sys.argv[1])  # 1 -> A* || 2 -> RBFS
        n = int(sys.argv[2])  # 3 -> 8-puzzle || 4 -> 15-puzzle
        h = int(sys.argv[3])  # 1 -> h1 || 2 -> h2
        input_file = open(sys.argv[4], 'r')  # 3*3 or 4*4 grid
        output_file = open(sys.argv[5], 'w')  # optimal move -> L,R,D,U
    elif len(sys.argv) == 2:
        input_file = open(sys.argv[1], 'r')  # 3*3 or 4*4 grid
    else:
        print(
            'Wrong number of arguments. Usage:\npuzzleSolver.py <A> <N> <H> '
            '<INPUT_FILE_PATH> <OUTPUT_FILE_PATH>>')

# test = [
#     [1,2,0],
#     [3,5,6],
#     [4,7,8]
# ]
test = [
    [1,5,2],
    [4,0,3],
    [7,8,6]
]

test2 = [
    [0,1,6,4],
    [5,3,2,7],
    [9,10,11,8],
    [13,14,15,12]
]
print(a_star(test2, 4, 2))

# practice = TileProblem(test, 3, 1)
# practice2 = TileProblem(test, 3, 1)
# queue = PriorityQueue()
# queue.put((1, id(practice), practice))
# queue.put((1, id(practice2), practice2))
#
# print(queue.get()[2].state)

input_file.close()
# output_file.close()
