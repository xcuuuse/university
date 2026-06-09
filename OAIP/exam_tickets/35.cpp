int maxi(int n){
    if (n == 0)
    {
        return 0;
    }
    return max(n % 10, maxi(n /  10));
}
