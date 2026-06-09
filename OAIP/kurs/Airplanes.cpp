#include "iostream"
#include "Airplanes.h"
#include "cstring"

void number_linear_search(Airplane flights[], int size, int number) {
    bool flag = false;
    for (int i = 0; i < size; i++) {
        if (number == flights[i].get_flight_number()) {
            std::cout << "The race is found at index " << i << ".\n";
            flag = true;
        }
    }
    if(!flag) {
        std::cout << "The race is not found.\n";
    }
}

void passengers_choice_sort(Airplane flights[], int size) {
    for (int i = 0; i < size - 1; i++) {
        int min_index = i;
        for (int j = i + 1; j < size; j++) {
            if (flights[j].get_passengers_amount() < flights[min_index].get_passengers_amount()) {
                min_index = j;
            }
        }
        if (min_index != i) {
            Airplane temp = flights[i];
            flights[i] = flights[min_index];
            flights[min_index] = temp;
        }
    }
}

int time_binary_search(Airplane flights[], int size, int time) {
    int left = 0;
    int right = size - 1;

    while(left <= right) {
        int mid = left + (right - left) / 2;
        if (flights[mid].get_departure_time() == time) {
            return mid;
        }
        else if(flights[mid].get_departure_time() > time) {
            right = mid - 1;
        }
        else {
            left = mid + 1;
        }
    }
    return -1;
}

void insertion_sort(Airplane flights[], int size) {
    for (int i = 1; i < size; i++) {
        Airplane key = flights[i];
        int j = i - 1;
        while(strcmp(flights[j].get_airplane_type(), key.get_airplane_type()) > 0 && j >= 0) {
            flights[j + 1] = flights[j];
            j--;
        }
        flights[j + 1] = key;
    }
}

int partition(Airplane flights[], int low, int high) {
    const char* pivot = flights[high].get_arrive_city();
    int i = low - 1;
    for (int j = low; j <= high; j++) {
        if (strcmp(flights[j].get_arrive_city(), pivot) < 0) {
            i++;
            std::swap(flights[i], flights[j]);
        }
    }
    std::swap(flights[i + 1], flights[high]);
    return i;
}

void quicksort(Airplane flights[], int low, int high) {
    if (low < high) {
        int pi = partition(flights, low, high);
        quicksort(flights, low, pi - 1);
        quicksort(flights, pi + 1, high);
    }
}