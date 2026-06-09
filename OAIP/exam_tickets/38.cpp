int amount(int n){
    if (n == 0)
    {
        return 0;
    }
    if ((n % 10) % 2 == 0)
    {
        return 1 + amount(n / 10);
    }
    else{
        return 0 + amount(n / 10);
    }
}
