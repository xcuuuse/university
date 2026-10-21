/*
 * Лабораторная работа №3 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентами группы 421702 БГУИР Говор Георгий Геннадьевич, Евик Алексей Николаевич, Лойко Станислав Павлович
 */
/*
 * Реализует операции (t-норма произведения, импликация Гогена) и прямой нечёткий
 * вывод {A'(x), A(x) ~> B(y)} |~ {B'(y)}, B'(y) = max по x { A'(x) * I(A(x), B(y)) }.
 * Вывод идёт итерациями: каждое правило применяется к каждому исходному и выведенному факту,
 * пока появляются новые факты или пока пользователь не прервёт вывод. Против зацикливания:
 * каждая пара "правило — факт" обрабатывается один раз, совпадающий факт не добавляется,
 * вычисленные степени округляются до 4 знаков (возможных фактов конечное число).
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с.
 * Рыжов А. П. Элементы теории нечётких множеств и её приложений. — М., 2003.
 */
#include "logic.h"

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <map>
#include <sstream>

namespace {

// Округляет вычисленную степень до 4 знаков после запятой.
double roundDegree(double value) {
    return std::round(value * 10000.0) / 10000.0;
}

// Записывает степень без лишних нулей: 0.6, 0.08, 0.6667, 1.0.
std::string fmt(double value) {
    std::ostringstream out;
    out << std::fixed << std::setprecision(4) << value;
    std::string text = out.str();
    while (text.back() == '0' && text[text.size() - 2] != '.') {
        text.pop_back();
    }
    return text;
}

// Сравнивает множества поэлементно (элемент без пары имеет степень 0).
bool sameSet(const FuzzySet& first, const FuzzySet& second) {
    for (const auto& [element, degree] : first) {
        if (std::fabs(degree - degreeOf(second, element)) > 1e-9) return false;
    }
    for (const auto& [element, degree] : second) {
        if (std::fabs(degree - degreeOf(first, element)) > 1e-9) return false;
    }
    return true;
}

// Проверяет, может ли факт быть посылкой A' для правила с посылкой A: все элементы факта есть
// в области определения A. Имя переменной не сравнивается — переменные унифицируются
// (факт C(y) с элементами из области A подставляется в правило как C(x)).
bool fits(const Fact& fact, const Fact& premise) {
    return std::all_of(fact.set.begin(), fact.set.end(), [&](const auto& p) {
        return std::any_of(premise.set.begin(), premise.set.end(),
                           [&](const auto& q) { return q.first == p.first; });
    });
}

// Проверяет, остались ли пары "правило — факт", к которым правило ещё не применялось
// (done[r] — сколько первых фактов правило r уже обработало).
bool hasWork(const KnowledgeBase& kb, const std::vector<std::size_t>& done) {
    for (std::size_t r = 0; r < kb.rules.size(); ++r) {
        for (std::size_t f = done[r]; f < kb.facts.size(); ++f) {
            if (fits(kb.facts[f], kb.facts[kb.rules[r].premise])) return true;
        }
    }
    return false;
}

// Подбирает свободное имя для нового факта: имя заключения и номер (B1, B2, ...).
std::string newName(const std::vector<Fact>& facts, const std::string& base, std::map<std::string, int>& counter) {
    std::string name;
    do {
        name = base + std::to_string(++counter[base]);
    } while (std::any_of(facts.begin(), facts.end(), [&](const Fact& fact) { return fact.name == name; }));
    return name;
}

// Записывает нечёткое отношение A(x) ~> B(y) как {<<x,y>,I(A(x),B(y))>,...}.
std::string implicationText(const FuzzySet& a, const FuzzySet& b) {
    std::string text = "{";
    for (const auto& [x, ax] : a) {
        for (const auto& [y, by] : b) {
            text += (text.size() > 1 ? "," : "") + std::string("<<") + x + "," + y + ">," + fmt(goguen(ax, by)) + ">";
        }
    }
    return text + "}";
}

}  // namespace

// Вычисляет алгебраическое произведение.
double tnorm(double a, double b) {
    return a * b;
}

// Импликация Гогена — остаточная операция для произведения:
// I(a, b) = sup{d из [0, 1] | a * d <= b}; при a <= b это 1, иначе b / a.
double goguen(double a, double b) {
    return a <= b ? 1.0 : b / a;
}

// Ищет элемент в множестве и возвращает его степень (0, если элемента нет).
double degreeOf(const FuzzySet& set, const std::string& element) {
    for (const auto& [name, degree] : set) {
        if (name == element) return degree;
    }
    return 0.0;
}

