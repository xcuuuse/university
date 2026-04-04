//
// Created by Алексей on 04.04.2026.
//
#include "node.h"

bool Node::eval(const std::map<std::string, bool> &interp) const {
    switch (kind) {
        case NodeKind::Var:
            return interp.at(name);
        case NodeKind::Neg:
            return !left->eval(interp);
        case NodeKind::Or:
            return left->eval(interp) || right->eval(interp);
        case NodeKind::And:
            return left->eval(interp) && right->eval(interp);
        case NodeKind::Equiv:
            return left->eval(interp) == right->eval(interp);
        case NodeKind::Impl:
            return !left->eval(interp) || right->eval(interp);
    }
    return false;
}


