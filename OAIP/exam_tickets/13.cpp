#include <iostream>
using namespace std;

struct Stack {
    int val;
    Stack* next;
};

int main() {
    Stack* first = nullptr;
    Stack* second = nullptr;

    for (int i = 0; i < 3; i++)
    {
        int num; cin >> num;
        Stack* node = new Stack;
        node->val = num;
        node->next = first;
        first = node;
    }

    for (int i = 0; i < 4; i++)
    {
        int num; cin >> num;
        Stack* node = new Stack;
        node->val = num;
        node->next = second;
        second = node;
    }

    Stack* current = first;
    int n; cin >> n;
    if (n < 3 && n >= 0)
    {
        for (int i = 0; i < n; i++)
        {
            current = current->next;
        }
        Stack* ost = current->next;
        Stack* second_end = second;
        while (second_end->next)
        {
            second_end = second_end->next;
        }
        current->next = second;
        second_end->next = ost;

    }
    else
    {
        cout << "Wrong pos\n";
        return 0;
    }

    current = first;
    while (current)
    {
        cout << current->val << " ";
        current = current->next;
    }
}
