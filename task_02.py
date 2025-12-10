def float_binary_search(arr, x):
    """
    Perform a binary search on a sorted array of floating-point numbers.
    """
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] >= x:
            upper_bound = arr[mid]
            high = mid - 1
        else:
            low = mid + 1

    return iterations, upper_bound
