
#ifndef LAB1PIO_DSU_H
#define LAB1PIO_DSU_H
#include "bits/stdc++.h"
using namespace std;

class Dsu
{
private:
    vector <int> parent; // хранит родителя
    vector <int> rank; // ранг каждого элемента
public:
    Dsu(int size);// конструктор
    int find(int x); //поиск элемента
    //объединение
    void unite_two_sets(int x, int y);
    //указанный элемент
    int get_set(int x);

    int size() const;


};
#endif //LAB1PIO_DSU_H
