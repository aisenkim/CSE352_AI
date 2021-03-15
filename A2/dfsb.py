import sys
from Node import Node
from csp import CSP


def dfs(csp: CSP, m: int) -> dict:
    """
    call normal dfs if m == 0
    otherwise call dfs++
    :param csp: instnace of CSP
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
    # select Most Constrained Variable
    variable: Node = csp.unsigned_vars.get()[1]
    #  find least constraining value(color)
    color_count: list = csp.set_LCV(assignment)  # holds count of each color used by already assigned variables
    while len(color_count) > 0:
        # get color that is used least by variables already assigned
        # (which are most constrained)
        value = color_count.pop(color_count.index(min(color_count)))
        # --------------------------------------------------------------------------------------------
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
            #  put it back to unassigned_vars
            csp.unsigned_vars.put((-len(csp.constraints[var_num]), Node(i, -1)))
    return {}  # return failure (should it be {} or assignment???)


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


def create_csp_problem(input_file) -> CSP:
    var_num, const_num, color_num = map(int, input_file.readline().split())
    constraints = [[] for i in range(var_num)]
    unsigned_vars = None  # set as priority queue in csp.py (for MCV)

    for i in input_file:
        first, second = map(int, i.split())
        constraints[first].append(second)  # append second column to index of row (which is variable)
        constraints[second].append(first)
    return CSP(constraints, unsigned_vars, const_num, color_num)


if __name__ == "__main__":
    # N M K as first line in file
    # N: number of variable
    # M: number of constraints
    # K: possible colors
    # Rest of the lines are constraints

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
    csp = create_csp_problem(input_file)
    if m == 1:
        csp.set_MCV()
    solution = dfs(csp, m)

    for i in range(len(solution)):
        print(solution[i].color)

    input_file.close()
    output_file.close()
