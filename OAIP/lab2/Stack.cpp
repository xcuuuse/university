#include "Stack.h"
#include <iostream>

Stack::Stack() : head(nullptr) {}

// Добавление элемента в стек (FILO)
void Stack::add_node(int new_data) {
    Node* new_node = new Node(new_data);
    new_node->next = head; // Новый элемент указывает на текущую вершину
    head = new_node;       // Обновляем вершину стека

}

// Печать всех элементов стека
void Stack::print_data() {
    Node* current_node = head;
    while (current_node != nullptr) {
        std::cout << current_node->data << " ";
        current_node = current_node->next;
    }
    std::cout << std::endl;
}

// Поиск минимального элемента
Node* Stack::find_min() {
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

// Поиск максимального элемента
Node* Stack::find_max() {
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

// Удаление элементов между минимумом и максимумом
void Stack::remove_between_min_max() {
    Node* min_node = find_min();
    Node* max_node = find_max();

    if (min_node == nullptr || max_node == nullptr || min_node == max_node) {
        std::cout << "Nothing to remove.\n";
        return;
    }

    // Определяем порядок узлов в списке
    Node* first = nullptr;  // Указатель на первый узел в списке (меньший)
    Node* second = nullptr; // Указатель на второй узел в списке (больший)

    Node* current = head;
    while (current != nullptr) {
        if (current == min_node || current == max_node) {
            if (first == nullptr) {
                first = current; // Первый найденный узел
            } else {
                second = current; // Второй найденный узел
                break; // Мы нашли оба узла, выходим из цикла
            }
        }
        current = current->next;
    }

    current = head;
    Node* previous = nullptr;
    bool is_between = false;

    while (current != nullptr) {
        if (current == first) {
            is_between = true; // Начинаем удаление
        } else if (current == second) {
            break; // Заканчиваем удаление
        }

        if (is_between && current != first && current != second) {
            // Удаляем текущий узел
            if (previous != nullptr) {
                previous->next = current->next; // Пропускаем текущий узел
            } else {
                head = current->next;
            }
            Node* temp = current;
            current = current->next; // Переходим к следующему узлу
            delete temp; // Освобождаем память
        } else {
            // Просто переходим к следующему узлу
            previous = current;
            current = current->next;
        }
    }
}

/*void Stack::replace() {
    if (head == nullptr)
    {
        std::cout << "Nothing to replace\n";
        return;
    }
    Node* min_node = find_min();

    int temp = head->data;
    head->data = min_node->data;
    min_node->data = temp;
} */