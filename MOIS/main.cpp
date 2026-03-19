//Гаврыш Иван Александрович РС-1

#include <iostream>
#include <cmath>

using  namespace std;

double GI_x(double x){
    return 3.7 * cos(1.8 * x + 1.2) - 0.7 * x * sin(pow(x, 2) + 0.6)
}

void GI_tabfun(double a, double b, int n){ // VOID == не возвращает тип данных, используется просто для каких то действий без возвращаемого типа
    double h = (b - a) / n;
    cout << "    x     :      y" << endl;
    for (double x = a; x <= b; x += h)
    { 
        cout << x << " " << fixed << GI_x(x) << setprecision(n % 4 + 2) << endl;
    }

}

// \n == endl

int main()
{
    cout << "вот тут выводишь всю хуйню";
    double a, b;
    int n = 6;
    GI_tabfun(a, b, n);
}