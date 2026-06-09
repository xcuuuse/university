/*
 * Лабораторная работа №1 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентом группы 421702 БГУИР Евик Алексей Николаевич
*/

/*
 * Содержит алгоритм рекурсивного спуска для разбора формул сокращённого языка логики высказываний и построения
 * абстрактного дерева.
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с.
 *     Алгоритм - Метод рекурсивного спуска - URL: https://ru.wikibooks.org/Реализации_алгоритмов/Метод рекурсивного спуска
 * (дата обращения: 03.04.2026)
 */
#include "parser.h"
#include <memory>


//пробелы фикс, язык сокращенный, в отчет добавлять время

/*Реализует обработку формулы сокращенного языка логики высказываний*/
std::shared_ptr<Node> Parser::parse(const std::string &input) {
    src = input;
    pos = 0;
    variables.clear();
    var_indices.clear();
    auto root = parse_formula();
    if (pos != (int)src.size()) {
        throw std::invalid_argument(
            "Некорректная формула сокращенного языка логики высказываний");
    }
    return root;
}

/*Позволяет обратиться к текущему символу выражения*/
char Parser::current() {
    return (pos < (int)src.size()) ? src[pos] : '\0';
}

/*Позволяет перейти на символ вперед*/
char Parser::move_symbol() {
    if (pos >= (int)src.size()) {
        throw std::invalid_argument("Неожиданный конец строки");
    }
    return src[pos++];
}


/*Ожидает на выходе определенный символ, если он не совпадает с ожидаемым - выбрасывается ошибка*/
void Parser::expect(char c) {
    if (current() != c) {
        throw std::invalid_argument("Некорректная формула сокращенного языка логики высказываний");
    }
    move_symbol();
}

/*Позволяет построить дерево по формуле для корректной обработки*/
std::shared_ptr<Node> Parser::parse_formula() {
    char c = current();
    /*Ожидание открывающей скобки*/
    if (c == '(') {
        int start_pos = pos;
        move_symbol();
        std::shared_ptr<Node> node;
        /*Отрицание*/
        if (current() == '!') {
            move_symbol();
            auto child = parse_formula();
            node = std::make_shared<Node>();
            node->kind = NodeKind::Neg;
            node->left = child;
        }
        else {

            auto left = parse_formula();
            node = std::make_shared<Node>();
            node->left = left;
            switch (current()) {
                /*Конъюнкция*/
                case '/':
                    if (pos + 1 < (int)src.size() && src[pos + 1] == '\\') {
                        pos += 2;
                        node->kind  = NodeKind::And;
                        node->right = parse_formula();
                    } else {
                        throw std::invalid_argument(
                            "Некорректная формула сокращенного языка логики высказываний");
                    }
                    break;
                    /*Дизъюнкция*/
                case '\\':
                    if (pos + 1 < (int)src.size() && src[pos + 1] == '/') {
                        pos += 2;
                        node->kind  = NodeKind::Or;
                        node->right = parse_formula();
                    } else {
                        throw std::invalid_argument(
                            "Некорректная формула сокращенного языка логики высказываний");
                    }
                    break;
                case '~':
                    /*Эквиваленция*/
                    move_symbol();
                    node->kind = NodeKind::Equiv;
                    node->right = parse_formula();
                    break;
                    /*Импликация*/
                case '-':
                    move_symbol();
                    if (current() != '>') {
                        throw std::invalid_argument("Некорректная формула сокращенного языка логики высказываний");
                    }
                    move_symbol();
                    node->kind = NodeKind::Impl;
                    node->right = parse_formula();
                    break;
                default:
                    throw std::invalid_argument(
                "Некорректная формула сокращенного языка логики высказываний");
            }
        }
        expect(')');
        node->text = src.substr(start_pos, pos - start_pos);
        return node;
    }
    /*Логические константы*/
    if (c == '0' || c == '1') {
        int start_pos = pos;
        move_symbol();
        auto node   = std::make_shared<Node>();
        node->kind  = NodeKind::Const;
        node->value = (c == '1');
        node->text  = src.substr(start_pos, pos - start_pos);
        return node;
    }

    if (std::isupper((unsigned char)c) && c != '\0') {
        int start_pos = pos;
        std::string name;
        name += move_symbol();
        variables.insert(name);
        auto it = var_indices.find(name);
        int idx;
        if (it == var_indices.end()) {
            idx = (int)var_indices.size();
            var_indices[name] = idx;
        } else {
            idx = it->second;
        }

        auto node = std::make_shared<Node>();
        node->kind = NodeKind::Var;
        node->name = name;
        node->var_index = idx;
        node->text = src.substr(start_pos, pos - start_pos);
        return node;
    }
    throw std::invalid_argument(
        "Некорректная формула сокращенного языка логики высказываний");
}




