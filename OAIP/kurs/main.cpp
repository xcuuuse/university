#include "iostream"
#include "Airplanes.h"
#include "Files.h"
#include "fstream"
#include "ctime"
#include "limits"
using namespace std;

const char* SEARCH_HISTORY_FILE = "search_history.txt";

void log_search(const string& message) {
    ofstream log_file(SEARCH_HISTORY_FILE, ios::app);
    if (log_file) {
        time_t now = time(0);
        char* dt = ctime(&now);
        dt[strlen(dt)-1] = '\0'; // удаляем символ новой строки
        log_file << "[" << dt << "] " << message << "\n";
    }
}

void display_and_clear_history() {
    ifstream log_file(SEARCH_HISTORY_FILE);
    if (log_file) {
        cout << "\n=== Search History ===\n";
        string line;
        while (getline(log_file, line)) {
            cout << line << "\n";
        }
        cout << "=====================\n";
        log_file.close();

        // Очищаем файл
        ofstream clear_file(SEARCH_HISTORY_FILE, ios::trunc);
    }
}

void display_flights(Airplane flights[], int size) {
    printf("%-15s%-15s%-15s%-15s%-20s%-20s\n",
           "Flight", "Departure", "Departure", "Arrival", "Airplane", "Passengers");
    printf("%-15s%-15s%-15s%-15s%-20s%-20s\n",
           "number", "time", "city", "city", "type", "amount");
    for (int i = 0; i < size; i++) {
        printf("%-15d%-15d%-15s%-15s%-20s%-20d\n",
               flights[i].get_flight_number(),
               flights[i].get_departure_time(),
               flights[i].get_depart_city(),
               flights[i].get_arrive_city(),
               flights[i].get_airplane_type(),
               flights[i].get_passengers_amount());
    }
}

void passenger_stats(Airplane flights[], int size, int start_time, int end_time) {
    Airplane period_flights[100];
    int period_count = 0;
    int total_passengers = 0;

    for (int i = 0; i < size; i++) {
        if (flights[i].get_departure_time() >= start_time &&
            flights[i].get_departure_time() <= end_time) {
            period_flights[period_count++] = flights[i];
            total_passengers += flights[i].get_passengers_amount();
        }
    }

    if (period_count == 0) {
        string msg = "No flights found between " + to_string(start_time) + " and " + to_string(end_time);
        cout << msg << endl;
        log_search(msg);
        return;
    }

    // Сортировка по убыванию пассажиров
    for (int i = 1; i < period_count; i++) {
        Airplane key = period_flights[i];
        int j = i - 1;
        while (j >= 0 && period_flights[j].get_passengers_amount() < key.get_passengers_amount()) {
            period_flights[j + 1] = period_flights[j];
            j--;
        }
        period_flights[j + 1] = key;
    }

    string msg = "Passenger stats: " + to_string(total_passengers) +
                 " passengers between " + to_string(start_time) +
                 " and " + to_string(end_time);
    cout << "\n" << msg << "\n";
    log_search(msg);
    display_flights(period_flights, period_count);
}

