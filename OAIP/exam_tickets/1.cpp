#include <iostream>
using namespace std;

struct Stack {
    int val;
    Stack* next;
};

int main() {
    Stack *top = nullptr;
    
    for (int i = 0; i < 7; i++) {
        int num;
        cin >> num;
        Stack* node = new Stack;
        node->val = num;
        node->next = top;
        top = node;
    }

    Stack* max_prev = nullptr;
    Stack* max_node = top;
    Stack* cur = top;

    while (cur->next)
    {
        if (cur->next->val > max_node->val)
        {
            max_node = cur->next;
            max_prev = cur;
        }
        cur = cur->next;
    }

    if (max_node == top->next)
    {
        top->next = max_node->next;
        max_node->next = top;
        top = max_node;
    }

    else
    {
        Stack* temp = top->next;
        top->next = max_node->next;
        max_prev->next = top;
        max_node->next = temp;
        top = max_node;
    }


    Stack* current = top;
    while (current)
    {
        cout << current->val << " ";
        current = current->next;
    }
    while (top) {
        Stack* temp = top;
        top = top->next;
        delete temp;

    }
}
