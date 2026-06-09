#include <bits/stdc++.h>

using namespace std;

int main()
{
    int n;
    cin >> n;
    int m = n;

    int** arr = new int*[n];
    for (int i = 0; i < n; i++)
    {
        arr[i] = new int[m];
    }

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            cin >> arr[i][j];
        }
    }

    int sum = 0;


    for (int i = 0; i < n; i++)
    {
        if (i % 2 != 0)  //индексы с 0
        {
            int temp_1 = arr[i][0];
            for (int j = 1; j < m; j++)
            {
                if (arr[i][j] > temp_1)
                {
                    temp_1 = arr[i][j];
                }
            }
            sum += temp_1;
        }
        else
        {
            int temp_2 = arr[i][0];
            for (int j = 1; j < m; j++)
            {
                if (arr[i][j] < temp_2)
                {
                    temp_2 = arr[i][j];
                }
            }
            sum += temp_2;
        }
    }

    cout << sum << endl;

    for (int i = 0; i < n; i++)
    {
        delete[] arr[i];
    }
    delete[] arr;

    return 0;
}