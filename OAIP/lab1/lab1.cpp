#include "bits/stdc++.h"

using namespace std;

double rec(double value, double sum)
{
    return value == 0 ? sqrt(sum) : rec(value - 1, value + sqrt(sum));
}

double sqrt_2(double n)
{
    double res = 0;
    for (int i = n; i >= 1; i--)
    {
        res = sqrt(i + res);
    }
    return res;
}
int main()
{
    double n;
    while (true)
    {
        cin >> n;
        if (n <= 0 || round(n) != n)
        {
            cout << "Error" << "\n";
            continue;
        }
        else
        {
            double ans1 = rec(n - 1, n);
            double ans2 = sqrt_2(n);
            cout << ans1 << "\n";
            cout << ans2 << "\n";
            break;
        }
    }
}
