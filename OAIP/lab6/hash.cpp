#include "iostream"

using namespace std;


struct Hash{
    char surname[100];
    int points_amount;
    int place;
    bool is_empty = true;
    bool is_deleted = false;
};

int hash_function(int points){
    return points % 15;
}

void insert_table(Hash table[], const Hash& element){
    int index = hash_function(element.points_amount);
    int p = 0;
    int new_index = index;
    int deleted_index = -1;

    while (p < 15)
    {
        new_index = (index + p * p) % 15;

        if (table[new_index].is_empty) {
            if (deleted_index != -1) {
                table[deleted_index] = element;
                table[deleted_index].is_empty = false;
                table[deleted_index].is_deleted = false;
            } else {
                table[new_index] = element;
                table[new_index].is_empty = false;
                table[new_index].is_deleted = false;
            }
            return;
        } else if (table[new_index].is_deleted && deleted_index == -1) {
            deleted_index = new_index;
        }

        p++;
    }

    if (deleted_index != -1) {
        table[deleted_index] = element;
        table[deleted_index].is_empty = false;
        table[deleted_index].is_deleted = false;
    } else {
        cout << "The table is full.\n";
    }
}


int search(Hash table[], int key){
    int index = hash_function(key);
    int p = 0;
    int new_index;

    while (p < 15)
    {
        new_index = (index + p * p) % 15;

        if (!table[new_index].is_empty) {
            if (!table[new_index].is_deleted && table[new_index].points_amount == key) {
                return new_index;
            }
        } else {
            break;
        }

        p++;
    }
    return -1;
}

void delete_from_table(Hash table[], int key)
{
    int index = search(table, key);
    if (index != -1)
    {
        table[index].is_deleted = true;
        cout << "The element is deleted\n";
    }
    else
    {
        cout << "No element\n";
    }
}

void print_array(Hash participants[], int n)
{
    for (int i = 0; i < n; i++)
    {
        cout << participants[i].surname << " " <<  participants[i].points_amount << " " <<
        participants[i].place << "\n";
    }
}

void print_table(Hash table[]){
    for (int i = 0; i < 15; i++)
    {
        if (!table[i].is_empty && !table[i].is_deleted)
        {
            cout << i << ": " << table[i].surname << " " << table[i].points_amount << " "
                 << table[i].place << "\n";
        }
        else {
            cout << i << ": ---\n";
        }
    }
}


int main(){
    Hash* participants = nullptr;
    int n = 0;
    Hash hash[15];
    bool table_built = false;
    int choice;
    do{
        cout << "\nMENU:\n";
        cout << "1. Enter participant\n";
        cout << "2. Build hashtable\n";
        cout << "3. Print array\n";
        cout << "4. Print table\n";
        cout << "5. Search by points\n";
        cout << "6. Add new\n";
        cout << "7. Delete participant\n";
        cout << "8. Exit\n";
        cout << "Choice: ";
        cin >> choice;
        switch (choice) {
            case 1:
                delete[] participants;
                cout << "Enter amount of people: ";
                cin >> n;
                participants = new Hash[n];
                for (int i = 0; i < n; i++)
                {
                    cout << "Participant " << i + 1 << ":\n";
                    cout << "Surname: ";
                    cin >> participants[i].surname;
                    cout << "Points: ";
                    cin >> participants[i].points_amount;
                   // cout << "Place: ";
                   // cin >> participants[i].place;
                }
                table_built = false;
                break;
            case 2:
                if (!participants || n == 0) {
                    cout << "Enter participants!\n";
                    break;
                }
                for (int i = 0; i < 15; i++) {
                    hash[i].is_empty = true;
                    hash[i].is_deleted = false;
                }
                for (int i = 0; i < n; i++) {
                    insert_table(hash, participants[i]);
                }
                table_built = true;
                cout << "The table is built.\n";
                break;

            case 3:
                if (participants)
                    print_array(participants, n);
                else
                    cout << "The array is not entered.\n";
                break;
            case 4:
                if (table_built)
                    print_table(hash);
                else
                    cout << "Build table.\n";
                break;
            case 5:
                if (!table_built) {
                    cout << "Build table.\n";
                    break;
                }
                int key;
                cout << "Enter amount of points: ";
                cin >> key;
                {
                    int index = search(hash, key);
                    if (index != -1) {
                        cout << "Element:\n";
                        cout << hash[index].surname << " "
                             << hash[index].points_amount << " "
                             << hash[index].place << "\n";
                    } else {
                        cout << "Element is not found.\n";
                    }
                }
                break;
            case 6:
                if (!table_built) {
                    cout << "Build table.\n";
                    break;
                }
                {
                    Hash newElement;
                    cout << "Surname: ";
                    cin >> newElement.surname;
                    cout << "Points: ";
                    cin >> newElement.points_amount;
                   // cout << "Place: ";
                   // cin >> newElement.place;
                    insert_table(hash, newElement);
                }
                break;
            case 7:
                if (!table_built) {
                    cout << "Build table.\n";
                    break;
                }
                {
                    int delKey;
                    cout << "Enter amount of points to delete: ";
                    cin >> delKey;
                    delete_from_table(hash, delKey);
                }
                break;

            case 8:
                cout << "Exiting.\n";
                break;

            default:
                cout << "Wrong.\n";

        }
    } while (choice != 8);

    delete[] participants;
    return 0;

}


