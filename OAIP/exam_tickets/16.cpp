#include <iostream>
using namespace std;

struct Stack {
    int val;
    Stack* next;
};

int main() {
    Stack* top = nullptr;
    Stack* positive = nullptr;
    for (int i = 0; i < 7; i++)
    {
        int num; cin >> num;
        if (num > 0)
        {
            Stack* node = new Stack;
            node->val = num;
            node->next = positive;
            positive = node;
        }
    }

    Stack* current = positive;
    while (current)
    {
        cout << current->val << " ";
        current = current->next;
    }

    while (positive)
    {
        Stack* temp = positive;
        positive = positive->next;
        delete temp;
    } 





}