int main() {
    const char *filename = "airplanes.bin";
    const char* report_name = "report.txt";
    create_file(filename);
    const int MAX_FLIGHTS = 100;
    Airplane flights[MAX_FLIGHTS];
    int choice;

    do {
        cout << "\nMenu:\n"
             << "1. View all flights\n"
             << "2. Add flight\n"
             << "3. Edit flight\n"
             << "4. Delete flight\n"
             << "5. Create report\n"
             << "6. Search by flight number\n"
             << "7. Search by departure time\n"
             << "8. Sort by arrival city\n"
             << "9. Sort by passengers\n"
             << "10. Sort by airplane type\n"
             << "11. Flights to city\n"
             << "12. Passenger statistics\n"
             << "13. Exit\n"
             << "Choice: ";

        // Input loop to ensure only valid integers are accepted
        while (!(cin >> choice)) {
            cout << "Invalid input. Please enter an integer: ";
            cin.clear(); // Clear the error flag
            cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Discard invalid input
        }

        // Process the choice
        switch (choice) {
            case 1: {
                int size = read_from_file_to_array(filename, flights, MAX_FLIGHTS);
                display_flights(flights, size);
                break;
            }
            case 2:
                add_to_file(filename);
                break;
            case 3:
                edit_info(filename);
                break;
            case 4:
                delete_from_file(filename);
                break;
            case 5:
                create_report_file(filename, report_name);
                break;
            case 6: {
                int number, size = read_from_file_to_array(filename, flights, MAX_FLIGHTS);
                cout << "Enter flight number: ";
                cin >> number;
                string msg = "Search by flight number: " + to_string(number);
                log_search(msg);
                number_linear_search(flights, size, number);
                break;
            }
            case 7: {
                int time, size = read_from_file_to_array(filename, flights, MAX_FLIGHTS);
                cout << "Enter departure time: ";
                cin >> time;
                string msg = "Search by departure time: " + to_string(time);
                log_search(msg);
                int index = time_binary_search(flights, size, time);
                if (index != -1) {
                    cout << "Flight found at index " << index << endl;
                    log_search("Found at index " + to_string(index));
                } else {
                    cout << "Flight not found\n";
                    log_search("Not found");
                }
                break;
            }
            case 8: {
                int size = read_from_file_to_array(filename, flights, MAX_FLIGHTS);
                quicksort(flights, 0, size-1);
                ofstream file(filename, ios::binary | ios::trunc);
                for (int i = 0; i < size; i++) {
                    file.write(reinterpret_cast<const char*>(&flights[i]), sizeof(Airplane));
                }
                file.close();
                cout << "Sorted by arrival city\n";
                log_search("Sorted flights by arrival city");
                break;
            }
            case 9: {
                int size = read_from_file_to_array(filename, flights, MAX_FLIGHTS);
                passengers_choice_sort(flights, size);
                ofstream file(filename, ios::binary | ios::trunc);
                for (int i = 0; i < size; i++) {
                    file.write(reinterpret_cast<const char*>(&flights[i]), sizeof(Airplane));
                }
                file.close();
                cout << "Sorted by passengers\n";
                log_search("Sorted flights by passengers amount");
                break;
            }
            case 10: {
                int size = read_from_file_to_array(filename, flights, MAX_FLIGHTS);
                insertion_sort(flights, size);
                ofstream file(filename, ios::binary | ios::trunc);
                for (int i = 0; i < size; i++) {
                    file.write(reinterpret_cast<const char*>(&flights[i]), sizeof(Airplane));
                }
                file.close();
                cout << "Sorted by airplane type\n";
                log_search("Sorted flights by airplane type");
                break;
            }
            case 11: {
                char city[100];
                int size = read_from_file_to_array(filename, flights, MAX_FLIGHTS);
                cout << "Enter arrival city: ";
                cin.ignore(); cin.getline(city, 100);

                string msg = "Search flights to city: " + string(city);
                log_search(msg);

                Airplane city_flights[100];
                int city_count = 0;
                for (int i = 0; i < size; i++) {
                    if (strcmp(flights[i].get_arrive_city(), city) == 0) {
                        city_flights[city_count++] = flights[i];
                    }
                }

                if (city_count == 0) {
                    cout << "No flights to this city\n";
                    log_search("No flights found to " + string(city));
                    break;
                }

                for (int i = 0; i < city_count-1; i++) {
                    for (int j = 0; j < city_count-i-1; j++) {
                        if (city_flights[j].get_departure_time() > city_flights[j+1].get_departure_time()) {
                            swap(city_flights[j], city_flights[j+1]);
                        }
                    }
                }

                display_flights(city_flights, city_count);
                log_search("Found " + to_string(city_count) + " flights");
                break;
            }
            case 12: {
                int start, end, size = read_from_file_to_array(filename, flights, MAX_FLIGHTS);
                cout << "Enter start time (HHMM): ";
                cin >> start;
                cout << "Enter end time (HHMM): ";
                cin >> end;
                passenger_stats(flights, size, start, end);
                break;
            }
            case 13:
                display_and_clear_history();
                cout << "Goodbye!\n";
                break;
            default:
                cout << "Invalid choice\n";
        }

        // Clear the input buffer
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

    } while (choice != 13);

    return 0;
}