#include <iostream>
using namespace std;

struct Stack {
    int val;
    Stack* next;
};

int main() {
    Stack* top = nullptr;
    for (int i = 0; i < 5; i++)
    {
        int num; cin >> num;
        Stack* node = new Stack;
        node->val = num;
        node->next = top;
        top = node;
    }
    Stack* current = top;

    while (current)
    {
        cout << current->val << " ";
        current = current->next;
    }
    cout << "\n";
    current = top;
    while (current->next->next->next)
    {
        current = current->next;
    }
    Stack* target = current->next;
    current->next = current->next->next;
    delete target;
    current = top;
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
