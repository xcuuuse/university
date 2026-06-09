#ifndef LAB1_STACK_H
#define LAB1_STACK_H
#include "iostream"
struct Node{
    int data;
    Node* next;

    Node(int new_data) : data(new_data), next(nullptr){}
};

class Stack{
private:
    Node* head;
public:
    Stack();
    void add_node(int new_data);
    void print_data();
    void remove_between_min_max();
    void replace();
private:
    Node* find_min();
    Node* find_max();
};
#endif //LAB1_STACK_H
