/*
 * Лабораторная работа №3 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентами группы 421702 БГУИР Говор Георгий Геннадьевич, Евик Алексей Николаевич, Лойко Станислав Павлович
 */
/*
 * Читает базу знаний. Каждая непустая строка сверяется с регулярным выражением, построенным
 * по грамматике из задания (факт: A(x) = {<a,0.5>,...}, правило: A(x) ~> B(y)), затем
 * выполняются смысловые проверки: факты идут раньше правил, имена предикатов не повторяются,
 * элементы в множестве не повторяются, правило ссылается на заданные факты с той же переменной.
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с. (с. 65–66: формат базы знаний)
 * Грамматика базы знаний - Третья лабораторная работа по логическим основам интеллектуальных систем -
 *     URL: https://scnedu.sourceforge.net/variety/_/index.html?variety=everface.json&gradient=interscreen.json
 *     (дата обращения: 01.03.2024)
 * Регулярные выражения - std::regex - URL: https://en.cppreference.com/w/cpp/regex (дата обращения: 13.10.2026)
 * Версия 2.0 (13.10.2026): упрощённая версия программы.
 */
#include "logic.h"

#include <algorithm>
#include <regex>
#include <stdexcept>

namespace {

// Бросает исключение с номером строки файла.
[[noreturn]] void fail(int line, const std::string& message) {
    throw std::runtime_error("строка " + std::to_string(line) + ": " + message);
}

// Возвращает номер факта с указанным именем или kb.facts.size(), если такого факта нет.
std::size_t findFact(const KnowledgeBase& kb, const std::string& name) {
    std::size_t i = 0;
    while (i < kb.facts.size() && kb.facts[i].name != name) {
        ++i;
    }
    return i;
}

// Находит факт, на который ссылается правило, и проверяет, что переменная совпадает с переменной факта.
std::size_t resolve(const KnowledgeBase& kb, const std::string& name, const std::string& var, int line) {
    const std::size_t i = findFact(kb, name);
    if (i == kb.facts.size()) {
        fail(line, "предикат " + name + " не задан ни одним фактом");
    }
    if (kb.facts[i].var != var) {
        fail(line, "предикат " + name + " задан с переменной " + kb.facts[i].var + ", а в правиле указана " + var);
    }
    return i;
}

}  // namespace

// Разбирает файл построчно: пустые строки пропускает, правила и факты проверяет по грамматике.
KnowledgeBase parseKnowledgeBase(std::istream& in) {
    const std::string name = "([A-Za-z][A-Za-z0-9]*)";                                  // <имя>
    const std::string head = "\\s*" + name + "\\s*\\(\\s*" + name + "\\s*\\)\\s*";      // <имя>(<имя>)
    const std::string pair = "<\\s*" + name + "\\s*,\\s*([0-9.]+)\\s*>";                // <элемент,степень>
    const std::regex blankLine("\\s*");
    const std::regex ruleLine(head + "~>" + head);
    const std::regex factLine(head + "=\\s*\\{\\s*(" + pair + "(\\s*,\\s*" + pair + ")*)\\s*\\}\\s*");
    const std::regex pairPattern(pair);
    const std::regex degreePattern("1(\\.0+)?|0(\\.[0-9]+)?");  // 1 | 1.0...0 | 0 | 0.<цифры>

    KnowledgeBase kb;
    std::string text;
    for (int line = 1; std::getline(in, text); ++line) {
        if (line == 1 && text.rfind("\xEF\xBB\xBF", 0) == 0) {
            text.erase(0, 3);  // метка UTF-8, которую добавляет Блокнот
        }
        std::smatch match;
        if (std::regex_match(text, blankLine)) {
            continue;
        }
        if (std::regex_match(text, match, ruleLine)) {
            kb.rules.push_back({resolve(kb, match[1], match[2], line), resolve(kb, match[3], match[4], line)});
        } else if (std::regex_match(text, match, factLine)) {
            if (!kb.rules.empty()) {
                fail(line, "факт после правил: сначала должны идти все факты, затем правила");
            }
            if (findFact(kb, match[1]) < kb.facts.size()) {
                fail(line, "предикат " + match[1].str() + " уже задан");
            }
            Fact fact{match[1], match[2], {}, ""};
            const std::string pairs = match[3];
            for (std::sregex_iterator it(pairs.begin(), pairs.end(), pairPattern), end; it != end; ++it) {
                const std::string element = (*it)[1];
                const std::string degree = (*it)[2];
                if (!std::regex_match(degree, degreePattern)) {
                    fail(line, "неверная степень принадлежности " + degree + " (допустимо 0, 1, 1.0 или 0.<цифры>)");
                }
                if (std::any_of(fact.set.begin(), fact.set.end(), [&](const auto& p) { return p.first == element; })) {
                    fail(line, "элемент " + element + " повторяется в множестве");
                }
                fact.set.emplace_back(element, std::stod(degree));
            }
            kb.facts.push_back(fact);
        } else {
            fail(line, "не соответствует грамматике: ожидается факт A(x) = {<a,0.5>,<b,1>} или правило A(x) ~> B(y)");
        }
    }
    if (kb.facts.empty()) {
        throw std::runtime_error("в базе знаний нет ни одного факта");
    }
    return kb;
}