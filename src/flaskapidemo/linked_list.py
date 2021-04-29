from __future__ import annotations
from typing import Any, Callable


def errstr(error):
    return "\033[1;31m" + error + "\033[0m"


class Node:
    def __init__(self, data=None, next_node=None):
        """Create a node for linked list.

        Args:
            data (Any, optional): Data of the node. Defaults to None.
        """
        self.data: Any = data
        self.next_node: Node = next_node

    def store(self, data, replace=False):
        if self.data is not None and replace is False:
            raise ValueError(
                errstr("Node already has data. Set ")
                + "`replace=True`"
                + errstr(" in the arguments.")
            )
        else:
            self.data = data

    def nxtpoint_to(self, node: Node):
        self.next_node = node


class LinkedList:
    def __init__(self) -> None:
        self.head: Node = None
        self.end: Node = None
        self.length: int = 0
        self.match_fnc = None

    def append(self, data=None, node: Node = None):

        if data is None and node is not None:
            if self.head is None and self.end is None:
                # Insert node in an empty list
                self.head = self.end = node
            else:
                self.end.nxtpoint_to(node)
                self.end = self.end.next_node

            self.end.nxtpoint_to(None)
            self.length += 1
        elif data is not None and node is None:
            new_node = Node(data=data, next_node=None)
            if self.head is None and self.end is None:
                # Insert data in an empty list
                self.head = self.end = new_node
            else:
                self.end.nxtpoint_to(new_node)
                self.end = self.end.next_node
            self.length += 1
        else:
            raise ValueError(
                errstr(
                    "Either one of the data or node arguments needs to passed (but not both)."
                )
            )

    def insert_beginning(self, data=None, node: Node = None):
        if data is None and node is not None:
            node.nxtpoint_to(self.head)
            if self.head is None and self.end is None:
                # Insert node in an empty list
                self.head = self.end = node
            else:
                self.head = node
            self.length += 1
        elif data is not None and node is None:
            if self.head is None and self.end is None:
                # Insert data in an empty list
                new_node = Node(data=data, next_node=None)
                self.head = self.end = new_node
            else:
                new_node = Node(data=data, next_node=self.head)
                self.head = new_node
            self.length += 1
        else:
            raise ValueError(
                errstr(
                    "Either one of the data or node arguments needs to passed (but not both)."
                )
            )

    def remove_head(self):
        if self.head is None:
            return None

        removed_node = self.head
        # Head removed by garbage collection
        self.head = self.head.next_node

        if self.head is None:
            self.end = None

        self.length -= 1
        return removed_node.data

    def search(self, attr, match: Callable):
        cursor = self.head
        if cursor is None:
            return None
        else:
            while cursor is not None:
                if match(cursor.data, attr) is True:
                    return cursor.data
                cursor = cursor.next_node
        return None

    def traverse_list(self):
        """
        traverse_list demo logic for traversing the linked list

        Template for other methods.
        """
        cursor = self.head
        if cursor is None:
            # raise error message: List is empty
            return
        else:
            while cursor is not None:
                # do something with node.data pointed to by cursor
                cursor = cursor.next_node

    def print(self):
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

    def to_list(self):
        list_repr = []
        if self.head is not None and self.end is not None:
            # create list when linked list is not empty
            cursor = self.head
            while cursor is not None:
                list_repr.append(cursor.data)
                cursor = cursor.next_node
        return list_repr


# ---------------------------------------------------------------------------- #
#                                 Tests Function                               #
# ---------------------------------------------------------------------------- #
