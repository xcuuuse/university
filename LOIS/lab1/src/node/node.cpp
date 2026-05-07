/*
 * Лабораторная работа №1 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентом группы 421702 БГУИР Евик Алексей Николаевич
 */

/*
 * Содержит рекурсивную функцию для вычисления значения формулы при заданной интерпретации переменных.
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с.
 *     Алгоритм - Метод рекурсивного спуска - URL: https://ru.wikibooks.org/Реализации_алгоритмов/Метод рекурсивного спуска
 * (дата обращения: 03.04.2026)
 */
#include "node.h"

bool Node::eval(const std::vector<bool>& interp) const {
    switch (kind) {
        case NodeKind::Var:
            return interp[var_index];
        case NodeKind::Const:
            return value;
        case NodeKind::Neg:
            return !left->eval(interp);
        case NodeKind::Or:
            return left->eval(interp) || right->eval(interp);
        case NodeKind::And:
            return left->eval(interp) && right->eval(interp);
        case NodeKind::Equiv:
            return left->eval(interp) == right->eval(interp);
        case NodeKind::Impl:
            return !left->eval(interp) || right->eval(interp);
    }
    return false;
}

