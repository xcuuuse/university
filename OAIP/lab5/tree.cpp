#include <iostream>
#include <cstring>
#include <string>
using namespace std;

struct Node {
    int key;
    char value[100];
    unsigned char height;
    Node *left, *right;

    Node(int k, const char* v) : key(k), height(1), left(nullptr), right(nullptr) {
        strncpy(value, v, 99); value[99] = '\0';
    }
};

unsigned char height(Node* p) { return p ? p->height : 0; }
void fix_height(Node* p) { p->height = max(height(p->left), height(p->right)) + 1; }

Node* insert_bst(Node* root, int key, const char* value) {
    if (!root) return new Node(key, value);
    if (key < root->key)
        root->left = insert_bst(root->left, key, value);
    else if (key > root->key)
        root->right = insert_bst(root->right, key, value);
    else {
        strncpy(root->value, value, 99);
        root->value[99] = '\0';
    }
    fix_height(root);
    return root;
}

int balance_factor(Node* p) { return height(p->right) - height(p->left); }

Node* rotate_right(Node* p) {
    Node* q = p->left;
    p->left = q->right;
    q->right = p;
    fix_height(p);
    fix_height(q);
    return q;
}

Node* rotate_left(Node* q) {
    Node* p = q->right;
    q->right = p->left;
    p->left = q;
    fix_height(q);
    fix_height(p);
    return p;
}

Node* balance_tree(Node* root) {
    if (!root) return nullptr;
    root->left = balance_tree(root->left);
    root->right = balance_tree(root->right);

    fix_height(root);
    if (balance_factor(root) == 2) {
        if (balance_factor(root->right) < 0)
            root->right = rotate_right(root->right);
        return rotate_left(root);
    }
    if (balance_factor(root) == -2) {
        if (balance_factor(root->left) > 0)
            root->left = rotate_left(root->left);
        return rotate_right(root);
    }
    return root;
}

const char* search(Node* root, int key) {
    if (!root) return nullptr;
    if (key == root->key) return root->value;
    return search(key < root->key ? root->left : root->right, key);
}

void printTree(Node* root, const string& prefix = "", bool isLeft = false) {
    if (!root) return;
    cout << prefix << (isLeft ? "|-- " : "\\-- ") << root->key << " (" << root->value << ")\n";
    printTree(root->left, prefix + (isLeft ? "|   " : "    "), true);
    printTree(root->right, prefix + (isLeft ? "|   " : "    "), false);
}

Node* findMin(Node* root) {
    return root->left ? findMin(root->left) : root;
}

Node* remove(Node* root, int key) {
    if (!root) return nullptr;
    if (key < root->key)
        root->left = remove(root->left, key);
    else if (key > root->key)
        root->right = remove(root->right, key);
    else {
        if (!root->left || !root->right) {
            Node* temp = root->left ? root->left : root->right;
            delete root;
            return temp;
        }
        Node* min = findMin(root->right);
        root->key = min->key;
        strcpy(root->value, min->value);
        root->right = remove(root->right, min->key);
    }
    fix_height(root);
    return root;
}

// --- TREE TRAVERSALS ---
void inorder(Node* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->key << " (" << root->value << ") ";
    inorder(root->right);
}

void preorder(Node* root) {
    if (!root) return;
    cout << root->key << " (" << root->value << ") ";
    preorder(root->left);
    preorder(root->right);
}

void postorder(Node* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    cout << root->key << " (" << root->value << ") ";
}

int main() {
    Node* root = nullptr;
    int choice;

    do {
        cout << "\n======= MENU =======\n";
        cout << "1. Enter nodes (key, value)\n";
        cout << "2. Show tree\n";
        cout << "3. Balance tree\n";
        cout << "4. Search by key\n";
        cout << "5. Delete node\n";
        cout << "6. Exit\n";
        cout << "7. Tree traversal (in-order, pre-order, post-order)\n";
        cout << "Choice: ";
        cin >> choice;

        switch (choice) {
            case 1: {
                string input;
                int key;
                char value[100];
                cout << "Enter pairs ('--') to stop:\n";
                while (true) {
                    cout << "Key: ";
                    cin >> input;
                    if (input == "--") break;

                    try {
                        key = stoi(input);
                    } catch (...) {
                        cout << "Wrong key.\n";
                        continue;
                    }

                    cout << "Value: ";
                    cin >> value;
                    root = insert_bst(root, key, value);
                }
                break;
            }
            case 2:
                cout << "Tree:\n";
                printTree(root);
                break;

            case 3:
                root = balance_tree(root);
                cout << "Balanced tree:\n";
                printTree(root);
                break;

            case 4: {
                int to_search;
                cout << "Enter key to search: ";
                cin >> to_search;
                const char* result = search(root, to_search);
                if (result)
                    cout << "Value: " << result << "\n";
                else
                    cout << "The key is not found\n";
                break;
            }

            case 5: {
                int to_remove;
                cout << "Enter the key to remove: ";
                cin >> to_remove;
                root = remove(root, to_remove);
                cout << "Tree after deleting node:\n";
                printTree(root);
                break;
            }

            case 6:
                cout << "Exiting.\n";
                break;

            case 7: {
                int subChoice;
                cout << "\nTraversal options:\n";
                cout << "1. In-order\n";
                cout << "2. Pre-order\n";
                cout << "3. Post-order\n";
                cout << "Choice: ";
                cin >> subChoice;

                cout << "Traversal result:\n";
                switch (subChoice) {
                    case 1: inorder(root); break;
                    case 2: preorder(root); break;
                    case 3: postorder(root); break;
                    default: cout << "Invalid option\n"; break;
                }
                cout << endl;
                break;
            }

            default:
                cout << "Wrong.\n";
        }
    } while (choice != 6);

    return 0;
}
