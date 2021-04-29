from typing import Any, Callable


class Node:
    def __init__(self, data: Any = None) -> None:
        self.data: Any = data
        self.left_child: Node = None
        self.right_child: Node = None


class BinarySearchTree:
    def __init__(self) -> None:
        self.root_node: Node = None

    def insert(self, data: Any, node: Node = None, compare: Callable = None):
        if self.root_node is None:
            self.root_node = Node(data=data)
        elif self.root_node is not None and node is None:
            self.insert(data=data, node=self.root_node, compare=compare)
        else:
            if compare(data, node.data) < 0:
                if node.left_child is None:
                    node.left_child = Node(data=data)
                else:
                    self.insert(data=data, node=node.left_child, compare=compare)
            elif compare(data, node.data) > 0:
                if node.right_child is None:
                    node.right_child = Node(data=data)
                else:
                    self.insert(data=data, node=node.right_child, compare=compare)
            else:
                return

    def search(self, key: int, node: Node = None, compare: Callable = None):
        if self.root_node is None:
            return None
        elif self.root_node is not None and node is None:
            return self.search(key=key, node=self.root_node, compare=compare)
        else:
            if compare(key, node.data) == 0:
                return node.data
            if compare(key, node.data) < 0 and node.left_child is not None:
                return self.search(key=key, node=node.left_child, compare=compare)
            if compare(key, node.data) > 0 and node.right_child is not None:
                return self.search(key=key, node=node.right_child, compare=compare)

            return None
