#include <iostream>
#include <string>
#include <stdexcept>

using namespace std;

// Узел связанного списка
struct Node {
    double data; // Данные узла
    Node* next;  // Указатель на следующий узел

    Node(double value) : data(value), next(nullptr) {}
};

// Класс стека, реализованный через связанный список
class Stack {
private:
    Node* topNode; // Указатель на верхний элемент стека

public:
    Stack() : topNode(nullptr) {}

    ~Stack() {
        while (!isEmpty()) {
            pop();
        }
    }

    bool isEmpty() const {
        return topNode == nullptr;
    }

    void push(double value) {
        Node* newNode = new Node(value);
        newNode->next = topNode;
        topNode = newNode;
    }

    void pop() {
        if (isEmpty()) {
            throw runtime_error("empty stack");
        }
        Node* temp = topNode;
        topNode = topNode->next;
        delete temp;
    }

    double top() const {
        if (isEmpty()) {
            throw runtime_error("empty stack");
        }
        return topNode->data;
    }
};

// Функция для определения приоритета операторов
int prioritet(char op) {
    if (op == '+' || op == '-')
        return 1;
    if (op == '*' || op == '/')
        return 2;
    return 0;
}

// Проверяет, является ли символ оператором
bool isOperator(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/';
}

// Проверяет, является ли символ операндом (буквой от 'a' до 'z')
bool isOperand(char c) {
    return (c >= 'a' && c <= 'z');
}

// Применяет операцию к двум операндам
double applyOp(double a, double b, char op) {
    switch (op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/':
            if (b == 0) throw runtime_error("division by zero");
            return a / b;
        default: return 0;
    }
}

bool checkParentheses(const string& expression) {
    int balance = 0;
    for (char c : expression) {
        if (c == '(') balance++;
        else if (c == ')') balance--;

        if (balance < 0) return false;
    }
    return balance == 0;
}

// Вычисляет значение выражения в постфиксной нотации
double evaluatePostfix(const string& expression, const double variables[]) {
    Stack operands;

    for (char c : expression) {
        if (isOperand(c)) {
            operands.push(variables[c - 'a']);
        } else if (isOperator(c)) {
            double operand2 = operands.top();
            operands.pop();
            double operand1 = operands.top();
            operands.pop();
            operands.push(applyOp(operand1, operand2, c));
        }
    }
    return operands.top();
}

string infixToPostfix(const string& expression) {
    if (!checkParentheses(expression)) {
        throw runtime_error("unbalanced parentheses");
    }

    string postfix = "";
    Stack operators;

    for (char c : expression) {
        if (c == ' ')
            continue;
        if (isOperand(c)) {
            postfix += c;
        } else if (c == '(') {
            operators.push(c);
        } else if (c == ')') {
            while (!operators.isEmpty() && operators.top() != '(') {
                postfix += operators.top();
                operators.pop();
            }
            if (operators.isEmpty()) {
                throw runtime_error("mismatched parentheses");
            }
            operators.pop(); // Удаляем '(' из стека
        } else if (isOperator(c)) {
            while (!operators.isEmpty() && operators.top() != '(' &&
                   prioritet(operators.top()) >= prioritet(c)) {
                postfix += operators.top();
                operators.pop();
            }
            operators.push(c);
        } else {
            throw runtime_error("invalid character in expression");
        }
    }

    while (!operators.isEmpty()) {
        if (operators.top() == '(') {
            throw runtime_error("mismatched parentheses");
        }
        postfix += operators.top();
        operators.pop();
    }
    return postfix;
}

int main() {
        string infix_expression = "a+b*c/(d+e)/f+(g+h-i)+(j/k)-l/m+(n*o+p)-q/r-s";
        double variables[5] = {8.6, 2.4, 5.1, 0.3, 7.9};

        cout << "Infix expression: " << infix_expression << endl;

        string postfix_expression = infixToPostfix(infix_expression);
        cout << "Postfix expression: " << postfix_expression << endl;


    return 0;
}
