#include "iostream"

using namespace std;

struct Queue{
    int val;
    Queue* next;
    Queue* prev;
};

int main()
{
    Queue* front = nullptr;
    Queue* back = nullptr;

    for (int i = 0; i < 9; i++)
    {
        int num; cin >> num;
        Queue* node = new Queue{num, nullptr, back};
        if (!back)
        {
            front = back = node;
        }
        else
        {
            back->next = node;
            back = node;
        }
    }
    Queue* current = front;
    while (current)
    {
        Queue* next_current = current->next;
        if (current->val % 2 == 0)
        {
            if (current->next)
            {
                current->next->prev = current->prev;
            }
            else back = current->prev;
            if (current->prev)
            {
                current->prev->next = current->next;
            }
            else front = current->next;

            delete current;
        }
        current = next_current;
    }

    current = front;
    while (current)
    {
        cout << current->val << " "; current = current->next;
    }

    while (front)
    {
        Queue* temp = front;
        front = front->next;
        delete temp;
    }


}
