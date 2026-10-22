# Definition for singly-linked list.
from jupyter_builder import jlpm


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def func(head: ListNode):
    if not head or head.next:
        pass


def show(head: ListNode):
    while(head):
        print(f"{head.val}->", end="")
        head = head.next


def main():
    arr = list(map(int, input().split()))
    print(sorted(arr)[1])