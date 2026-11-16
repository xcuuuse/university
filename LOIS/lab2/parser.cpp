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
#include <stdexcept>
using namespace std;

namespace {
    typedef vector<pair<int, string>> Block;  // строки одной таблицы: <номер строки, текст>

    const string NAME = "[A-Za-z][A-Za-z0-9]*", DEG = "(1(\\.0+)?|0(\\.[0-9]+)?)";
    const regex NAME_RE("^" + NAME + "$"), NAMES_RE("^" + NAME + "( +" + NAME + ")*$"),
        DEGS_RE("^" + DEG + "( +" + DEG + ")*$");

    // Записывает ошибку и возвращает false
    bool fail(ParserError& err, int line, const string& message) {
        err = {line, message};
        return false;
    }

    vector<string> words(const string& s) {
        istringstream in(s);
        vector<string> w;
        for (string t; in >> t; ) {
            w.push_back(t);
        }
        return w;
    }

    bool domain(const pair<int, string>& l, vector<string>& d, ParserError& err) {
        d = words(l.second);
        if (set<string>(d.begin(), d.end()).size() != d.size()) {
            return fail(err, l.first, "элементы домена повторяются");
        }
        return true;
    }

    bool degrees(const pair<int, string>& l, size_t cnt, vector<double>& v, ParserError& err) {
        v.clear();
        try {
            for (auto& w : words(l.second)) {
                v.push_back(stod(w));
            }
        } catch (const invalid_argument&) {
            return fail(err, l.first, "степень принадлежности не является числом");
        } catch (const out_of_range&) {
            return fail(err, l.first, "степень принадлежности выходит за пределы типа double");
        }
        if (v.size() != cnt) {
            return fail(err, l.first, "ожидалось " + to_string(cnt) + " степеней, найдено " + to_string(v.size()));
        }
        return true;
    }

    // Заполняет задачу по паре таблиц (следствие, правило) с проверкой согласованности размеров
    bool fill(Task& t, const Block& cons, const Block& rule, ParserError& err) {
        if (cons.size() != 2) {
            return fail(err, cons[0].first, "таблица следствия должна состоять из двух строк");
        }
        if (!domain(cons[0], t.Y, err) || !degrees(cons[1], t.Y.size(), t.b, err) || !domain(rule[0], t.X, err)) {
            return false;
        }
        if (rule.size() - 1 != t.Y.size()) {
            return fail(err, rule[0].first, "в таблице правила " + to_string(rule.size() - 1) +
                                                " строк степеней, а элементов второго домена " + to_string(t.Y.size()));
        }
        t.r.assign(rule.size() - 1, {});
        for (size_t j = 1; j < rule.size(); j++) {
            if (!degrees(rule[j], t.X.size(), t.r[j - 1], err)) {
                return false;
            }
        }
        return true;
    }

    // Делит строки после заголовка на таблицы по пустым строкам, проверяя синтаксис каждой строки
    bool split_blocks(const vector<string>& lines, vector<Block>& blocks, ParserError& err) {
        blocks.assign(1, Block());
        for (size_t k = 2; k < lines.size(); k++) {
            int ln = (int)k + 1;
            if (lines[k].empty()) {
                if (blocks.back().empty()) {
                    return fail(err, ln, "лишняя пустая строка");
                }
                blocks.emplace_back();
            } else if (blocks.back().empty() && !regex_match(lines[k], NAMES_RE)) {
                return fail(err, ln, "ожидались элементы домена (имена через пробел)");
            } else if (!blocks.back().empty() && !regex_match(lines[k], DEGS_RE)) {
                return fail(err, ln, "ожидались степени принадлежности (0, 0.цифры, 1, 1.0...) через пробел");
            } else {
                blocks.back().push_back({ln, lines[k]});
            }
        }
        if (blocks.size() == 1) {
            return fail(err, (int)lines.size(), "отсутствует вторая таблица");
        }
        if (blocks.size() > 2) {
            return fail(err, blocks[2][0].first, "лишняя таблица: должны быть только таблицы следствия и правила");
        }
        return true;
    }
} // namespace

bool parse(const string& file, Task& t, ParserError& err) {
    ifstream in(file);
    if (!in) {
        return fail(err, 0, "не удалось открыть файл \"" + file + "\"");
    }
    vector<string> lines;
    for (string s; getline(in, s); lines.push_back(s)) {
        while (!s.empty() && isspace((unsigned char)s.back())) {
            s.pop_back();
        }
    }
    while (!lines.empty() && lines.back().empty()) {
        lines.pop_back();
    }
    if (lines.empty()) {
        return fail(err, 1, "файл пуст");
    }
    if (!regex_match(lines[0], NAME_RE)) {
        return fail(err, 1, "ожидалось имя предиката посылки");
    }
    t.name = lines[0];
    if (lines.size() < 3 || !lines[1].empty()) {
        return fail(err, 2, "после имени предиката должна идти пустая строка и таблицы");
    }

    vector<Block> blocks;
    if (!split_blocks(lines, blocks, err)) {
        return false;
    }

    // Пробуем оба порядка: "следствие, правило" и "правило, следствие".
    // Если не подошёл ни один, сообщаем ошибку того порядка, в котором следствие состоит из двух строк
    ParserError errs[2];
    for (int k = 0; k < 2; k++) {
        if (fill(t, blocks[k], blocks[1 - k], errs[k])) {
            return true;
        }
    }
    err = (blocks[0].size() == 2 || blocks[1].size() != 2) ? errs[0] : errs[1];
    return false;
}