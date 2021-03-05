class Heuristics:
    def manhattan_d(self, cur_state, goal_state):
        """
        h1 -> implement manhattan distance algorithm
        :param cur_state: current state of board
        :param goal_state: dictionary containing goal state
        :return: summation of distance between each tile in cur_state & goal_state
        """
        h = 0  # sum of all distance
        for i in range(len(cur_state)):
            for j in range(len(cur_state[0])):
                value = cur_state[i][j]  # actual value # 1- 8
                goal_x, goal_y = goal_state[value]  # goal tile position (coordinate)
                # cur_x = i && cur_y = j
                h += abs(i - goal_x) + abs(j - goal_y)

        return h

    def hamming_d(self, cur_state, goal_state):
        """
        h2 -> implement hamming distance algorithm
        :param cur_state:  current state board
        :param goal_state:  goal state board
        :return: total number of tiles misplaced
        """
        h = 0  # num of tiles misplaced
        for i in range(len(cur_state)):
            for j in range(len(cur_state[0])):
                # 0 is empty space
                if cur_state[i][j] != goal_state[i][j] and cur_state != 0:
                    h += 1  # increment

        return h

