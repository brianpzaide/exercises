from __future__ import annotations
from collections import deque

class Node:
    def __init__(self, val: int, prev: Node | None = None, next: Node | None = None, child: Node | None = None):
        self._val = val
        self._prev = prev
        self._next = next
        self._child = child

    @property
    def val(self) -> int:
        return self._val

    @val.setter
    def val(self, val: int):
        if not isinstance(val, (int,)):
            raise TypeError("val must be an int")
        self._val = val

    @property
    def prev(self) -> Node | None:
        return self._prev

    @prev.setter
    def prev(self, value: Node | None):
        if not isinstance(value, (Node, type(None))):
            raise TypeError("prev must be a Node or None")
        self._prev = value

    @property
    def next(self) -> Node | None:
        return self._next

    @next.setter
    def next(self, value: Node | None):
        if not isinstance(value, (Node, type(None))):
            raise TypeError("next must be a Node or None")
        self._next = value

    @property
    def child(self) -> Node | None:
        return self._child

    @child.setter
    def child(self, value: Node | None):
        if not isinstance(value, (Node, type(None))):
            raise TypeError("child must be a Node or None")
        self._child = value


def flatten_multilevel_linked_list_recursive(head: Node | None) -> Node:
    if not head:
        return None
    runner = head
    while runner is not None:
        if runner.child is not None:
            flattened = flatten_multilevel_linked_list_recursive(runner.child)

            temp = runner.next
            
            runner.next = flattened
            flattened.prev = runner
            
            while flattened.next is not None:
                flattened = flattened.next

            if temp:
                flattened.next = temp
                temp.prev = flattened

            runner.child = None

        runner = runner.next
    
    return head 

def flatten_multilevel_linked_list_iterative(head: Node | None) -> Node:
    if not head:
        return None
    stack_ = deque()
    runner = head
    while runner is not None:
        if runner.child is not None:
            child_ = runner.child

            if runner.next is not None:
                stack_.append(runner.next)
            
            runner.next = child_
            child_.prev = runner
            
        if (runner.next is None) and len(stack_) > 0:
            temp = stack_.pop()
            runner.next = temp
            temp.prev = runner
        
        runner = runner.next
    
    return head     

def print_linked_list(head: Node| None):
    runner = head
    sofar = ""
    while runner is not None:
        sofar += f"{runner.val} -> "
        runner = runner.next
    sofar += "None"
    print(sofar)

def main():
    node1 = Node(val=1)
    node2 = Node(val=2)
    node3 = Node(val=3)
    node4 = Node(val=4)
    node5 = Node(val=5)
    node6 = Node(val=6)
    node7 = Node(val=7)
    node8 = Node(val=8)
    node9 = Node(val=9)
    node10 = Node(val=10)
    node11 = Node(val=11)
    node12 = Node(val=12)
    node13 = Node(val=13)
    
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node6
    node7.next = node8
    node8.next = node9
    node9.next = node10
    node11.next = node12

    node3.child = node7
    node8.child = node11

    node12.child = node13

    head = flatten_multilevel_linked_list_iterative(node1)
    print_linked_list(head)


if __name__ == '__main__':
    main()
    
