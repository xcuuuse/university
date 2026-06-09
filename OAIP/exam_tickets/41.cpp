#include "iostream"

using namespace std;

bool is_palindrome(char* s, int left, int right){
    if (left >= right)
    {
        return true;
    }
    else{
        if (s[left] != s[right])
        {
            return 0;
        }
    }
    return is_palindrome(s, left + 1, right - 1);
}


