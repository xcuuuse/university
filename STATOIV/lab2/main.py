# Definition for singly-linked list.
from jupyter_builder import jlpm


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def func(head: ListNode):
    if not head or not head.next:
        return head
    current = head
    if current.next.val == current.val:
        pass


def show(head: ListNode):
    while(head):
        print(f"{head.val}->", end="")
        head = head.next



def main():
    n = int(input())
    ans = {}
    for _ in range(n):
        s = str(input())
        ans[s.split()[0]] = s.split()[1]
    new_s = str(input())
    if new_s in ans.keys():
        print(ans[new_s])
    else:
        for i in ans.keys():
            if ans[i] == new_s:
                print(i)


if __name__ == '__main__':
    main()
