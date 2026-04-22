#ifdef _WIN32
#include <windows.h>
#endif

#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <memory>
#include <stdexcept>
#include <algorithm>
#include <iomanip>

enum class NodeKind {
    Var,
    Neg,
    And,
    Or,
    Impl,
    Equiv
};

struct Node {
    NodeKind kind;
    std::string name;
    std::string text;
    std::shared_ptr<Node> left;
    std::shared_ptr<Node> right;


    bool eval(const std::map<std::string, bool>& interp) const {
        switch (kind) {
            case NodeKind::Var:
                return interp.at(name);
            case NodeKind::Neg:
                return !left->eval(interp);
            case NodeKind::And:
                return left->eval(interp) && right->eval(interp);
            case NodeKind::Or:
                return left->eval(interp) || right->eval(interp);
            case NodeKind::Impl:
                return !left->eval(interp) || right->eval(interp);
            case NodeKind::Equiv:
                return left->eval(interp) == right->eval(interp);
        }
        return false;
    }
};

class Parser {
public:
    std::set<std::string> variables;

    std::shared_ptr<Node> parse(const std::string& input) {
        src = input;
        pos = 0;
        variables.clear();
        skipSpaces();
        auto root = parseFormula();
        skipSpaces();
        if (pos != (int)src.size()) {
            throw std::invalid_argument(
                "лишние символы после формулы на позиции "
                + std::to_string(pos + 1) + ": '" + src.substr(pos) + "'");
        }
        return root;
    }

private:
    std::string src;
    int pos = 0;

    void skipSpaces() {
        while (pos < (int)src.size() && src[pos] == ' ') ++pos;
    }

    char peek() {
        return (pos < (int)src.size()) ? src[pos] : '\0';
    }

    char consume() {
        if (pos >= (int)src.size())
            throw std::invalid_argument("Неожиданный конец строки");
        return src[pos++];
    }

    void expect(char c) {
        skipSpaces();
        if (peek() != c)
            throw std::invalid_argument(
                std::string("Ожидался '") + c + "', получен '"
                + (peek() ? std::string(1, peek()) : "конец строки")
                + "' на позиции " + std::to_string(pos + 1));
        consume();
    }

    std::shared_ptr<Node> parseFormula() {
        skipSpaces();
        char c = peek();

        if (c == '(') {
            int startPos = pos;
            consume(); // '('
            skipSpaces();

            std::shared_ptr<Node> node;

            if (peek() == '!') {
                consume(); // '~'
                auto child = parseFormula();
                node = std::make_shared<Node>();
                node->kind  = NodeKind::Neg;
                node->left  = child;
            } else {
                auto left = parseFormula();
                skipSpaces();

                node = std::make_shared<Node>();
                node->left = left;
                if (pos + 1 < (int)src.size() && src[pos] == '/' && src[pos + 1] == '\\') {
                    pos += 2;
                    node->kind  = NodeKind::And;
                    node->right = parseFormula();
                } else if (pos + 1 < (int)src.size() && src[pos] == '\\' && src[pos + 1] == '/') {
                    pos += 2;
                    node->kind  = NodeKind::Or;
                    node->right = parseFormula();
                } else if (peek() == '-') {
                    consume();
                    if (peek() != '>')
                        throw std::invalid_argument(
                            "Ожидался '>' после '-' на позиции "
                            + std::to_string(pos + 1));
                    consume();
                    node->kind  = NodeKind::Impl;
                    node->right = parseFormula();
                } else if (peek() == '~') {
                    consume();
                    node->kind  = NodeKind::Equiv;
                    node->right = parseFormula();
                } else {
                    throw std::invalid_argument(
                        "Ожидался оператор (/\\, \\/, ->, ~) на позиции "
                        + std::to_string(pos + 1) + ", получен '"
                        + (peek() ? std::string(1, peek()) : "конец строки") + "'");
                }
            }

            skipSpaces();
            expect(')');
            node->text = src.substr(startPos, pos - startPos);
            return node;
        } else if (std::isupper((unsigned char)c) && c != '\0') {
            // Атомарная переменная
            int startPos = pos;
            std::string name;
            name += consume();
            while (std::isdigit((unsigned char)peek()))
                name += consume();

            variables.insert(name);

            auto node   = std::make_shared<Node>();
            node->kind  = NodeKind::Var;
            node->name  = name;
            node->text  = src.substr(startPos, pos - startPos);
            return node;

        } else {
            throw std::invalid_argument(
                "Ожидалась формула (буква или '('), получен '"
                + (c ? std::string(1, c) : "конец строки")
                + "' на позиции " + std::to_string(pos + 1));
        }
    }
};
void collectSubformulas(const std::shared_ptr<Node>& node,
                        std::vector<std::shared_ptr<Node>>& result,
                        std::set<std::string>& seen) {
    if (!node) return;
    collectSubformulas(node->left,  result, seen);
    collectSubformulas(node->right, result, seen);
    if (node->kind != NodeKind::Var && seen.find(node->text) == seen.end()) {
        seen.insert(node->text);
        result.push_back(node);
    }
}

