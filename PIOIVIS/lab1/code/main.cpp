#include "bits/stdc++.h"
#include "DSU.h"

using namespace std;

void input(Dsu &dsu)
{
    cout << "Enter the number of edges: ";
    int edges;
    cin >> edges;

    cout << "Enter edges as 'x y': \n";
    for (int i = 0; i < edges; i++)
    {
        int x, y;
        cin >> x >> y;

        if (x < 0 || x >= dsu.size() || y < 0 || y >= dsu.size()) {
            cout << "Error: elements must be in the range [0, " << dsu.size() - 1 << "]\n";
            i--;
            continue;
        }

        dsu.unite_two_sets(x, y);
    }

    cout << "Result of union:\n";
    for (int i = 0; i < dsu.size(); i++)
    {
        cout << dsu.get_set(i) << "\n";
    }
}

int main()
{
    const int size = 5;

    Dsu dsu(size);
    input(dsu);

    return 0;
}
