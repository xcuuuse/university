#include <bits/stdc++.h>

using namespace std;

int main()
{
    int n = 100;
    char *s = new char[n];
    char *ans = new char[n * 2];
    cout << "Enter the string:";
    cin.getline(s, n);
    for (int i = 0; i < strlen(s); i++)
    {
        ans[i] = s[strlen(s) - 1 - i];
    }

    for (int i = 0; i < strlen(s); i++)
    {
        ans[strlen(s) + i] = s[i];
    }

    ans[2 * strlen(s)] = '\0';

    cout << ans;

    delete[] s;
    delete[] ans;


    return 0;
}