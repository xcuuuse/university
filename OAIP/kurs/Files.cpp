#include "Files.h"
#include "iostream"
#include "fstream"
#include "cstring"
#include "Airplanes.h"
#include "limits"
#include "cctype"
#include "bits/stdc++.h"
void create_file(const char* filename)
{
    std::ofstream file(filename, std::ios::binary | std::ios::trunc);
    if (!file)
    {
        std::cout << "Cannot create the file.\n";
        return;
    }
    Airplane initial_flights[] = {
            {101, 600, "Paris", "Moscow", "Boeing 737", 150},
            {102, 700, "New-York", "London", "Airbus A320", 200},
            {103, 800, "Tokyo", "Beijing", "Boeing 777", 300},
            {104, 900, "Berlin", "Moscow", "Airbus A321", 180}
    };
    int size = sizeof(initial_flights) / sizeof(Airplane);

    for (int i = 0; i < size; i++)
    {
        file.write(reinterpret_cast<const char*>(&initial_flights[i]), sizeof(Airplane));
    }

    file.close();

}

void view_info(const char* filename)
{
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        std::cout << "Cannot open file for reading.\n";
        return;
    }

    printf("%-15s%-15s%-15s%-15s%-20s%-20s\n",
           "Flight number", "Departure time", "Departure city", "Arrival city", "Airplane type", "Passengers amount");

    Airplane temp;
    while (file.read(reinterpret_cast<char*>(&temp), sizeof(Airplane))) {
        printf("%-15d%-15d%-15s%-15s%-20s%-20d\n",
               temp.get_flight_number(),
               temp.get_departure_time(),
               temp.get_depart_city(),
               temp.get_arrive_city(),
               temp.get_airplane_type(),
               temp.get_passengers_amount());
    }

    file.close();
}
bool is_valid_time(int time) {
    if (time < 0 || time > 2359) return false;

    int hours = time / 100;
    int minutes = time % 100;

    return (hours >= 0 && hours <= 23) && (minutes >= 0 && minutes <= 59);
}
void add_to_file(const char* filename) {
    std::ofstream file(filename, std::ios::binary | std::ios::app);
    if (!file) {
        std::cout << "Cannot open file for appending.\n";
        return;
    }

    Airplane new_flight;

    // Функция для проверки, что строка содержит только буквы и пробелы
    auto is_valid_string = [](const char* str) {
        for (int i = 0; str[i] != '\0'; ++i) {
            if (!isalpha(str[i]) && !isspace(str[i])) {
                return false;
            }
        }
        return true;
    };

    // Ввод номера рейса с проверкой
    int flight_number;
    while (true) {
        std::cout << "Enter flight number: ";
        if (std::cin >> flight_number && flight_number > 0) {
            new_flight.set_flight_number(flight_number);
            break;
        }
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Error: Flight number must be a positive integer!\n";
    }

    // Ввод времени вылета с проверкой (0-2359)
    int departure_time;
    while (true) {
        std::cout << "Enter departure time (HHMM format, e.g. 1430): ";
        if (std::cin >> departure_time && is_valid_time(departure_time)) {
            new_flight.set_departure_time(departure_time);
            break;
        }
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Error: Time must be in HHMM format (0000-2359) with valid hours (00-23) and minutes (00-59)!\n";
    }

    // Ввод города отправления с проверкой
    char dep_city[100];
    std::cin.ignore();
    while (true) {
        std::cout << "Enter departure city: ";
        std::cin.getline(dep_city, 100);
        if (strlen(dep_city) > 0 && is_valid_string(dep_city)) {
            new_flight.set_depart_city(dep_city);
            break;
        }
        std::cout << "Error: City name can only contain letters and spaces!\n";
    }

    // Ввод города прибытия с проверкой
    char arr_city[100];
    while (true) {
        std::cout << "Enter arrival city: ";
        std::cin.getline(arr_city, 100);
        if (strlen(arr_city) > 0 && is_valid_string(arr_city)) {
            new_flight.set_arrive_city(arr_city);
            break;
        }
        std::cout << "Error: City name can only contain letters and spaces!\n";
    }

    // Ввод типа самолета с проверкой
    char type[100];
    while (true) {
        std::cout << "Enter airplane type: ";
        std::cin.getline(type, 100);
        if (strlen(type) > 0) {  // Можно добавить дополнительные проверки
            new_flight.set_airplane_type(type);
            break;
        }
        std::cout << "Error: Airplane type cannot be empty!\n";
    }

    // Ввод количества пассажиров с проверкой
    int pass_amount;
    while (true) {
        std::cout << "Enter passengers amount: ";
        if (std::cin >> pass_amount && pass_amount >= 0) {
            new_flight.set_passengers_amount(pass_amount);
            break;
        }
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Error: Passengers amount must be a non-negative integer!\n";
    }

    file.write(reinterpret_cast<const char*>(&new_flight), sizeof(Airplane));
    file.close();
    std::cout << "New flight has been added to the file.\n";
}
void edit_info(const char* filename)
{
    std::ifstream file(filename, std::ios::binary);
    if(!file)
    {
        std::cout << "Troubles with file opening.\n";
        return;
    }

    int number_to_edit;
    std::cout << "Enter flight number to edit: ";
    std::cin >> number_to_edit;
    Airplane temp;
    bool found = false;
    int index = 0;

    while(file.read(reinterpret_cast<char*>(&temp), sizeof(Airplane)))
    {
        if (temp.get_flight_number() == number_to_edit)
        {
            found = true;
            break;
        }
        index++;
    }
    file.close();

    if (!found)
    {
        std::cout << "Flight with this number is not found.\n";
        return;
    }

    std::fstream update_file(filename, std::ios::binary | std::ios::in | std::ios::out);
    if (!update_file)
    {
        std::cout << "Troubles with file opening.\n";
        return;
    }

    update_file.seekp(index * sizeof(Airplane), std::ios::beg);

    Airplane updated_flight;
    updated_flight.set_flight_number(temp.get_flight_number());
    std::cout << "Enter new departure time (current: " << temp.get_departure_time() << "): ";
    int new_time; std::cin >> new_time;
    updated_flight.set_departure_time(new_time);

    std::cout << "Enter new departure city (current: " << temp.get_depart_city() << "): ";
    std::cin.ignore(); // Очищаем буфер после числа
    char new_depart_city[100]; std::cin.getline(new_depart_city, 100);
    updated_flight.set_depart_city(new_depart_city);

    std::cout << "Enter new arrival city (current: " << temp.get_arrive_city() << "): ";
    char new_arrival_city[100]; std::cin.getline(new_arrival_city, 100);
    updated_flight.set_arrive_city(new_arrival_city);

    std::cout << "Enter new airplane type (current: " << temp.get_airplane_type() << "): ";
    char new_type[100]; std::cin.getline(new_type, 100);
    updated_flight.set_airplane_type(new_type);

    std::cout << "Enter new passengers amount (current: " << temp.get_passengers_amount() << "): ";
    int new_amount; std::cin >> new_amount;
    updated_flight.set_passengers_amount(new_amount);

    update_file.write(reinterpret_cast<const char*>(&updated_flight), sizeof(Airplane));

    update_file.close();
    std::cout << "Flight with number " << number_to_edit << " has been updated.\n";



}

