#include <node/node.h>
#include <parser/parser.h>
#include <vector>
#include <iostream>
#include <stdexcept>
#include <algorithm>
#include <iomanip>
#include <memory>
#include <windows.h>
using namespace std;
void collect_subformulas(const std::shared_ptr<Node>& node,
    std::vector<std::shared_ptr<Node>>& result, std::set<std::string>& seen) {
    if (!node)
        return;
    collect_subformulas(node->left, result, seen);
    collect_subformulas(node->right, result, seen);
    if (node->kind != NodeKind::Var && seen.find(node->text) == seen.end()) {
        seen.insert(node->text);
        result.push_back(node);
    }
}

static int col_width(const std::string& header) {
    return std::max(3, (int)header.size());
}

static void print_cell(const std::string& val, int width) {
    int pad = width - (int)val.size();
    int left = pad / 2;
    int right = pad - left;
    std::cout << std::string(left, ' ') << val << std::string(right, ' ');
}

bool build_truth_table(const std::shared_ptr<Node>& root,
    const std::set<std::string>& var_set) {

    std::vector<std::string> vars(var_set.begin(), var_set.end());
    int n = (int)vars.size();
    long long rows = (n == 0) ? 1 : (1LL << n);

    // Заголовок — только переменные и результат
    for (auto& v : vars)
        std::cout << v << " | ";
    std::cout << "Результат\n";

    std::string sep(vars.size() * 4 + 10, '-');
    std::cout << sep << "\n";

    bool any_true = false;

    for (long long mask = 0; mask < rows; ++mask) {
        std::map<std::string, bool> interp;
        for (int i = 0; i < n; ++i) {
            bool val = (mask >> (n - 1 - i)) & 1;
            interp[vars[i]] = val;
        }

        bool result = root->eval(interp);
        if (result) any_true = true;

        for (int i = 0; i < n; ++i)
            std::cout << (interp[vars[i]] ? "1" : "0") << " | ";
        std::cout << (result ? "1" : "0") << "\n";
    }

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
        if (!getline(cin, formula)) {
            break;
        }
        size_t s = formula.find_first_not_of(" \t\r\n");
        size_t e = formula.find_last_not_of(" \t\r\n");
        if (s == std::string::npos) { std::cout << "(пустая строка)\n\n"; continue; }
        formula = formula.substr(s, e - s + 1);
        if (formula == "exit" || formula == "quit") break;
        Parser parser;
        std::shared_ptr<Node> root;
        try {
            root = parser.parse(formula);
        }
        catch (const invalid_argument& ex) {
            cout << "Ошибка синтаксиса: " << ex.what() << "\n\n";
            continue;
        }
        bool unsat = false;
        try {
            unsat = build_truth_table(root, parser.variables);
        }
        catch (const exception& ex) {
            cout << "Ошибка вычисления: " << ex.what() << "\n\n";
            continue;
        }
        cout << "\nФормула является ";
        if (unsat)
            std::cout << "НЕВЫПОЛНИМОЙ.\n"
                         "Все интерпретации дают значение ЛОЖЬ.\n";
        else
            std::cout << "ВЫПОЛНИМОЙ.\n"
                         "Существует интерпретация, при которой формула ИСТИННА.\n";
        std::cout << "\n";
    }
    return 0;
}

/*bool build_truth_table(const std::shared_ptr<Node>& root,
    const std::set<std::string>& var_set) {
    std::vector<std::string> vars(var_set.begin(), var_set.end());
    int n = (int)vars.size();
    std::vector<std::shared_ptr<Node>> subformulas;
    std::set<std::string> seen;
    collect_subformulas(root, subformulas, seen);
    std::vector<int> widths;
    for (auto& v : vars) {
        widths.push_back(col_width(v));
    }
    std::vector<int> subwidths;
    for (auto& s: subformulas) {
        subwidths.push_back(col_width(s->text));
    }
    const std::string separator = " | ";
    for (int i = 0; i < n; i++) {
        print_cell(vars[i], widths[i]);
        std::cout << separator;
    }
    for (int i = 0; i < (int)subformulas.size(); ++i) {
        print_cell(subformulas[i]->text, subwidths[i]);
        if (i + 1 < (int)subformulas.size()) std::cout << separator;
    }
    auto print_separator = [&]() {
        for (int i = 0; i < n; i++) {
            std::cout << std::string(widths[i], '-');
        }
        for (int i = 0; i < (int)subformulas.size(); i++) {
            std::cout << std::string(subwidths[i], '-');
            if (i + 1 < (int)subformulas.size()) {
                //std::cout << "---";
            }
        }
        std::cout << "\n";
    };
    print_separator();
    std::cout << "\n";
    long long rows = (n == 0) ? 1 : (1LL << n);
    bool any_true = false;

    for (long long mask = 0; mask < rows; ++mask) {
        std::map<std::string, bool> interp;
        for (int i = 0; i < n; ++i) {
            bool val = (mask >> (n - 1 - i)) & 1;
            interp[vars[i]] = val;
        }
        for (int i = 0; i < n; ++i) {
            print_cell(interp[vars[i]] ? "1" : "0", widths[i]);
            std::cout << separator;
        }
        for (int i = 0; i < (int)subformulas.size(); ++i) {
            bool val = subformulas[i]->eval(interp);
            print_cell(val ? "1" : "0", subwidths[i]);
            if (i + 1 < (int)subformulas.size()) std::cout << separator;
            // Последняя подформула — это корень (вся формула)
            if (i + 1 == (int)subformulas.size() && val)
                any_true = true;
        }
        std::cout << "\n";
    }
    print_separator();
    if (subformulas.empty()) {
        for (long long mask = 0; mask < rows; mask++) {
            std::map<std::string, bool> interp;
            for (int i = 0; i < n; i++) {
                bool val = (mask >> (n - 1 - i)) & 1;
                interp[vars[i]] = val;
            }
            if (root->eval(interp)) any_true = true;
        }
    }
    return !any_true;
} если хочу полную таблицу*/