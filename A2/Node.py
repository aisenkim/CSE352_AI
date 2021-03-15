class Node:
    def __init__(self, value: int, color: int, color_list: list = None):
        self.value = value
        self.color = color
        self.color_list = color_list

    def __lt__(self, other):
        return self.value < other.value
