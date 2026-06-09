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
    Queue* back  = nullptr;

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
    int index = 1;
    while (current)
    {
        Queue* current_next = current->next;
        if (index % 3 == 0)
        {
            if (current->next)
            {
                current->prev->next = current->next;
                current->next->prev = current->prev;
            }
            else
            {
                back = current->prev;
                back->next = nullptr;
            }
            delete current;
        }
        current = current_next;
        index++;
    }

    current = front;
    while (current)
    {
        cout << current->val << " ";
        current = current->next;
    }

    while (front)
    {
        Queue* temp = front;
        front = front->next;
        delete temp;
    }
}
