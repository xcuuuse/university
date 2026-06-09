#ifndef KURS_WORK_AIRPLANES_H
#define KURS_WORK_AIRPLANES_H
#include "iostream"
#include "cstring"

struct Airplane{
private:
    int flight_number;
    int departure_time;
    char arrive_city[100];
    char depart_city[100];
    char airplane_type[100];
    int passengers_amount;
public:
    Airplane() : flight_number(0), departure_time(0), passengers_amount(0) {}

    // Конструктор с параметрами
    Airplane(int flightNum, int depTime, const char* arrCity, const char* depCity, const char* airType, int passAmount)
            : flight_number(flightNum), departure_time(depTime), passengers_amount(passAmount) {
        strcpy(arrive_city, arrCity);
        strcpy(depart_city, depCity);
        strcpy(airplane_type, airType);
    }

    int get_flight_number() const { return flight_number; }
    int get_departure_time() const { return departure_time; }
    const char* get_arrive_city() const { return arrive_city; }
    const char* get_depart_city() const { return depart_city; }
    const char* get_airplane_type() const { return airplane_type; }
    int get_passengers_amount() const { return passengers_amount; }

    // Сеттеры для изменения данных
    void set_flight_number(int num) { flight_number = num; }
    void set_departure_time(int time) { departure_time = time; }
    void set_arrive_city(const char* city) { strcpy(arrive_city, city); }
    void set_depart_city(const char* city) { strcpy(depart_city, city); }
    void set_airplane_type(const char* type) { strcpy(airplane_type, type); }
    void set_passengers_amount(int amount) { passengers_amount = amount; }
};

void number_linear_search(Airplane flights[], int size, int number);
void passengers_choice_sort(Airplane flights[], int size);
int time_binary_search(Airplane flights[], int size, int time);
void insertion_sort(Airplane flights[], int size);
int partition(Airplane flights[], int low, int high);
void quicksort(Airplane flights[], int low, int high);

#endif //KURS_WORK_AIRPLANES_H
