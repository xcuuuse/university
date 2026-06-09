#include "bits/stdc++.h"

using namespace std;
int fib_rec(int n)
{
    if (n == 0 || n == 1) return 1;
    return fib_rec(n - 1) + fib_rec(n - 2);
}
int fib_iter(int n)
{
    if (n == 0 || n == 1) return 1;
    int a = 1, b = 1, c;
    for (int i = 2; i <= n; i++)
    {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}
int main()
{
    double n;
    while(true)
    {
        cin >> n;
        if (n < 0 || round(n) != n)
        {
            cout << "Error, try again" << "\n";
            continue;
        }
        else
        {
            cout << fib_rec(n - 1) << "\n" << fib_iter(n - 1);
            break;
        }
    }

}
