#include <iostream>
using namespace std;

struct Stack {
    int val;
    Stack* next;
};

int main() {
    Stack *top = nullptr;
    for (int i = 0; i < 6; i++)
    {
        int num; cin >> num;
        Stack* node = new Stack;
        node->val = num;
        node->next = top;
        top = node;
    }

    Stack* current = top;
    Stack* plus = nullptr;
    Stack* last = nullptr;

    while (current)
    {
        if (current->val > 0)
        {
            Stack* new_node = new Stack;
            new_node->val = current->val;
            new_node->next = nullptr;

            if (plus == nullptr)
            {
                plus = new_node;
                last = plus;

            }
            else
            {
                last->next = new_node;
                last = new_node;
            }
        }
        current = current->next;
    }

    current = plus;
    while (current)
    {
        cout << current->val << " ";
        current = current->next;
    }
    while (top)
    {
        Stack* temp = top;
        top = top->next;
        delete temp;
    }

    while (plus)
    {
        Stack* temp = plus;
        plus = plus->next;
        delete temp;
    }
}
