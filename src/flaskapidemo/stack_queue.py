from typing import Any

import linked_list


class Queue(linked_list.LinkedList):
    def __init__(self) -> None:
        super().__init__()

    def enqueue(self, data: Any):
        self.append(data=data)

    def dequeue(self):
        return self.remove_head()


class Stack(linked_list.LinkedList):
    def __init__(self) -> None:
        super().__init__()
        self.top = self.head

    def peek(self):
        return self.top

    def push(self, data: Any):
        self.insert_beginning(data=data)

    def pop(self):
        return self.remove_head()
