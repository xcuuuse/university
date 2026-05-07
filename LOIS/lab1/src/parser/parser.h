/*
* Лабораторная работа №1 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентом группы 421702 БГУИР Евик Алексей Николаевич
 */
/*
 * Объявляет интерфейс синтаксического анализатора:
 * метод разбора строки в дерево и вспомогательные методы для работы с позицией чтения.
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с.
 * Алгоритм - Метод рекурсивного спуска - URL: https://ru.wikibooks.org/Реализации_алгоритмов/Метод рекурсивного спуска
 * (дата обращения: 03.04.2026)
 */
#ifndef LAB1_PARSER_H
#define LAB1_PARSER_H
#include <set>
#include <string>
#include <memory>
#include <node/node.h>
#include <map>
class Parser {
public:
    std::set<std::string> variables;
    std::map<std::string, int> var_indices;
    std::shared_ptr<Node> parse(const std::string& input);
private:
    std::string src;
    int pos = 0;
    char current();
    char move_symbol();
    void expect(char c);
    std::shared_ptr<Node> parse_formula();

};
#endif //LAB1_PARSER_H
