from typing import List, Union
class Node:
    def __init__(self, data: str = None, left: Union[None, str, 'Node', List['Node']] = None, right: Union[None, str, 'Node', List['Node']] = None) -> None:
        self.left = left
        self.right = right
        self.data = data

    def __str__(self) -> str:
        return "({data}, (left, {left}, right, {right}))".format(data=self.data, left=self.left, right=self.right)

    def __repr__(self) -> str:
        return str(self)

class IfElseNode(Node):

    def __init__(self, data: str = None, left: Union[None, str, 'Node', List['Node']] = None, center: Union[None, str, 'Node', List['Node']] = None, right: Union[None, str, 'Node', List['Node']] = None) -> None:
        super().__init__(data, left, right)
        self.center = center

    def __str__(self) -> str:
        return "({data}, (left, {left}, center, {center}, right, {right}))".format(data=self.data, left=self.left, center=self.center, right=self.right)

    def __repr__(self) -> str:
        return str(self)