static int colWidth(const std::string& header) {
    return std::max(3, (int)header.size());
}

static void printCell(const std::string& val, int width) {
    int pad = width - (int)val.size();
    int left  = pad / 2;
    int right = pad - left;
    std::cout << std::string(left, ' ') << val << std::string(right, ' ');
}

bool buildAndPrintTable(const std::shared_ptr<Node>& root,
                        const std::set<std::string>& varSet) {
    std::vector<std::string> vars(varSet.begin(), varSet.end());
    int n = (int)vars.size();

    std::vector<std::shared_ptr<Node>> subformulas;
    std::set<std::string> seen;
    collectSubformulas(root, subformulas, seen);

    std::vector<int> varWidths;
    for (auto& v : vars)       varWidths.push_back(colWidth(v));

    std::vector<int> subWidths;
    for (auto& sf : subformulas) subWidths.push_back(colWidth(sf->text));

    const std::string sep = " | ";

    for (int i = 0; i < n; ++i) {
        printCell(vars[i], varWidths[i]);
        std::cout << sep;
    }
    for (int i = 0; i < (int)subformulas.size(); ++i) {
        printCell(subformulas[i]->text, subWidths[i]);
        if (i + 1 < (int)subformulas.size()) std::cout << sep;
    }
    std::cout << "\n";

    auto printSep = [&]() {
        for (int i = 0; i < n; ++i) {
            std::cout << std::string(varWidths[i], '-') << "-+-";
        }
        for (int i = 0; i < (int)subformulas.size(); ++i) {
            std::cout << std::string(subWidths[i], '-');
            if (i + 1 < (int)subformulas.size()) std::cout << "-+-";
        }
        std::cout << "\n";
    };
    printSep();

    long long rows = (n == 0) ? 1 : (1LL << n);
    bool anyTrue = false;

    for (long long mask = 0; mask < rows; ++mask) {
        std::map<std::string, bool> interp;
        for (int i = 0; i < n; ++i) {
            bool val = (mask >> (n - 1 - i)) & 1;
            interp[vars[i]] = val;
        }

        for (int i = 0; i < n; ++i) {
            printCell(interp[vars[i]] ? "1" : "0", varWidths[i]);
            std::cout << sep;
        }

        for (int i = 0; i < (int)subformulas.size(); ++i) {
            bool val = subformulas[i]->eval(interp);
            printCell(val ? "1" : "0", subWidths[i]);
            if (i + 1 < (int)subformulas.size()) std::cout << sep;
            if (i + 1 == (int)subformulas.size() && val)
                anyTrue = true;
        }
        std::cout << "\n";
    }

    printSep();

    if (subformulas.empty()) {
        for (long long mask = 0; mask < rows; ++mask) {
            std::map<std::string, bool> interp;
            for (int i = 0; i < n; ++i) {
                bool val = (mask >> (n - 1 - i)) & 1;
                interp[vars[i]] = val;
            }
            if (root->eval(interp)) anyTrue = true;
        }
    }

    return !anyTrue;
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
#endif

    std::cout << "=== Проверка невыполнимости формулы логики высказываний ===\n";
    while (true) {
        std::cout << "Формула: ";
        std::string line;
        if (!std::getline(std::cin, line)) break;

        // Обрезаем пробе0ы
        size_t s = line.find_first_not_of(" \t\r\n");
        size_t e = line.find_last_not_of(" \t\r\n");
        if (s == std::string::npos) { std::cout << "(пустая строка)\n\n"; continue; }
        line = line.substr(s, e - s + 1);

        if (line == "exit" || line == "quit") break;

        Parser parser;
        std::shared_ptr<Node> root;

        // Разбор
        try {
            root = parser.parse(line);
        } catch (const std::invalid_argument& ex) {
            std::cout << "Ош1бка синтаксиса: " << ex.what() << "\n\n";
            continue;
        }

        // Таб01ца
        std::cout << "\nТаблица истинности:\n";
        bool unsat = false;
        try {
            unsat = buildAndPrintTable(root, parser.variables);
        } catch (const std::exception& ex) {
            std::cout << "Ошибка вычисления: " << ex.what() << "\n\n";
            continue;
        }

        // Вывод
        std::cout << "\nФормула является ";
        if (unsat)
            std::cout << "НЕВЫПОЛНИМОЙ\n"
                         "Все интерпретации дают значен1е 0\n";
        else
            std::cout << "ВЫПОЛНИМОЙ.\n";
        std::cout << "\n";
    }
    return 0;
}