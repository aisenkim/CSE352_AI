import sys
import copy
from Node import Node
from queue import PriorityQueue
from collections import deque
from csp import CSP


def dfs(csp: CSP, m: int) -> dict:
    """
    call normal dfs if m == 0
    otherwise call dfs++
    :param csp: instance of CSP
    :param m: 0 -> normal dfs || 1 -> dfs++
    :return: dictionary containing solution
    """
    if m == 0:
        return dfs_backtrack({}, csp)
    else:
        return dfs_plus_backtrack({}, csp)


def dfs_backtrack(assignment: dict, csp: CSP):
    # if the assignment's length == M: variable number, then return assignment
    if len(assignment) == len(csp.constraints):
        return assignment
    # select idx of assignment
    variable: Node = select_unassigned(assignment, csp)

    for value in range(csp.color_num):
        # check if value consistent with assignment
        var_num: int = variable.value
        var_constraints: list = csp.constraints[var_num]  # list of constraints for current variable
        # loop through each constraint to check
        if is_color_valid(var_constraints, assignment, value):
            variable.color = value
            assignment[var_num] = variable
            # recursive call
            result = dfs_backtrack(assignment, csp)
            if len(result) != 0:  # if result != failure
                return result
            assignment.pop(var_num)
    return {}  # return failure (should it be {} or assignment???)


def dfs_plus_backtrack(assignment: dict, csp: CSP) -> dict:
    if len(assignment) == len(csp.constraints):
        return assignment
    # AC_3 to prune domain
    AC_3(csp)
    # select most constrained variable
    variable: Node = csp.set_MCV()
    # sort domains of current variable for LCV
    sort_domains(csp.constraints, csp.colors_domains, variable.value, csp.color_num)
    for color in csp.colors_domains[variable.value]:
        if is_color_valid(csp.constraints[variable.value], assignment, color):
            variable.color = color
            assignment[variable.value] = variable
            # push into assignments so mark as used by setting it as empty
            # instead of doing it in csp.py
            csp.constraints[variable.value] = []
            #recursive call
            result = dfs_plus_backtrack(assignment, csp)
            if len(result) != 0:
                return result
            assignment.pop(variable.value)
    return {}


def sort_domains(constraints, colors_domains, var_value, color_num):
    lst = [0 for i in range(color_num)]
    # for each constraints in variable...
    for i in constraints[var_value]:
        # for each color in domain of constrained variable
        for j in colors_domains[i]:
            if j != -1:
                lst[j] += 1  # increment color's counter
    # sort the list from least to greatest
    for i in range(color_num):
        min_idx = lst.index(min(lst))
        lst[min_idx] += 100  # to get the next min idx
        # update original var_value domain with sorted list
        colors_domains[var_value][i] = min_idx


def AC_3(csp: CSP):
    local_arcs: deque = copy.deepcopy(csp.arcs)
    while local_arcs:
        val_i, val_j = local_arcs.popleft()
        if remove_inconsistent_value(val_i, val_j, csp.colors_domains):
            for k in local_arcs:
                # if k[0] is Xi
                if k[0] == val_i:
                    local_arcs.append([k[1], k[0]])


def remove_inconsistent_value(val_i: int, val_j: int, color_domains: list) -> bool:
    removed = False
    val_i_domain = color_domains[val_i]  # [ val_i colors ]
    val_j_domain = color_domains[val_j]  # [val_j colors ]
    for i in range(len(color_domains[val_i])):
        satisfied_counter = 0
        for j in range(len(color_domains[val_j])):
            if val_i_domain[i] != val_j_domain[j] and val_j_domain[j] != -1:
                # at least 1 color that allows (x,y) to be satisfied
                satisfied_counter += 1
        # if non satisfied for a color ... prune
        if satisfied_counter == 0:
            val_i_domain[i] = -1
            removed = True
    return removed


def is_color_valid(constraints: list, assignment: dict, color: int) -> bool:
    for constraint in constraints:
        if assignment.get(constraint) is None:  # if not in assignment
            continue  # continue checking for next constraint variable
        if assignment.get(constraint).color == color:
            return False
    return True


def select_unassigned(assignment: dict, csp: CSP) -> Node:
    """
    selects variable that hasn't been assigned
    :param assignment: dictionary where key=variable and value=value(color)
    :param csp: instance of CSP class
    :return: Variable that hasn't been assigned (returns it as instance of Node)
    """
    for i in range(len(csp.constraints)):
        # check if i-th variable has been assigned and pick the next unassigned variable
        if assignment.get(i) is None:
            variable = Node(i, -1)
            return variable


def create_csp_problem(input_file, m) -> CSP:
    var_num, const_num, color_num = map(int, input_file.readline().split())
    constraints = [[] for i in range(var_num)]
    arcs = deque()
    color_domains = [[i for i in range(color_num)] for j in range(var_num)]
    for i in input_file:
        first, second = map(int, i.split())
        constraints[first].append(second)  # append second column to index of row (which is variable)
        constraints[second].append(first)
        if m == 1:
            arcs.append([first, second])
    return CSP(constraints, const_num, color_num, arcs, color_domains)


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
    # sys.setrecursionlimit(10000)

    input_file = ""
    output_file = ""
    m = 0

    if len(sys.argv) == 4:
        input_file = open(sys.argv[1], 'r')  # -> Input file path
        output_file = open(sys.argv[2], 'w')  # -> Output file paht
        m = int(sys.argv[3])  # -> plain dfsb || altered dfsb
    else:
        print(
            'Wrong number of arguments. Usage:\ndfsb.py <I> <> <H> '
            '<INPUT_FILE_PATH> <OUTPUT_FILE_PATH>>')
    csp = create_csp_problem(input_file, m)
    # if m == 1:
    #     csp.init_nodes()
    solution = dfs(csp, m)

    for i in range(len(solution)):
        print(solution[i].color)

        # script to check if soution is valid
    for i in range(len(solution)):
        for j in csp.constraints[i]:
            if solution[i].color == solution[j].color:
                print("False Failed")

    make_solution_file(solution)

    input_file.close()
    output_file.close()
