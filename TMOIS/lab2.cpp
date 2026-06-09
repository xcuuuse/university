#include "bits/stdc++.h"

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    int n, m;
    cout << "Enter the number of pairs for set P: ";
    cin >> n;
    cout << "Enter the pairs of set P:\n";

    set<pair<string, string>> unique_P;
    vector<string> P(n * 2);

    for (int i = 0; i < n * 2; i += 2) {
        string a, b;
        cin >> a >> b;
        if (!unique_P.insert({a, b}).second)
        {
            cout << "Duplicate pair found in set P: <" << a << ", " << b << ">\n";
            return 1;
        }

        P[i] = a;
        P[i + 1] = b;
    }

    cout << "Enter the number of pairs for set Q: ";
    cin >> m;
    cout << "Enter the pairs of set Q:\n";

    set<pair<string, string>> unique_Q;
    vector<string> Q(m * 2);

    for (int i = 0; i < m * 2; i += 2) {
        string a, b;
        cin >> a >> b;

        if (!unique_Q.insert({a, b}).second) {
            cout << "Duplicate pair found in set Q: <" << a << ", " << b << ">\n";
            return 1;
        }

        Q[i] = a;
        Q[i + 1] = b;
    }
    vector<string> p_x, p_y;
    vector<string> q_x, q_y;
    for (int i = 0; i <= n; i += 2) {
        p_x.push_back(P[i]);
    }
    for (int i = 1; i <= n +1; i += 2) {
        p_y.push_back(P[i]);
    }
    for (int i = 0; i <= m; i += 2) {
        q_x.push_back(Q[i]);
    }
    for (int i = 1; i <= m+ 1; i += 2) {
        q_y.push_back(Q[i]);
    }


    cout << "\n";
    vector<string> comp;
    for (int i = 0; i < n * 2; i += 2) {
        string p1 = P[i];
        string p2 = P[i + 1];

        for (int j = 0; j < m * 2; j += 2)
        {
            string q1 = Q[j];
            string q2 = Q[j + 1];

            if (p2 == q1)
            {
                comp.push_back("<" + p1 + " " + q2 + ">");
            }
        }
    }

    vector<string> dekart;
    for (int i = 0; i < n * 2; i += 2) {
        string p1 = P[i];
        string p2 = P[i + 1];

        for (int j = 0; j < m * 2; j += 2) {
            string q1 = Q[j];
            string q2 = Q[j + 1];

            dekart.push_back("{" + p1 + ", " + p2 + ", " + q1 + ", " + q2 + "}");
        }
    }

    // Invert pairs
    for (int i = 0; i < n * 2; i += 2)
    {
        swap(P[i], P[i + 1]);
    }

    for (int i = 0; i < m * 2; i += 2)
    {
        swap(Q[i], Q[i + 1]);
    }

    cout << "Proection i1 on P: ";
    for (auto i : p_x)
    {
        cout << i << " ";
    }
    cout << "\n" << "Proection i2 on P:";
    for (auto i : p_y)
    {
        cout << i << " ";
    }
    cout << "\n" << "Proection i1 on Q:";
    for (auto i : q_x)
    {
        cout << i << " ";
    }
    cout << "\n" << "Proection i2 on Q:";
    for (auto i : q_y)
    {
        cout << i << " ";
    }
    cout << "\n";
    cout << "Inverted pairs of P: ";
    for (int i = 0; i < P.size(); i++) {
        if (i % 2 == 0)
        {
            cout << "<" << P[i];
        }
        else
        {
            cout << " " << P[i] << ">";
        }
    }
    cout << "\n";

    cout << "Inverted pairs of Q: ";
    for (int i = 0; i < Q.size(); i++)
    {
        if (i % 2 == 0)
        {
            cout << "<" << Q[i];
        }
        else
        {
            cout << " " << Q[i] << ">";
        }
    }
    cout << "\n";

    if (comp.empty())
    {
        cout << "No composite pairs\n";
    }
    else
    {
        cout << "Composition: ";
        for (int i = 0; i < comp.size(); i++)
        {
            cout << comp[i];
            if ((i % 2 == 1) && (i < comp.size() - 1))
            {
                cout << ", ";
            }
        }
        cout << "\n";
    }

    cout << "Cartesian Product: ";
    for (auto i: dekart)
    {
        cout << i << " ";
    }
    cout << "\n";

    return 0;
}
