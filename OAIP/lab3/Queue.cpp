#include "Queue.h"
#include <iostream>

// конструктор
Queue::Queue() : head(nullptr) {}

// деструктор для освобождения памяти
Queue::~Queue() {
    Node* current = head;
    while (current != nullptr) {
        Node* temp = current;
        current = current->next;
        delete temp;
    }
}

// добавление элемента в начало списка
void Queue::add_node(int new_data) {
    Node* new_node = new Node(new_data);
    if (head == nullptr) {
        head = new_node; // если список пуст, новый узел становится головой
    } else {
        new_node->next = head; // новый узел указывает на текущую голову
        head->previous = new_node; // текущая голова указывает на новый узел как на предыдущий
        head = new_node;       // обновляем голову
    }
}
void Queue::add_node_to_end(int new_data) {
    Node* new_node = new Node(new_data);
    if (head == nullptr) {
        head = new_node; // Если список пуст, новый узел становится головой
    } else {
        Node* current = head;
        while (current->next != nullptr) {
            current = current->next; // Находим последний узел
        }
        current->next = new_node; // Последний узел указывает на новый узел
        new_node->previous = current; // Новый узел указывает на предыдущий как на previous
    }
}

// печать всех элементов списка
void Queue::print_data() {
    Node* current = head;
    while (current != nullptr) {
        std::cout << current->data << " ";
        current = current->next;
    }
    std::cout << std::endl;
}

// поиск минимального элемента
Node* Queue::find_min() {
    if (head == nullptr) {
        return nullptr;
    }
    Node* min_node = head;
    Node* current = head;
    while (current != nullptr) {
        if (current->data < min_node->data) {
            min_node = current;
        }
        current = current->next;
    }
    return min_node;
}

// поиск максимального элемента
Node* Queue::find_max() {
    if (head == nullptr) {
        return nullptr;
    }
    Node* max_node = head;
    Node* current = head;
    while (current != nullptr) {
        if (current->data > max_node->data) {
            max_node = current;
        }
        current = current->next;
    }
    return max_node;
}

void Queue::remove_between_min_max() {
    Node* min_node = find_min();
    Node* max_node = find_max();

    if (min_node == nullptr || max_node == nullptr || min_node == max_node) {
        std::cout << "Nothing to remove.\n";
        return;
    }

    // определяем порядок узлов в списке
    Node* first = nullptr;  // указатель на первый узел в списке (меньший)
    Node* second = nullptr; // указатель на второй узел в списке (больший)

    // находим порядок: min -> max или max -> min
    Node* current = head;
    bool order_set = false;

    while (current != nullptr && !order_set) {
        if (current == min_node || current == max_node) {
            first = current;
            current = current->next;
            while (current != nullptr) {
                if (current == min_node || current == max_node) {
                    second = current;
                    order_set = true;
                    break;
                }
                current = current->next;
            }
        } else {
            current = current->next;
        }
    }

    if (!order_set) {
        std::cout << "Min and Max nodes are not in the list or are adjacent.\n";
        return;
    }

    // Начинаем удаление элементов между first и second
    current = first->next;

    while (current != second) {
        Node* temp = current;
        if (temp->previous != nullptr) {
            temp->previous->next = temp->next;
        }
        if (temp->next != nullptr) {
            temp->next->previous = temp->previous;
        }
        current = temp->next; // Переходим к следующему узлу
        delete temp;          // Освобождаем память
    }
}

// Замена местами второго с последним и первого с предпоследним элементом
void Queue::swap_elements() {
    if (head == nullptr || head->next == nullptr) {
        std::cout << "Not enough elements to perform swap.\n";
        return;
    }

    // Находим первый, второй, предпоследний и последний узлы
    Node* first = head;
    Node* second = head->next;

    Node* current = head;
    Node* last = nullptr;
    Node* pre_last = nullptr;

    while (current != nullptr) {
        if (current->next == nullptr) {
            last = current;
        } else if (current->next->next == nullptr) {
            pre_last = current;
        }
        current = current->next;
    }

    if (last == nullptr || pre_last == nullptr) {
        std::cout << "Not enough elements to perform swap.\n";
        return;
    }

    // Меняем местами второй и последний элементы
    swap_nodes(second, last);

    // Меняем местами первый и предпоследний элементы
    swap_nodes(first, pre_last);
}

// Вспомогательная функция для обмена двух узлов
void Queue::swap_nodes(Node* node1, Node* node2) {
    if (node1 == nullptr || node2 == nullptr || node1 == node2) {
        return;
    }

    // Сохраняем соседей узлов
    Node* prev1 = node1->previous;
    Node* next1 = node1->next;
    Node* prev2 = node2->previous;
    Node* next2 = node2->next;

    // Обновляем связи для node1
    if (prev1 != nullptr) {
        prev1->next = node2;
    } else {
        head = node2; // Если node1 был головой, теперь голова — node2
    }
    if (next1 != nullptr) {
        next1->previous = node2;
    }

    // Обновляем связи для node2
    if (prev2 != nullptr) {
        prev2->next = node1;
    } else {
        head = node1; // Если node2 был головой, теперь голова — node1
    }
    if (next2 != nullptr) {
        next2->previous = node1;
    }

    // Меняем указатели previous и next узлов
    node1->previous = prev2;
    node1->next = next2;
    node2->previous = prev1;
    node2->next = next1;
}




