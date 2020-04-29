class Node:
    def __init__(self, data=None, left=None, right=None):
        self.left = left
        self.right = right
        self.data = data

    def __str__(self):
        return "({data}, (left, {left}, right, {right}))".format(data=self.data, left=self.left, right=self.right)

    def __repr__(self):
        return str(self)
