/*
 * Лабораторная работа №1 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентом группы 421702 БГУИР Евик Алексей Николаевич
 * Точка входа программы.
 * Содержит главный цикл взаимодействия с пользователем,
 * обработку ввода формулы, построение таблицы истинности и вывод результата проверки на выполнимость.
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с.
 *     Алгоритм - Метод рекурсивного спуска - URL: https://ru.wikibooks.org/Реализации_алгоритмов/Метод рекурсивного спуска
 * (дата обращения: 03.04.2026)
 */


#include <node/node.h>
#include <parser/parser.h>
#include <vector>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <memory>
#include <windows.h>
using namespace std;

bool build_truth_table(const shared_ptr<Node>& root,
    const set<string>& var_set,
    const map<string, int>& var_indices,
    const string& formula_text) {

    vector vars(var_set.begin(), var_set.end());
    int n = (int)vars.size();
    long long rows = (n == 0) ? 1 : (1LL << n);
    bool print_table = (n <= 15);
    vector<int> bit_to_var(n);
    for (int i = 0; i < n; ++i) {
        bit_to_var[i] = var_indices.at(vars[i]);
    }

    ostringstream buf;

    if (print_table) {
        for (auto& v : vars)
            buf << v << " | ";
        buf << formula_text << "\n";
    } else {
        cout << "Слишком много переменных (" << n
             << ") — таблица не выводится, только проверка.\n";
    }

    bool any_true = false;
    vector<bool> interp(n);  // <-- вектор вместо map

    for (long long mask = 0; mask < rows; ++mask) {
        for (int i = 0; i < n; ++i) {
            bool val = (mask >> (n - 1 - i)) & 1;
            interp[bit_to_var[i]] = val;
        }

        bool result = root->eval(interp);

        if (print_table) {
            for (int i = 0; i < n; ++i)
                buf << (interp[bit_to_var[i]] ? '1' : '0') << " | ";
            buf << (result ? '1' : '0') << '\n';
        }

        if (result) {
            any_true = true;
            if (print_table) buf << "...\n";
            break;
        }
    }

    if (print_table) cout << buf.str();
    return !any_true;
}
int main() {
#ifdef _WIN32
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
#endif
    while (true) {
        cout << "Формула: ";
        string formula;
        if (!getline(cin, formula)) break;
        if (formula.empty()) continue;
        if (formula == "exit") break;

        Parser parser;
        shared_ptr<Node> root;
        try {
            root = parser.parse(formula);
        }
        catch (const invalid_argument& ex) {
            cout << "Ошибка синтаксиса: " << ex.what() << "\n\n";
            continue;
        }

        bool unsat = false;
        try {
            unsat = build_truth_table(root, parser.variables, parser.var_indices, formula);
        }
        catch (const exception& ex) {
            cout << "Ошибка вычисления: " << ex.what() << "\n\n";
            continue;
        }

        cout << "\nФормула является ";
        if (unsat)
            cout << "НЕВЫПОЛНИМОЙ.\n";
        else
            cout << "ВЫПОЛНИМОЙ.\n";
        cout << "\n";
    }
    return 0;
}