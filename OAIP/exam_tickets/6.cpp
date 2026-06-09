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

    int inserts[3];
    for (int i = 0; i < 3; i++)
    {
        cin >> inserts[i];
    }
    Queue* current = front;

    int index = 1, insert = 0;

    while (current and insert < 3)
    {
        if (index % 3 == 0)
        {
            Queue* new_node = new Queue{inserts[insert], current, current->prev};

            current->prev->next = new_node;
            current->prev = new_node;

            insert++;
            current = current->next;
            index++;

        }
        else
        {
            current = current->next;
            index++;
        }
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
