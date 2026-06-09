#include "Stack.h"
#include <bits/stdc++.h>
using namespace std;

// Функция для отображения меню
void display_menu() {
    cout << "\n--- Menu ---\n";
    cout << "1. Add elements to the stack\n";
    cout << "2. View the stack\n";
    cout << "3. Replace\n";
    cout << "4. Exit\n";
    cout << "Enter your choice: ";
}

int main()
{
    Stack stack;
    int choice;
    bool exit_program = false;

    while (!exit_program) {
        display_menu();
        cin >> choice;

        switch (choice) {
            case 1: {
                int n;
                cout << "Enter the number of elements to add: ";
                cin >> n;
                cout << "Enter " << n << " elements:\n";
                for (int i = 0; i < n; i++) {
                    int x;
                    cin >> x;
                    stack.add_node(x);
                }
                cout << "Elements added successfully.\n";
                break;
            }

            case 2: {
                cout << "Current stack: ";
                stack.print_data();
                break;
            }

            case 3: {
                stack.remove_between_min_max();
                cout << "Updated stack: ";
                stack.print_data();
                break;
            }


            case 4: {
                cout << "Exiting the program. Goodbye!\n";
                exit_program = true;
                break;
            }

            default: {
                cout << "Invalid choice. Please try again.\n";
                break;
            }
        }
    }

    return 0;
}