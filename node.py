class Node:
    def __init__(self, data, left=None, right=None):
        self.left = left
        self.right = right
        self.data = data

    def __str__(self):
        return "({data}, {left}, {right})".format(data=self.data, left=self.left, right=self.right)