// Собирает запись множества {<a,0.8>,<b,0.4>}.
std::string toString(const FuzzySet& set) {
    std::string text = "{";
    for (const auto& [element, degree] : set) {
        text += (text.size() > 1 ? "," : "") + std::string("<") + element + "," + fmt(degree) + ">";
    }
    return text + "}";
}

// Собирает запись факта A(x) = {...}.
std::string toString(const Fact& fact) {
    return fact.name + "(" + fact.var + ")=" + toString(fact.set);
}

// Собирает запись правила A(x) ~> B(y) с переменными, как они записаны в правиле.
std::string toString(const KnowledgeBase& kb, const Rule& rule) {
    return kb.facts[rule.premise].name + "(" + rule.premiseVar + ")~>" + kb.facts[rule.conclusion].name + "(" +
           rule.conclusionVar + ")";
}

// Для каждого y перебирает все x посылки: A'(x), I(A(x), B(y)), их произведение и максимум.
FuzzySet conclude(const FuzzySet& aPrime, const FuzzySet& a, const FuzzySet& b, const std::string& name,
                  std::ostream& log) {
    FuzzySet result;
    for (const auto& [y, by] : b) {
        double best = 0.0;
        std::string terms;
        for (const auto& [x, ax] : a) {
            const double given = degreeOf(aPrime, x);
            const double implication = goguen(ax, by);
            best = std::max(best, tnorm(given, implication));
            terms += (terms.empty() ? "" : ",") + fmt(given) + "*" + fmt(implication);
        }
        result.emplace_back(y, roundDegree(best));
        log << "      " << name << "'(" << y << ")=max{" << terms << "}=" << fmt(best) << "\n";
    }
    return result;
}

// Печатает импликации правил, затем итерациями применяет каждое правило к каждому подходящему
// факту, к которому оно ещё не применялось; между итерациями спрашивает пользователя.
Result infer(KnowledgeBase kb, std::ostream& log, const std::function<Command(int)>& ask) {
    log << "\nНечёткие импликации (Гоген):\n";
    for (const Rule& rule : kb.rules) {
        log << "  " << toString(kb, rule) << "="
            << implicationText(kb.facts[rule.premise].set, kb.facts[rule.conclusion].set) << "\n";
    }
    const std::size_t initialCount = kb.facts.size();
    std::vector<std::size_t> done(kb.rules.size(), 0);
    std::map<std::string, int> counter;
    Result result;
    bool askUser = true;
    while (hasWork(kb, done)) {
        if (result.iterations > 0 && askUser) {
            const Command command = ask(result.iterations);
            if (command == Command::Stop) {
                result.stabilized = false;
                break;
            }
            askUser = (command == Command::Next);
        }
        ++result.iterations;
        log << "\n--- Итерация " << result.iterations << " ---\n";
        const std::size_t known = kb.facts.size();
        for (std::size_t r = 0; r < kb.rules.size(); ++r) {
            const Rule& rule = kb.rules[r];
            for (std::size_t f = done[r]; f < known; ++f) {
                const Fact& given = kb.facts[f];
                const Fact& a = kb.facts[rule.premise];
                const Fact& b = kb.facts[rule.conclusion];
                if (!fits(given, a)) continue;
                // Унификация: факт подставляется в правило с переменной посылки, например C(y) как C(x).
                const std::string premise = given.name + "(" + rule.premiseVar + ")";
                const std::string origin = "{" + premise + "," + toString(kb, rule) + "}";
                log << "  " << origin << "|~" << b.name << "'(" << rule.conclusionVar << ")";
                if (given.var != rule.premiseVar) {
                    log << "   (" << given.name << "(" << given.var << ") унифицирован как " << premise << ")";
                }
                log << "\n";
                Fact derived{"", rule.conclusionVar, conclude(given.set, a.set, b.set, b.name, log), origin};
                log << "      " << b.name << "'(" << rule.conclusionVar << ")=" << toString(derived.set);
                const auto same = std::find_if(kb.facts.begin(), kb.facts.end(),
                                               [&](const Fact& fact) { return sameSet(fact.set, derived.set); });
                if (same != kb.facts.end()) {
                    log << "  -> совпадает с " << same->name << "(" << same->var << "), не добавлен\n";
                    continue;
                }
                derived.name = newName(kb.facts, b.name, counter);
                log << "  -> новый факт " << derived.name << "(" << derived.var << ")\n";
                kb.facts.push_back(derived);  // ссылки given, a, b дальше не используются
            }
            done[r] = known;
        }
    }
    log << (result.stabilized ? "\nНовых фактов больше нет: вывод стабилизировался.\n"
                              : "\nВывод прерван пользователем.\n");
    result.derived.assign(kb.facts.begin() + static_cast<std::ptrdiff_t>(initialCount), kb.facts.end());
    return result;
}