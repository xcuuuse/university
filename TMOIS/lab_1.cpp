#include <bits/stdc++.h>

using namespace std;

bool check(vector <int> arr) //Проверка на наличие одинаковых элементов
{
    for (int i = 0; i < arr.size(); i++)
    {
        for (int j = i + 1; j < arr.size(); j++)
        {
            if (arr[i] == arr[j])
            {
                return true;
            }
        }
    }
    return false;
}

bool is_in_range(vector <int> arr, int x, int y) //Проверка на наличие элементов в универсуме
{
    for (int i : arr)
    {
        if (i < x || i > y)
        {
            return false;
        }
    }
    return true;
}


int main()
{
    int x, y;
    cout << "Enter set boundaries:" << "\n";
    cin >> x >> y;
    int a, b;
    cout << "Enter power of set A:" << "\n";
    cin >> a;
    cout << "Enter set A:" << "\n";
    vector <int> arr(a);
    for (int i = 0; i < a; i++)
    {
        cin >> arr[i];
    }
    cout << "Enter power  of set B: " << "\n";
    cin >> b;
    vector <int> brr(b);
    cout << "Enter set B:" << "\n";
    for (int i = 0; i < b; i++)
    {
        cin >> brr[i];
    }

    if (is_in_range(arr, x, y) && is_in_range(brr, x, y))
    {
        ;
    }
    else
    {
        cout << "Error. The sets have to be in universum range. Please try again.";
        return 1;
    }
    if (check(arr)) //Если есть одинавоквые элементы, работа прерывается
    {
        cout << "The set must not contain identical elements." << endl;
        return 0;
    }
    if (check(brr))
    {
        cout << "The set must not contain identical elements." << endl;
        return 0;
    }

    //ОБЪЕДИНЕНИЕ

    vector <int> ob;
    for (int i : arr)
    {
        ob.push_back(i);
    }
    for (int i : brr)
    {
        bool flag = false;
        for (int j : ob)
        {
            if(i == j)
            {
                flag = true;
                break;
            }
        }
        if (!flag)
        {
            ob.push_back(i);
        }
    }
    cout << "Association: ";
    for (int i : ob)
    {
        cout << i << " ";
    }
    cout << endl;


    //ПЕРЕСЕЧЕНИЕ
    vector <int> per;
    for (int i : brr)
    {
        for (int j : arr)
        {
            if (i == j)
            {
                per.push_back(i);
            }
        }
    }
    cout << "Intersection: ";
    for (int i : per)
    {
        cout << i << " ";
    }
    cout << endl;


    //A - B
    vector <int> raznab;

    for (int i : arr)
    {
        bool flag = false;
        for (int j : brr)
        {
            if (i == j)
            {
                flag = true;
                break;
            }
        }
        if (!flag)
        {
            raznab.push_back(i);
        }
    }
    cout << "Difference between A and B: ";
    for (int i : raznab)
    {
        cout << i << " ";
    } cout << endl;

    //B - A
    vector <int> raznba;

    for (int i : brr)
    {
        bool flag = false;
        for (int j : arr)
        {
            if (i == j)
            {
                flag = true;
                break;
            }
        }

        if (!flag)
        {
            raznba.push_back(i);
        }
    }
    cout << "Difference between B and A: ";
    for (int i : raznba)
    {
        cout << i << " ";
    }
    cout << endl;


    //СИММЕТРИЧНАЯ РАЗНОСТЬ

    vector <int> symm;

    for (int i : raznab) {
        symm.push_back(i);
    }

    for (int i : raznba)
    {
        bool flag = false;
        for (int j : symm)
        {
            if (i == j)
            {
                flag = true;
                break;
            }
        }
        if(!flag)
        {
            symm.push_back(i);
        }
    }
    cout << "Symmetric difference: ";
    for (int i : symm)
    {
        cout << i << " ";
    }
    cout << endl;


    //ДОПОЛНЕНИЕ A

    vector <int> dop_a;
    // int un_size_a = 15;
    for (int i = x; i <= y; i++) {
        bool flag = false;
        for (int j: arr) {
            if (i == j) {
                flag = true;
                break;
            }
        }
        if (!flag) {
            dop_a.push_back(i);
        }
    }
    cout << "Appendix A: ";
    for (int i : dop_a)
    {
        cout << i << " ";
    }
    cout << endl;


    //ДОПОЛНЕНИЕ В

    vector <int> dop_b;

    int un_size_b = 15;

    for (int i = x; i <= y; i++)
    {
        bool flag = false;
        for (int j : brr)
        {
            if (i == j)
            {
                flag = true;
                break;
            }
        }
        if (!flag)
        {
            dop_b.push_back(i);
        }
    }

    cout << "Appendix B: ";
    for (int i : dop_b)
    {
        cout << i << " ";
    }
    cout << endl;

    return 0;

}
