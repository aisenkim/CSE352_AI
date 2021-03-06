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


def recursive_best_first_search(puzzle, board_type, heuristics_type):
    # initial stage
    problem = TileProblem(puzzle, board_type, heuristics_type)

    return RBFS(problem, float('inf'))


def RBFS(problem, f_limit):
    if problem.is_goal():
        return problem, None  # where problem -> solution
    successors = []
    g_val = problem.g_value
    g_val += 1
    # add child node -> successors
    for action in range(len(problem.move)):
        if canMove(problem.state, action):
            # g_val +=1 
            new_child = problem.transition_func(action)
            new_child.g_value = g_val  # update g_value ###########&*&*&*&*& ccheck!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            f_value = new_child.f_func(g_val)
            new_child.f_value = f_value  # keep recording f_value in all instance
            successors.append(new_child)
            # successors.put((max(f_value, problem.f_value), id(new_child), new_child))
    if len(successors) == 0:
        return None, float('inf')
    # for i in range(len(successors.queue)) : 
    #     s = successors.queue[i][2] # TileProblem Object
    #     s.f_value = max(f_value, problem.f_value)  # how do we know if there is any value from previous search
    while len(successors) != 0:
        successors.sort(key=lambda x: x.f_value, reverse=False)
        # best = successors.queue[0][2] # --> TileProblem containing the lowest f_value (best)
        best = successors[0]
        if best.f_value > f_limit:
            return None, best.f_value
        alternative = successors[1]  # --> TileProblem containing the second lowest f_value (second best)
        result, best.f_value = RBFS(best, min(f_limit, alternative.f_value))
        successors.append(best)
        if result != None:
            return result, None


"""   
def RBFS(problem, f_limit):
    if problem.is_goal():
        return problem, None # where problem -> solution 
    successors = PriorityQueue() 
    g_val = problem.g_value
    g_val += 1
    # add child node -> successors
    for action in range(len(problem.move)):
        if canMove(problem.state, action):
            new_child = problem.transition_func(action)
            f_value = new_child.f_func(g_val)
            #update f with value from previous search, if any 
            new_child.f_value = f_value # keep recording f_value in all instance
            if new_child.state != new_child.parent.state: # don't consider what was added (maybe remove this)
                successors.put((max(f_value, problem.f_value), id(new_child), new_child))
    if successors.empty():
        return None, float('inf')
    while 1:
        best = successors.get() # [0]-> f-value, [1] -> id, [2] -> TileProblem instance
        best_f =best[0] # f-value of dequeued 
        best_puzzle = best[2]
        best_puzzle.f_value = best_f # update the TileProblem.f_value 
        if best_puzzle.f_value > f_limit:
            return None, best_puzzle.f_value
        alternative_f = successors.get()[0] # second best f-val
        result, best_puzzle.f_value = RBFS(best_puzzle, min(f_limit, alternative_f)) 
        if result != None:
            return result, None

"""


def is_explored(current, explored):
    if len(explored) == 0:
        return False
    for i in range(len(explored)):
        if current.state == explored[i].state:
            return True
    return False


def create_board(size, input_text):
    """
    given text file, creates board
    :param size:  3 -> 3*3  or  4-> 4*4
    :param input_text: text from text file
    :return: 2d board
    """
    lst = []
    int_lst = []
    for i in input_text:
        lst += i.rstrip().split(",")
    counter = 0
    tmp = []
    for i in lst:
        counter += 1
        if i == "":
            i = 0
        num = int(i)
        tmp.append(num)
        if (counter % size) == 0:
            int_lst.append(tmp)
            tmp = []
    return int_lst


def get_solution(board, search_type, size, heuristic):
    solution = []
    if search_type == 1:
        solutoin = a_star(board, size, heuristic)
    else:
        result = recursive_best_first_search(board, n, h)[0]
        solution.append(result.moved_state)
        # track back to parent nodes
        parent = result.parent
        while parent.parent is not None:
            solution.append(parent.moved_state)
            parent = parent.parent
        solution.reverse()

    return solution


def print_solution(solution):
    str = []
    for letter in solution:
        print(','.join(letter))


# def convert_to_board(puzzle_type):
#     for i i

if __name__ == '__main__':
    if len(sys.argv) == 6:
        a = int(sys.argv[1])  # 1 -> A* || 2 -> RBFS
        n = int(sys.argv[2])  # 3 -> 8-puzzle || 4 -> 15-puzzle
        h = int(sys.argv[3])  # 1 -> h1 || 2 -> h2
        input_file = open(sys.argv[4], 'r')  # 3*3 or 4*4 grid
        output_file = open(sys.argv[5], 'w')  # optimal move -> L,R,D,U
    else:
        print(
            'Wrong number of arguments. Usage:\npuzzleSolver.py <A> <N> <H> '
            '<INPUT_FILE_PATH> <OUTPUT_FILE_PATH>>')

board = create_board(n, input_file)
solution = get_solution(board, a, n, h)

"""
# test = [
#     [1,6,2],
#     [4,0,5],
#     [7,8,3]
# ]

# test = [
#     [0, 6, 2],
#     [4, 1, 5],
#     [7, 8, 3]
# ]

test = [
    [1,5,2],
    [7,4,3],
    [0,8,6]
]

test2 = [
    [0, 1, 6, 4],
    [5, 3, 2, 7],
    [9, 10, 11, 8],
    [13, 14, 15, 12]
]

test3 = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [10, 11, 0, 12],
    [9, 13, 14, 15]
]

print(a_star(test, 3, 2))
result = recursive_best_first_search(test, 3, 1)[0]
# result = recursive_best_first_search(test2, 4, 2)[0]
# result = recursive_best_first_search(test3, 4, 2)[0]
solution = []
solution.append(result.moved_state)
# track back to parent nodes
parent = result.parent
while parent.parent is not None:
    solution.append(parent.moved_state)
    parent = parent.parent
solution.reverse()
print(solution)

# practice = TileProblem(test, 3, 1)
# practice2 = TileProblem(test, 3, 1)
# queue = PriorityQueue()
# queue.put((1, id(practice), practice))
# queue.put((1, id(practice2), practice2))
#
# print(queue.get()[2].state)
"""
input_file.close()
# output_file.close()