void delete_from_file(const char* filename)
{
    std::ifstream file(filename, std::ios::binary);
    if (!file)
    {
        std::cout << "Troubles with file opening.\n";
        return;
    }

    int number_to_delete;
    std::cout << "Enter the number to delete: ";
    std::cin >> number_to_delete;

    const char* temp_filename = "temp.bin";

    std::ofstream temp_file(temp_filename, std::ios::binary);
    if (!temp_file)
    {
        std::cout << "Troubles with creating file.\n";
        file.close();
        return;
    }

    Airplane temp;
    bool found = false;

    while(file.read(reinterpret_cast<char*>(&temp), sizeof(Airplane)))
    {
        if (temp.get_flight_number() == number_to_delete)
        {
            found = true;
            continue;
        }
        temp_file.write(reinterpret_cast<const char*>(&temp), sizeof(Airplane));
    }

    file.close();
    temp_file.close();

    if (!found)
    {
        std::cout << "Flight with number " << number_to_delete << " is not found.\n";
        remove(temp_filename);
        return;
    }

    remove(filename);
    rename(temp_filename, filename);

    std::cout << "Flight with number " << number_to_delete << " was successfully deleted.\n";
}

void create_report_file(const char* binary_filename, const char* report_filename)
{
    std::ifstream binary_file(binary_filename, std::ios::binary);
    if (!binary_file)
    {
        std::cout << "Cannot open binary file for reading.\n";
        return;
    }
    std::ofstream report_file(report_filename);
    if (!report_file) {
        std::cout << "Cannot create report file.\n";
        binary_file.close();
        return;
    }

    report_file << "Flight Report\n";
    report_file << "-----------------------------\n";
    report_file << std::setw(15) << std::left << "Flight number"
                << std::setw(15) << std::left << "Departure time"
                << std::setw(15) << std::left << "Depart city"
                << std::setw(15) << std::left << "Arrive city"
                << std::setw(20) << std::left << "Airplane type"
                << std::setw(20) << std::left << "Passengers amount\n";
    report_file << "-----------------------------\n";

    Airplane temp; // Временный объект для чтения данных
    while (binary_file.read(reinterpret_cast<char*>(&temp), sizeof(Airplane))) {
        // Записываем данные о каждом рейсе в текстовый файл
        report_file << std::setw(15) << std::left << temp.get_flight_number()
                    << std::setw(15) << std::left << temp.get_departure_time()
                    << std::setw(15) << std::left << temp.get_depart_city()
                    << std::setw(15) << std::left << temp.get_arrive_city()
                    << std::setw(20) << std::left << temp.get_airplane_type()
                    << std::setw(20) << std::left << temp.get_passengers_amount() << "\n";
    }

    binary_file.close();
    report_file.close();

    std::cout << "Report has been created in file: " << report_filename << "\n";
}

int read_from_file_to_array(const char* filename, Airplane flights[], int max_size) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        std::cout << "Cannot open file for reading.\n";
        return 0;
    }

    int count = 0;
    while (count < max_size && file.read(reinterpret_cast<char *>(&flights[count]), sizeof(Airplane))) {
        if (strlen(flights[count].get_arrive_city()) == 0 || strlen(flights[count].get_depart_city()) == 0 ||
            strlen(flights[count].get_airplane_type()) == 0) {
            break;
        }
        count++;
    }

    file.close();
    return count;
}