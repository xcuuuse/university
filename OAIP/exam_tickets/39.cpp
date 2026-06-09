int find_min(int* arr, int index, int size){
    if (index == size - 1)
    {
        return arr[index];
    }
    return min(arr[index], find_min(arr, index + 1, size));
}
