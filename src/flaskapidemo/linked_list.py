from __future__ import annotations
from typing import Any


class Node:
    def __init__(self, data=None):
        """Create a node for linked list.

        Args:
            data (Any, optional): Data of the node. Defaults to None.
        """
        self.data: Any = data
        self.next_node: Node = None

    def store(self, data, replace=False):
        if self.data is not None and replace is False:
            raise ValueError(
                "Node already has data. Set `replace=True` in the arguments"
            )
        else:
            self.data = data

    def point_to(self, node: Node):
        self.next_node = node


class linked_list:
    def __init__(self) -> None:
        self.head: Node = None
        self.end: Node = None
        self.length: int = 0

    def print_list(self):
        """
        print_list Print all elements in the list.

        Print all elements in the list.
        """
        ll_string = ""
        node = self.head

        if node is None:
            print("List is empty.")
        else:
            while node is not None:
                ll_string += f"{str(node.data)} -> "
                if node.next_node is None:
                    ll_string += "END"
                node = node.next_node

            print(ll_string)

    def append(self, node: Node):

        if self.head is None and self.end is None:
            self.head = node
            self.end = node
        else:
            self.end.next_node = node
            self.end = node

        self.end.next_node = None
        self.length += 1

    def insert_beginning(self, node: Node):
        pass


# -------------------------------------------------------------------------- #


def main():
    myLinkedList = linked_list()
    myLinkedList.append(node=Node(data="first"))
    myLinkedList.append(node=Node(data="second"))
    myLinkedList.append(node=Node(data="third"))

    myLinkedList.print_list()


if __name__ == "__main__":
    main()
