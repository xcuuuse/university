#include "Queue.h"
#include <iostream>
using namespace std;

void display_menu() {
    cout << "\n--- Menu ---\n";
    cout << "1. Add elements to the list\n";
    cout << "2. View the list\n";
    cout << "3. Remove elements between min and max\n";
    cout << "4. Exit\n";
    cout << "Enter your choice: ";
}

int main() {
    Queue queue;
    int choice;
    bool exit_program = false;

    while (!exit_program) {
        display_menu();
        cin >> choice;

        switch (choice) {
            case 1: {
                int n, position;
                cout << "Enter the number of elements to add: ";
                cin >> n;
                cout << "Where do you want to add the elements?\n";
                cout << "1. At the beginning\n";
                cout << "2. At the end\n";
                cin >> position;

                if (position != 1 && position != 2) {
                    cout << "Invalid position. Elements will be added at the beginning by default.\n";
                    position = 1;
                }

                cout << "Enter " << n << " elements:\n";
                for (int i = 0; i < n; i++) {
                    int x;
                    cin >> x;
                    if (position == 1) {
                        queue.add_node(x); // Добавляем в начало
                    } else {
                        queue.add_node_to_end(x); // Добавляем в конец
                    }
                }
                cout << "Elements added successfully.\n";
                break;
            }
            case 2: {
                cout << "Current list: ";
                queue.print_data();
                break;
            }
            case 3: {
                queue.swap_elements();
                cout << "Updated list: ";
                queue.print_data();
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
