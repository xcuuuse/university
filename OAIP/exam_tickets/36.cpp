int sum(int n){
    if (n == 0)
    {
        return 0;
    }
    if ((n % 10) % 2 != 0)
    {
        return n % 10 + sum(n / 10);
    }
    else{
        return sum(n / 10);
    }
}
