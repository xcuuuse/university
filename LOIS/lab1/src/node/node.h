//
// Created by Алексей on 04.04.2026.
//

#ifndef LAB1_NODE_H
#define LAB1_NODE_H
#include <string>
#include <memory>
#include <map>
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
    bool eval(const std::map<std::string, bool>& interp) const;

};
#endif //LAB1_NODE_H
