/*
 * Лабораторная работа №1 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентом группы 421702 БГУИР Евик Алексей Николаевич
 */
/*
 *  Файл node.h.
 *  Описывает один узел дерева формулы и типы операций
 *  (переменная, константа, отрицание, конъюнкция, дизъюнкция, импликация, эквиваленция).
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с.
 *     Алгоритм - Метод рекурсивного спуска - URL: https://ru.wikibooks.org/Реализации_алгоритмов/Метод рекурсивного спуска
 * (дата обращения: 03.04.2026)
 */
#ifndef LAB1_NODE_H
#define LAB1_NODE_H
#include <string>
#include <memory>
#include <vector>
enum class NodeKind {
    Var,
    Const,
    Neg,
    And,
    Or,
    Impl,
    Equiv
};

struct Node {
    NodeKind kind;
    std::string name;
    std::string text;
    bool value = false;
    int var_index = -1;
    std::shared_ptr<Node> left;
    std::shared_ptr<Node> right;
    bool eval(const std::vector<bool>& interp) const;
};
#endif //LAB1_NODE_H
