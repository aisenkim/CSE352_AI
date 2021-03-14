class Node:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __lt__(self, other):
        return self.value < other.value
