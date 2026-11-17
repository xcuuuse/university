/*
* Лабораторная работа №4 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентами группы 421702 БГУИР Говор Георгий Геннадьевич, Евик Алексей Николаевич, Лойко Станислав Павлович
 */
/*
 * Обратный нечёткий логический вывод на основе операции нечёткой композиции max(xi·yi) (вариант 2).
 * Решается система B(y) = max по x (A(x)·R(x,y)). Наибольшее решение: Â(x) = min по y I_G(R(x,y), B(y)),
 * где I_G - импликация Гогена; если Â не удовлетворяет системе, решений нет. Иначе для каждого y с B(y) > 0
 * выбирается x, на котором достигается B(y) (там A(x) = Â(x)); каждый выбор даёт брус решений
 * [нижняя граница, Â]. Поглощённые брусы исключаются, ответ - объединение оставшихся.
 * Все шаги записываются в протокол, значения выводятся с 4 знаками после запятой.
 * Версия 1.0 от 16.11.2026.
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с (разделы "Обратный нечёткий логический вывод",
 *     "Лабораторная работа №3. Метод решения систем уравнений нечётких множеств")
 */

#include "inference.h"
#include <algorithm>
#include <cmath>
#include <functional>
#include <iomanip>
#include <set>
#include <sstream>

using namespace std;

namespace {
    const double EPS = 1e-9;

    string f4(double v) {
        ostringstream s;
        s << fixed << setprecision(4) << v;
        return s.str();
    }

    double goguen(double a, double b) {
        return a <= b + EPS ? 1.0 : b / a;
    }

    void print_input(const Task& t, ostream& out) {
        size_t n = t.X.size(), m = t.Y.size();
        out << "Исходные данные\nСледствие B(y) = {";
        for (size_t j = 0; j < m; j++) {
            out << (j ? ", ": "") << "<" << t.Y[j] << ", " << f4(t.b[j]) << ">";
        }
        out << "}\nПравило R(x, y) (строки - y, столбцы - x):\n" << setw(10) << "";
        for (auto& x : t.X) {
            out << setw(10) << x;
        }
        for (size_t j = 0; j < m; j++) {
            out << "\n" << setw(10) << t.Y[j];
            for (size_t i = 0; i < n; i++) {
                out << setw(10) << f4(t.r[j][i]);
            }
        }
        out << "\n\nСистема уравнений (max-product композиция):\n";
        for (size_t j = 0; j < m; j++) {
            out << "  max(";
            for (size_t i = 0; i < n; i++) {
                out << (i ? ", " : "") << f4(t.r[j][i]) << "·" << t.name << "(" << t.X[i] << ")";
            }
            out << ") = " << f4(t.b[j]) << "\n";
        }
    }

    vector <double> greatest(const Task& t, ostream& out) {
        out << "\nШаг 1. Наибольшее решение Â(x) = min по y I_G(R(x,y), B(y)), I_G(a,b) = 1 при a <= b, иначе b/a\n";
        vector <double> up (t.X.size(), 1.0);
        for (size_t i = 0; i < t.X.size(); i++) {
            out << "  Â(" << t.X[i] << ") = min(";
            for (size_t j = 0; j < t.Y.size(); j++) {
                double g = goguen(t.r[j][i], t.b[j]);
                up[i] = min(up[i], g);
                out << (j ? ", " : "") << "I_G(" << f4(t.r[j][i]) << ", " << f4(t.b[j]) << ")=" << f4(g);
            }
            out << ") = " << f4(up[i]) << "\n";
        }
        return up;
    }

    bool check(const Task& t, const vector<double>& up, ostream& out) {
        out << "\nШаг 2. Подстановка Â в систему\n";
        bool ok = true;
        for (size_t j = 0; j < t.Y.size(); j++) {
            double mx = 0;
            out << "  " << t.Y[j] << ": max(";
            for (size_t i = 0; i < t.X.size(); i++) {
                mx = max(mx, t.r[j][i] * up[i]);
                out << (i ? ", " : "") << f4(t.r[j][i]) << "·" << f4(up[i]) << "=" << f4(t.r[j][i] * up[i]);
            }
            bool eq = fabs(mx - t.b[j]) < EPS;
            ok = ok && eq;
            out << ") = " << f4(mx) << (eq ? " = " : " != ") << "B(" << t.Y[j] << ") = " << f4(t.b[j]) << "\n";
        }
        return ok;
    }

    // Шаг 3. Для каждого y с B(y) > 0 - индексы x, на которых достигается B(y)
    vector<vector<size_t>> attainers(const Task& t, const vector<double>& up, ostream& out) {
        out << "\nШаг 3. Элементы x, на которых достигается B(y) (R(x,y)·Â(x) = B(y)):\n";
        vector<vector<size_t>> S;
        for (size_t j = 0; j < t.Y.size(); j++) {
            out << "  " << t.Y[j] << ": ";
            if (t.b[j] < EPS) {
                out << "B = 0, выполняется при любых A <= Â\n";
                continue;
            }
            S.emplace_back();
            for (size_t i = 0; i < t.X.size(); i++) {
                if (fabs(t.r[j][i] * up[i] - t.b[j]) < EPS) S.back().push_back(i);
            }
            for (size_t k = 0; k < S.back().size(); k++) {
                out << (k ? ", " : "{") << t.X[S.back()[k]];
            }
            out << "}\n";
        }
        return S;
    }

    // Шаг 4. Перебор выборов (по одному x на каждый y) и исключение поглощённых наборов.
    // Набор - отметки тех x, у которых нижняя граница равна Â(x) (у остальных она 0)
    vector<vector<bool>> minimal_sets(const vector<vector<size_t>>& S, size_t n, ostream& out) {
        set<vector<bool>> covers;
        vector<bool> cur(n, false);
        function<void(size_t)> dfs = [&](size_t k) {
            if (k == S.size()) {
                covers.insert(cur);
                return ;
            }
            for (size_t i: S[k]) {
                if (cur[i]) {
                    dfs(k + 1);
                    return ;
                }
            }
            for (size_t i : S[k]) {
                cur[i] = true;
                dfs(k + 1);
                cur[i] = false;
            }
        };
        dfs(0);
        vector<vector<bool>> res;
        for (auto& a: covers) {
            bool absorbed = false;
            for (auto& c: covers) {
                bool sub = c != a;
                for (size_t i = 0; i < n && sub; i++) {
                    sub = !c[i] || a[i];
                }
                absorbed = absorbed || sub;
            }
            if (!absorbed){res.push_back(a);}
        }
        out << "\nШаг 4. Найдено наборов нижних границ: " << covers.size()
        << ", после исключения поглощённых: " << res.size() << "\n";
        return res;
    }
} // namespace

std::string solve(const Task &t) {
    ostringstream out;
    print_input(t, out);
    vector<double> up = greatest(t, out);
    if (!check(t, up, out)) {
        out << "\nСистема не имеет решения: множество посылок " << t.name << " пусто (∅).\n";
        return out.str();
    }
    vector<vector<bool>> res = minimal_sets(attainers(t, up, out), t.X.size(), out);
    out << "\nОтвет: множество всех решений " << t.name << "(x) =\n";
    for (size_t k = 0; k < res.size(); k++) {
        out << (k ? "  ∪ {" : "    {");
        for (size_t i = 0; i < t.X.size(); i++) {
            out << (i ? ", " : "") << "<" << t.X[i] << ", [" << f4(res[k][i] ? up[i] : 0.0) << ", " << f4(up[i]) << "]>";
        }
        out << "}\n";
    }
    return out.str();
}