#include <iostream>
using namespace std;

struct Stack {
    int val;
    Stack* next;
};

int main() {
    Stack *top = nullptr;
    Stack* otr = nullptr;
    for (int i = 0; i < 8; i++) {
        int num;
        cin >> num;
        if (num < 0)
        {
            Stack* node = new Stack;
            node->val = num;
            node->next = otr;
            otr = node;
        }
        else
        {
            Stack* node = new Stack;
            node->val = num;
            node->next = top;
            top = node;
        }
    }

    Stack* current = top;
    while (current)
    {
        cout << current->val << " ";
        current = current->next;
    }
    cout << "\n";
    current = otr;
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
    while (otr)
    {
        Stack* temp = otr;
        otr = otr->next;
        delete temp;
    }
}
