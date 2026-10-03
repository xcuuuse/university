# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def func(head: ListNode, k: int):
    if not head:
        return None
    current = head
    current2 = head.next
    while current2:
        current = current.next
        current2 = current2.next
    current2.next = head
    current.next = None
    head = current2

    return head


