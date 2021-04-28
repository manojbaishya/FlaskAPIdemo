from __future__ import annotations
from typing import Any, List

import linked_list


class Data:
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value

    @staticmethod
    def match(node_data: Data, probe: str):
        return True if node_data.key == probe else False


class HashTable:
    def __init__(self, table_size):
        self.size = table_size
        self.table: List[linked_list.LinkedList] = [None] * table_size

    def hash(self, key: str) -> int:
        index = 0
        for ch in key:
            index += ord(ch)
            index = (index * ord(ch)) % self.size
        return index

    def insert(self, key: str, value: Any):
        index = self.hash(key)
        if self.table[index] is None:
            self.table[index] = linked_list.LinkedList()
            self.table[index].append(data=Data(key, value))
        else:
            self.table[index].append(data=Data(key, value))

    def search(self, key: str):
        index = self.hash(key)
        if self.table[index] is not None:
            data = self.table[index].search(attr=key, match=Data.match)
            if data is not None:
                return data.value
        return None

    def print(self):
        print("[")
        for i, llist in enumerate(self.table):
            if llist is not None:
                ll_string = ""
                node = llist.head
                while node is not None:
                    ll_string += f"{str(node.data.key)}: {str(node.data.value)} --> "
                    if node.next_node is None:
                        ll_string += "END"
                    node = node.next_node

                print(f"\t{i} = {{{ll_string}}}".expandtabs(4))
            else:
                print(f"\t{i} = None".expandtabs(4))
        print("]")
