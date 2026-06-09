int find_max(int* arr, int index, int size){
    if (index == size - 1)
    {
        return arr[index];
    }
    return max(arr[index], find_max(arr, index + 1, size));
}
