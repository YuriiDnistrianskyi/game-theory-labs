class Node:
    def __init__(self, value: int, xy: list[int]):
        self.value = value
        self.xy = xy

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return self.value > other
