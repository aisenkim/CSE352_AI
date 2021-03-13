import sys
from Node import Node
from csp import CSP


def dfs(csp):
    """calls the recursive function dfs_backtrack()

    Args:
        csp (list): contains all the constraints 

    Returns:
        [list]: [list of nodes]
    """
    # return dfs_backtrack({}, csp)


# def dfs_backtrack(assignment, csp):
#     # if the assignment's length == M: variable number, then return assignment 
#     if len(assignment) == len(csp):
#         return assignment
#     # select idx of assignment 
#     node = select_unassigned(assignment, csp)


def create_csp_problem(input_file) -> CSP:
    var_num, const_num, color_num = map(int, input_file.readline().split())
    constraints = [[] for i in range(var_num)]
    unsigned_vars = [i for i in range(var_num)]

    for i in input_file:
        first, second = map(int, i.split())
        constraints[first].append(second)  # append second column to index of row (which is variable)
    return CSP(constraints, unsigned_vars)


if __name__ == "__main__":
    # N M K as first line in file
    # N: number of variable
    # M: number of constraints
    # K: possible colors
    # Rest of the lines are constraints 

    if len(sys.argv) == 4:
        input_file = open(sys.argv[1], 'r')  # -> Input file path
        output_file = open(sys.argv[2], 'w')  # -> Output file paht
        m = int(sys.argv[3])  # -> plain dfsb || altered dfsb
    else:
        print(
            'Wrong number of arguments. Usage:\ndfsb.py <I> <> <H> '
            '<INPUT_FILE_PATH> <OUTPUT_FILE_PATH>>')
    create_csp_problem(input_file)

    input_file.close()
    output_file.close()
