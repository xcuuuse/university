#include "iostream"

using namespace std;

struct Queue {
    char val;
    Queue* next;
    Queue* prev;
};

int main()
{
    Queue* front = nullptr;
    Queue* back = nullptr;

    // Ввод 7 символов
    for (int i = 0; i < 7; i++) {
        char s;
        cin >> s;
        Queue* node = new Queue{s, nullptr, back};
        if (!back) {
            front = back = node;
        } else {
            back->next = node;
            back = node;
        }
    }

    // Вставка в середину
    int len = 7;
    int index = len / 2; // середина
    Queue* current = front;
    for (int i = 0; i < index; i++) {
        current = current->next;
    }

    Queue* new_node = new Queue{'w', current, current->prev};
    current->prev->next = new_node;
    current->prev = new_node;

    // Вывод
    current = front;
    while (current) {
        cout << current->val << " ";
        current = current->next;
    }

    // Очистка памяти
    while (front) {
        Queue* temp = front;
        front = front->next;
        delete temp;
    }

    return 0;
}
