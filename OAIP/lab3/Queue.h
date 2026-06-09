#ifndef LAB2_QUEUE_H
#define LAB2_QUEUE_H
#include <iostream>

struct Node {
    int data;
    Node* next;
    Node* previous; // Указатель на предыдущий узел
    Node(int new_data) : data(new_data), next(nullptr), previous(nullptr) {}
};

class Queue {
private:
    Node* head; // Головной узел списка
public:
    Queue();
    ~Queue(); // Деструктор для освобождения памяти
    void add_node(int new_data); // Добавление элемента в начало списка
    void add_node_to_end(int new_data);
    void print_data(); // Печать всех элементов списка
    void remove_between_min_max(); // Удаление элементов между минимумом и максимумом
    void swap_elements();
    void swap_nodes(Node* node1, Node* node2);
private:
    Node* find_min(); // Поиск минимального элемента
    Node* find_max(); // Поиск максимального элемента
};

#endif //LAB2_QUEUE_H