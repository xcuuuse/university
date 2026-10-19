/*
 * Лабораторная работа №3 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентами группы 421702 БГУИР Говор Георгий Геннадьевич, Евик Алексей Николаевич, Лойко Станислав Павлович
 */
/*
 * Объявляет структуры базы знаний (нечёткое множество, факт, правило) и функции программы:
 * чтение базы знаний, операции варианта 2 (t-норма произведения, импликация Гогена)
 * и прямой нечёткий логический вывод.
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с.
 * Рыжов А. П. Элементы теории нечётких множеств и её приложений. — М., 2003.
 */
#ifndef FUZZY_H
#define FUZZY_H

#include <cstddef>
#include <functional>
#include <ostream>
#include <string>
#include <utility>
#include <vector>

// Нечёткое множество: пары <элемент, степень принадлежности> в порядке записи в файле.
using FuzzySet = std::vector<std::pair<std::string, double>>;

// Факт — нечёткий предикат вида A(x) = {<a,0.8>,<b,0.4>}.
struct Fact {
    std::string name;
    std::string var;
    FuzzySet set;
    std::string origin;  // для выведенного факта — из какой посылки и по какому правилу он получен
};

// Правило — нечёткая импликация A(x) ~> B(y); хранит номера фактов A и B в базе знаний.
struct Rule {
    std::size_t premise;
    std::size_t conclusion;
};

// База знаний: факты и правила.
struct KnowledgeBase {
    std::vector<Fact> facts;
    std::vector<Rule> rules;
};

// Команда пользователя между итерациями: следующая итерация, до конца без вопросов, прервать.
enum class Command {
    Next, All, Stop
};

// Итог вывода: выведенные факты, число итераций и причина остановки.
struct Result {
    std::vector<Fact> derived;
    int iterations = 0;
    bool stabilized = true;  // false — вывод прерван пользователем
};

// Читает базу знаний по грамматике из задания; при ошибке бросает std::runtime_error с номером строки.
KnowledgeBase parseKnowledgeBase(std::istream& in);

// t-норма — алгебраическое произведение: T(a, b) = a * b.
double tnorm(double a, double b);

// Импликация Гогена: I(a, b) = 1 при a <= b, иначе b / a.
double goguen(double a, double b);

// Возвращает степень принадлежности элемента (0, если элемента нет в множестве).
double degreeOf(const FuzzySet& set, const std::string& element);

// Записывает множество как {<a,0.8>,<b,0.4>}.
std::string toString(const FuzzySet& set);

// Записывает факт как A(x) = {<a,0.8>,<b,0.4>}.
std::string toString(const Fact& fact);

// Записывает правило как A(x) ~> B(y).
std::string toString(const KnowledgeBase& kb, const Rule& rule);

// Вычисляет B'(y) = max по x { A'(x) * I(A(x), B(y)) } и печатает расчёт каждого значения в log.
FuzzySet conclude(const FuzzySet& aPrime, const FuzzySet& a, const FuzzySet& b, const std::string& name,
                  std::ostream& log);

// Выполняет прямой вывод до стабилизации или до команды Stop; ask вызывается между итерациями.
Result infer(KnowledgeBase kb, std::ostream& log, const std::function<Command(int)>& ask);

#endif