//
// Created by Алексей on 04.04.2026.
//

#ifndef LAB1_PARSER_H
#define LAB1_PARSER_H
#include <set>
#include <string>
#include <memory>
#include <node/node.h>
class Parser {
public:
    std::set<std::string> variables;
    std::shared_ptr<Node> parse(const std::string& input);
private:
    std::string src;
    int pos = 0;
    void skip_spaces();
    char peek();
    char consume();
    void expect(char c);
    std::shared_ptr<Node> parse_formula();

};
#endif //LAB1_PARSER_H
