//
// Created by Алексей on 04.04.2026.
//
#include "parser.h"
#include <memory>

std::shared_ptr<Node> Parser::parse(const std::string &input) {
    src = input;
    pos = 0;
    variables.clear();
    skip_spaces();
    auto root = parse_formula();
    skip_spaces();
    if (pos != (int)src.size()) {
        throw std::invalid_argument(
            "Лишние символы после формулы на позиции "
            + std::to_string(pos + 1)
            + ": '" + src.substr(pos) + "'");
    }
    return root;
}

void Parser::skip_spaces() {
    while (pos < (int)src.size() && src[pos] == ' ') {++pos;}
}


char Parser::peek() {
    return (pos < (int)src.size()) ? src[pos] : '\0';
}

char Parser::consume() {
    if (pos >= (int)src.size()) {
        throw std::invalid_argument("Неожиданный конец строки");
    }
    return src[pos++];
}

void Parser::expect(char c) {
    skip_spaces();
    if (peek() != c) {
        throw std::invalid_argument(
                std::string("Ожидался '") + c + "', получен '"
                + (peek() ? std::string(1, peek()) : "конец строки"));
    }
    consume();
}

std::shared_ptr<Node> Parser::parse_formula() {
    skip_spaces();
    char c = peek();
    if (c == '(') {
        int start_pos = pos;
        consume();
        skip_spaces();
        std::shared_ptr<Node> node;
        if (peek() == '!') {
            consume();
            auto child = parse_formula();
            node = std::make_shared<Node>();
            node->kind = NodeKind::Neg;
            node->left = child;
        }
        else {
            auto left = parse_formula();
            skip_spaces();
            node = std::make_shared<Node>();
            node->left = left;
            switch (peek()) {
                case '^':
                    consume();
                    node->kind = NodeKind::And;
                    node->right = parse_formula();
                    break;
                case 'v':
                    consume();
                    node->kind = NodeKind::Or;
                    node->right = parse_formula();
                    break;
                case '~':
                    consume();
                    node->kind = NodeKind::Equiv;
                    node->right = parse_formula();
                    break;
                case '-':
                    consume();
                    if (peek() != '>') {
                        throw std::invalid_argument("Ожидался '>' после '-' на позиции "
                            +std::to_string(pos + 1));
                    }
                    consume();
                    node->kind = NodeKind::Impl;
                    node->right = parse_formula();
                    break;
                default:
                    throw std::invalid_argument(
                "Ожидался оператор (^, v, ->, ~) на позиции "
                + std::to_string(pos + 1) + ", получен '"
                + (peek() ? std::string(1, peek()) : "конец строки") + "'");
            }
        }
        skip_spaces();
        expect(')');
        node->text = src.substr(start_pos, pos - start_pos);
        return node;
    } else if (std::isupper((unsigned char)c) && c != '\0') {
        int start_pos = pos;
        std::string name;
        name += consume();
        while (std::isdigit((unsigned char)peek())) {
            name += consume();
        }
        variables.insert(name);
        auto node = std::make_shared<Node>();
        node->kind = NodeKind::Var;
        node->name = name;
        node->text = src.substr(start_pos, pos - start_pos);
        return node;
    }
    else {
        throw std::invalid_argument(
                "Ожидалась формула (буква или '('), получен '"
                + (c ? std::string(1, c) : "конец строки")
                + "' на позиции " + std::to_string(pos + 1));
    }
}





