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


char Parser::peek(){
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
                + (peek() ? std::string(1, peek()) : "конец строки")
                + "' на позиции " + std::to_string(pos + 1));
    }
    consume();
}



