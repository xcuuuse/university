#include "bits/stdc++.h"

using namespace std;

double s(double x, int k)
{
    return pow(-1, (k + 1)) * (pow(x, (2 * k + 1))) / (4 * k * k - 1);
}

double y(double x)
{
    return ((1 + pow(x, 2)) / 2) * atan(x) - x / 2;
}

int main() {
    double temp1, temp2;
    double a, b, h, e;
    cin >> a >> b >> h >> e;

    cout << "       x    " << "    S(x)    " << "      Y(x)      "  << "    |S(x) - Y(x)|" << "\n";
    for (double x = a; x <= b; x += h)
    {
        double comp = x * x * x;
        temp1 = comp / 3;
        temp2 = y(x);
        int k = 1;

        while(fabs(temp2 - temp1) > e)
        {
            k++;
            comp *= -1 * x * x;
            temp1 += comp / (4 * k * k - 1);
        }
        cout << fixed << setprecision(9) << "|" << x << " | " << temp1 << " | "
             << temp2 << " | " << fabs((temp2 - temp1)) << " | " << k << " |\n";
    }

    return 0;
}