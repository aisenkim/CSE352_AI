import sys
import random
from Node import Node
from csp import CSP


def min_conflict(csp: CSP, max_steps: int, current_state: list):
    # current_state = list of list containing colors (2d list)
    # declare vairble to keep track of colors of solution
    # set used list to -1
    assignment = {}  # hold the solution of colors
    # set all the conflicting constraint varaibles
    conflict_vars = gather_conflict_vars(csp.constraints, current_state, assignment)
    for i in range(max_steps):
        if check_solution(current_state, csp):
            # print("Steps taken to solve: ", i)
            return current_state
        if len(conflict_vars) == 0:
            conflict_vars = gather_conflict_vars(csp.constraints, current_state, assignment)
        """
        if len(assignment) == len(csp.constraints):
            # return assignment
            print("Steps taken to solve: ", i)
            return current_state
        """
        # set random var from conflict_vars, using random index
        # remove it from conflict_vars
        # -------------- start ---------------------------------
        random_idx = random.randrange(len(conflict_vars))
        random_var = conflict_vars[random_idx]
        conflict_vars.pop(random_idx)
        # assignment[random_var.value] = random_var
        # -------------- end ---------------------------------

        # get value that minimize conflict
        # random_idx different from variable.value
        min_const_val = get_min_conflict_val(random_var.value, csp.constraints, current_state, csp.color_num)

        # set min_const_val to current_state
        current_state[random_var.value].color = min_const_val
        assignment[random_var.value] = current_state[random_var.value]
    return {}


def check_solution(current_state, csp):
    for i in range(len(current_state)):
        for j in csp.constraints[i]:
            if current_state[i].color == current_state[j].color:
                return False
    return True


def get_min_conflict_val(variable_val, constraints, current_state, color_num):
    """
    Find minimized conflict value by counting the colors of
    constraining variable.
    :param variable_val:
    :param constraints:
    :param current_state:
    :param color_num:
    :return: min color used by conflicting variables
    """
    color_count = [j for j in range(color_num)]
    for x in range(color_num):
        for constraint in constraints[variable_val]:
            color_node = current_state[constraint]
            color_count[color_node.color] += 1
    min_color = color_count.index(min(color_count))
    if min_color == current_state[variable_val].color:
        return color_count.index(random.choice(color_count))
    return color_count.index(min(color_count))


def gather_conflict_vars(constraints, current_state, assignment):
    conflict_vars = []
    idx = 0  # keep track of index of variable in constraints 2d list
    for x in constraints:
        conflict_added = False
        for constraint in x:
            if current_state[constraint].color == current_state[idx].color:
                conflict_vars.append(current_state[idx])
                conflict_added = True
                break  # only add variable once
        if not conflict_added:
            # if no conflict exists, put it to the assignment
            assignment[idx] = current_state[idx]
        idx += 1
    return conflict_vars


def set_current_state(var_num, color_num):
    # init current_state with random colors
    current_state = []
    for i in range(var_num):
        # create node with value and random color
        node = Node(i, random.randrange(color_num))
        current_state.append(node)
    return current_state


def init_csp(input_file) -> CSP:
    # var_num, const_num, color_num = map(int, input_file.readline().split())
    constraints = [[] for i in range(var_num)]
    # color_used =[[i for i in range(color_num)] for i in range(var_num)]
    for i in input_file:
        first, second = map(int, i.split())
        constraints[first].append(second)  # append second column to index of row (which is variable)
        constraints[second].append(first)
    return CSP(constraints, const_num, color_num, None, None)


def make_solution_file(sol):
    if len(sol) == 0:
        output_file.write("No answer")
        return
    for i in range(len(sol)):
        output_file.write(str(sol[i].color))
        output_file.write("\n")


if __name__ == "__main__":
    # N M K as first line in file
    # N: number of variable
    # M: number of constraints
    # K: possible colors
    # Rest of the lines are constraints

    # init
    input_file = ""
    output_file = ""
    m = 0

    if len(sys.argv) == 3:
        input_file = open(sys.argv[1], 'r')  # -> Input file path
        output_file = open(sys.argv[2], 'w')  # -> Output file paht
    else:
        print(
            'Wrong number of arguments. Usage:\ndfsb.py <I> <> <H> '
            '<INPUT_FILE_PATH> <OUTPUT_FILE_PATH>>')

    var_num, const_num, color_num = map(int, input_file.readline().split())
    csp = init_csp(input_file)
    cur_state = set_current_state(var_num, color_num)
    # call min_conflict() here
    solution = min_conflict(csp, 1000000, cur_state)
    make_solution_file(solution)

    for i in range(len(solution)):
        print(solution[i].color)

    # script to check if soution is valid
    for i in range(len(solution)):
        for j in csp.constraints[i]:
            if solution[i].color == solution[j].color:
                print("False Failed")

    input_file.close()
    output_file.close()
