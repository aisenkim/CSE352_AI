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

    return RBFS(problem, float('inf'), count = 1)


def RBFS(problem, f_limit, count):
    if problem.is_goal():
        print(count)
        return problem, None  # where problem -> solution
    successors = []
    g_val = problem.g_value
    g_val += 1
    # add child node -> successors
    for action in range(len(problem.move)):
        if canMove(problem.state, action):
            # g_val +=1 
            new_child = problem.transition_func(action)
            new_child.g_value = g_val  # update g_value ####
            f_value = new_child.f_func(g_val)
            new_child.f_value = f_value  # keep recording f_value in all instance
            successors.append(new_child)
            # successors.put((max(f_value, problem.f_value), id(new_child), new_child))
    if len(successors) == 0:
        return None, float('inf')
    for i in range(len(successors)) :
        s = successors[i] # TileProblem Object
        s.f_value = max(s.f_value, problem.f_value)  # how do we know if there is any value from previous search
    while len(successors) != 0:
        successors.sort(key=lambda x: x.f_value, reverse=False)
        count += 1
        # best = successors.queue[0][2] # --> TileProblem containing the lowest f_value (best)
        best = successors[0]
        if best.f_value > f_limit:
            return None, best.f_value
        alternative = successors[1]  # --> TileProblem containing the second lowest f_value (second best)
        result, best.f_value = RBFS(best, min(f_limit, alternative.f_value), count)
        successors.append(best)
        if result != None:
            return result, None



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


def get_solution(puzzle, search_type, size, heuristic):
    sol = []
    if search_type == 1:
        sol = a_star(puzzle, size, heuristic)
    else:
        result = recursive_best_first_search(puzzle, size, heuristic)[0]
        sol.append(result.moved_state)
        # track back to parent nodes
        parent = result.parent
        while parent.parent is not None:
            sol.append(parent.moved_state)
            parent = parent.parent
        sol.reverse()

    return sol


# def print_solution(solution):
#     str = []
#     for letter in solution:
#         (','.join(letter))


def make_solution_file(sol):
    for i in range(len(sol)):
        output_file.write(sol[i])
        if i != len(sol) - 1:
            output_file.write(",")


if __name__ == '__main__':
    a = 0
    n = 0
    h = 0
    input_file = ''
    out_file = ''

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
make_solution_file(solution)


input_file.close()
output_file.close()
