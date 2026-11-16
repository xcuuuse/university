/*
* Лабораторная работа №4 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентами группы 421702 БГУИР Говор Георгий Геннадьевич, Евик Алексей Николаевич, Лойко Станислав Павлович
 */
/*
 * Разбор входного файла по грамматике из задания: имя предиката-посылки, пустая строка и две таблицы
 * через пустую строку в любом порядке:
 *   таблица следствия - строка элементов второго домена (y) и строка степеней B(y);
 *   таблица правила - строка элементов первого домена (x) и по одной строке на каждый y (в порядке
 *                       следствия), в которой через пробел записаны R(x1,y), ..., R(xn,y).
 * Каждая строка сверяется с регулярным выражением (имена, степени 0 | 0.цифры | 1 | 1.нули), затем выполняются
 * смысловые проверки: элементы доменов не повторяются, размеры таблиц согласованы. Порядок таблиц
 * определяется перебором двух вариантов. При ошибке сообщается номер строки.
 * Версия 1.0 от 16.11.2026.
 * Использованные материалы - Практикум по логическим основам интеллектуальных систем
 *     (требования и грамматика входного файла лабораторной работы №4).
 */

#include "parser.h"
#include <cctype>
#include <fstream>
#include <regex>
#include <set>
#include <sstream>
using namespace std;

namespace {
    typedef vector<pair<int, string>> Block;

    const string NAME = "[A-Za-z][A-Za-z0-9]*", DEG = "(1(\\.0+)?|0(\\.[0-9]+)?)";
    const regex NAME_RE("^" + NAME + "$"), NAMES_RE("^" + NAME + "( +" + NAME + ")*$"),
    DEGS_RE("^" + DEG + "( +" + DEG + ")*$");

    vector<string> words(const string& s) {
        istringstream in(s);
        vector<string> w;
        for (string t; in >> t; ) w.push_back(t);
        return w;
    }

    vector<string> domain(const pair<int, string>& l) {
        vector<string> d = words(l.second);
        if (set<string>(d.begin(), d.end()).size() != d.size())
            throw ParserError{l.first, "элементы повторяются"};
        return d;
    }

    vector<double> degrees(const pair<int, string>& l, size_t cnt) {
        vector<double> v;
        for (auto& w : words(l.second)) {
            v.push_back(stod(w));
        }
        if (v.size() != cnt) {
            throw ParserError{
                l.first, "ожидалось " + to_string(cnt) + " степеней, найдено " + to_string(v.size())
            };
        }
        return v;
    }

    void fill(Task& t, const Block& cons, const Block& rule) {
        if (cons.size() != 2) throw ParserError{cons[0].first, "таблица следствия должна состоять из двух строк"};
        t.Y = domain(cons[0]);
        t.b = degrees(cons[1], t.Y.size());
        t.X = domain(rule[0]);
        if (rule.size() - 1 != t.Y.size())
            throw ParserError{rule[0].first, "в таблице правила " + to_string(rule.size() - 1) +
                                                " строк степеней, а элементов второго домена " + to_string(t.Y.size())};
        t.r.clear();
        for (size_t j = 1; j < rule.size(); j++) t.r.push_back(degrees(rule[j], t.X.size()));
    }
 } // namespace

Task parse(const string& file) {
    ifstream in(file);
    if (!in) {
        throw ParserError{0, "не удалось открыть файл \"" + file + "\""};
    }
    vector<string> lines;
    for (string s; getline(in, s); lines.push_back(s)) {
        while (!s.empty() && isspace((unsigned char)s.back())) s.pop_back();
    }
    while (!lines.empty() && lines.back().empty()) {
        lines.pop_back();
    }
    if (lines.empty()) {
        throw ParserError{1, "файл пуст"};
    }
    Task t;
    if (!regex_match(lines[0], NAME_RE)) {
        throw ParserError{1, "ожидалось имя предиката посылки"};
    }
    t.name = lines[0];
    if (lines.size() < 3 || !lines[1].empty()) {
        throw ParserError{2, "после имени предиката должна идти пустая строка и таблицы"};
    }

    vector<Block> blocks(1);
    for (size_t k = 2; k < lines.size(); k++) {
        int ln = (int)k+1;
        if (lines[k].empty()) {
            if (blocks.back().empty()) {
                throw ParserError{ln, "лишняя пустая строка"};
                blocks.emplace_back();
            }
            else if (blocks.back().empty() && !regex_match(lines[k], NAMES_RE)) {
                throw ParserError{ln, "ожидались элементы домена (имена через пробел)"};
            } else if (!blocks.back().empty() && !regex_match(lines[k], DEGS_RE)) {
                throw ParserError{ln, "ожидались степени принадлежности (0, 0.цифры, 1, 1.0...) через пробел"};
            } else {
                blocks.back().push_back({ln, lines[k]});
            }
        }
        if (blocks.size() == 1) throw ParserError{(int)lines.size(), "отсутствует вторая таблица"};
        if (blocks.size() > 2)
            throw ParserError{blocks[2][0].first, "лишняя таблица: должны быть только таблицы следствия и правила"};

        // Пробуем оба порядка: "следствие, правило" и "правило, следствие"
        vector<ParserError> errs;
        for (int k = 0; k < 2; k++) {
            try {
                fill(t, blocks[k], blocks[1 - k]);
                return t;
            } catch (ParserError& e) {
                errs.push_back(e);
            }
        }
        throw (blocks[0].size() == 2 || blocks[1].size() != 2) ? errs[0] : errs[1];
    }
}