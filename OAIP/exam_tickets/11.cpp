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

    for (int i = 0; i < 7; i++)
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
    Queue* frontpos = nullptr;
    Queue* backpos = nullptr;

    Queue* current  = front;
    int index = 1;
    while (current)
    {
        if (index % 2 == 0)
        {
            Queue* newnode = new Queue{current->val, nullptr, backpos};
            if (!backpos)
            {
                frontpos = backpos = newnode;
            }
            else
            {
                backpos->next = newnode;
                backpos = newnode;
            }
        }
        current = current->next;
        index++;
    }

    current = frontpos;
    while (current)
    {
        cout << current->val << " "; current = current->next;
    }
    while (frontpos)
    {
        Queue* temp = frontpos;
        frontpos = frontpos->next;
        delete temp;
    }
    while (front)
    {
        Queue* temp = front;
        front = front->next;
        delete temp;
    }
}
