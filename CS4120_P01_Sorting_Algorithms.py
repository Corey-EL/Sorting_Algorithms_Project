import time
import random
import pandas as pd
import sys
sys.setrecursionlimit(8000) 

def fill_random_numbers(arr, SIZE):
	
	for i in range(SIZE):
		arr.append(random.randint(1, 1000000))


def fill_sorted_numbers(arr1, SIZE):
    step = 1000000 / SIZE
    for i in range(SIZE):
        arr1.append(int(i*step)+1)



# iniciate the arrays to be used in the fill functions

Arr_1000_Sorted = []
Arr_1000_Rand = []
Arr_2000_Sorted = []
Arr_2000_Rand = []
Arr_4000_Sorted = []
Arr_4000_Rand = []
Arr_8000_Sorted = []
Arr_8000_Rand = []

# fill in all arrays with elements of the desire size

fill_random_numbers(Arr_1000_Rand, 1000)
fill_sorted_numbers(Arr_1000_Sorted, 1000)
Arr_1000_Reverse = Arr_1000_Sorted[::-1]

fill_random_numbers(Arr_2000_Rand, 2000)
fill_sorted_numbers(Arr_2000_Sorted, 2000)
Arr_2000_Reverse = Arr_2000_Sorted[::-1]

fill_random_numbers(Arr_4000_Rand, 4000)
fill_sorted_numbers(Arr_4000_Sorted, 4000)
Arr_4000_Reverse = Arr_4000_Sorted[::-1]

fill_random_numbers(Arr_8000_Rand, 8000)
fill_sorted_numbers(Arr_8000_Sorted, 8000)
Arr_8000_Reverse = Arr_8000_Sorted[::-1]


# Table is created to store the observable data with headers
df = pd.DataFrame(columns=['Algorithm', 'Timer', 'Num of Comparisons'])

def bubble_sort(arr):
    n = len(arr)
    swapped = True
    last_swap_pos = n - 1
    comparisons = 0
    
    while swapped:
        swapped = False
        for i in range(last_swap_pos):
            comparisons += 1
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                last_swap_pos = i
        n -= 1
    return comparisons

def insertion_sort(arr):
    comparisons = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            comparisons += 1
        arr[j + 1] = key
        comparisons += j != i - 1 # increment comparisons if there was a swap
    return comparisons

def merge(arr, left, mid1, mid2, right):
    #Merge function to merge the arrays together after sorting
    n1, n2, n3 = mid1 - left + 1, mid2 - mid1, right - mid2
    L, M, R = arr[left:mid1+1], arr[mid1+1:mid2+1], arr[mid2+1:right+1]
    i, j, k, p = 0, 0, 0, left
    comparisons = 0
    
    while i < n1 and j < n2 and k < n3:
        if L[i] <= M[j] and L[i] <= R[k]:
            arr[p] = L[i]
            i += 1
        elif M[j] <= L[i] and M[j] <= R[k]:
            arr[p] = M[j]
            j += 1
        else:
            arr[p] = R[k]
            k += 1
        p += 1
        comparisons += 1
    while i < n1 and j < n2:
        if L[i] <= M[j]:
            arr[p] = L[i]
            i += 1
        else:
            arr[p] = M[j]
            j += 1
        p += 1
        comparisons += 1
    while j < n2 and k < n3:
        if M[j] <= R[k]:
            arr[p] = M[j]
            j += 1
        else:
            arr[p] = R[k]
            k += 1
        p += 1
        comparisons += 1
    while i < n1 and k < n3:
        if L[i] <= R[k]:
            arr[p] = L[i]
            i += 1
        else:
            arr[p] = R[k]
            k += 1
        p += 1
        comparisons += 1
    while i < n1:
        arr[p] = L[i]
        i += 1
        p += 1
        comparisons += 1
    while j < n2:
        arr[p] = M[j]
        j += 1
        p += 1
        comparisons += 1
    while k < n3:
        arr[p] = R[k]
        k += 1
        p += 1
        comparisons += 1
    return comparisons

def merge_sort_3way(arr, left, right):
    #Main 3-way Merge sort function that recursively divides the array into 3 subarrays
    
    if left < right:
        comparisons = 0
        mid1 = left + (right - left) // 3
        mid2 = left + 2 * (right - left) // 3
        comparisons += merge_sort_3way(arr, left, mid1)
        comparisons += merge_sort_3way(arr, mid1+1, mid2)
        comparisons += merge_sort_3way(arr, mid2+1, right)
        comparisons += merge(arr, left, mid1, mid2, right)
        return comparisons
    else:
        return 0

def merge_sort(arr):
    # function to make a call to the 3-way merge
    if (len(arr) == 0):
         return
    else:
        return merge_sort_3way(arr, 0, len(arr)-1)
   
def heap_sort(arr):
    n = len(arr)
    comparisons = 0

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        comparisons += heapify(arr, n, i)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        comparisons += heapify(arr, i, 0)

    return comparisons

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    # If left child is larger than root
    if l < n and arr[l] > arr[largest]:
        largest = l

    # If right child is larger than largest so far
    if r < n and arr[r] > arr[largest]:
        largest = r

    # If largest is not root
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        return 1 + heapify(arr, n, largest)
    else:
        return 1
 
def quicksort(arr):
    if len(arr) <= 1:
        return 0
    else:
        pivot = random.choice(arr)
        left = []
        right = []
        equal = []
        for element in arr:
            if element < pivot:
                left.append(element)
            elif element > pivot:
                right.append(element)
            else:
                equal.append(element)
        return len(arr) - 1 + quicksort(left) + quicksort(right)

# copies of the array are made for each iteration of the search algorithms

Arr_1000_Sorted_bubble = Arr_1000_Sorted.copy()
Arr_1000_Reverse_bubble = Arr_1000_Reverse.copy()
Arr_1000_Rand_bubble = Arr_1000_Rand.copy()

Arr_2000_Sorted_bubble = Arr_2000_Sorted.copy()
Arr_2000_Reverse_bubble = Arr_2000_Reverse.copy()
Arr_2000_Rand_bubble = Arr_2000_Rand.copy()

Arr_4000_Sorted_bubble = Arr_4000_Sorted.copy()
Arr_4000_Reverse_bubble = Arr_4000_Reverse.copy()
Arr_4000_Rand_bubble = Arr_4000_Rand.copy()

Arr_8000_Sorted_bubble = Arr_8000_Sorted.copy()
Arr_8000_Reverse_bubble = Arr_8000_Reverse.copy()
Arr_8000_Rand_bubble = Arr_8000_Rand.copy()
# break
Arr_1000_Sorted_insert = Arr_1000_Sorted.copy()
Arr_1000_Reverse_insert = Arr_1000_Reverse.copy()
Arr_1000_Rand_insert = Arr_1000_Rand.copy()

Arr_2000_Sorted_insert = Arr_2000_Sorted.copy()
Arr_2000_Reverse_insert = Arr_2000_Reverse.copy()
Arr_2000_Rand_insert = Arr_2000_Rand.copy()

Arr_4000_Sorted_insert = Arr_4000_Sorted.copy()
Arr_4000_Reverse_insert = Arr_4000_Reverse.copy()
Arr_4000_Rand_insert = Arr_4000_Rand.copy()

Arr_8000_Sorted_insert = Arr_8000_Sorted.copy()
Arr_8000_Reverse_insert = Arr_8000_Reverse.copy()
Arr_8000_Rand_insert = Arr_8000_Rand.copy()
#break
Arr_1000_Sorted_quick = Arr_1000_Sorted.copy()
Arr_1000_Reverse_quick = Arr_1000_Reverse.copy()
Arr_1000_Rand_quick = Arr_1000_Rand.copy()

Arr_2000_Sorted_quick = Arr_2000_Sorted.copy()
Arr_2000_Reverse_quick = Arr_2000_Reverse.copy()
Arr_2000_Rand_quick = Arr_2000_Rand.copy()

Arr_4000_Sorted_quick = Arr_4000_Sorted.copy()
Arr_4000_Reverse_quick = Arr_4000_Reverse.copy()
Arr_4000_Rand_quick = Arr_4000_Rand.copy()

Arr_8000_Sorted_quick = Arr_8000_Sorted.copy()
Arr_8000_Reverse_quick = Arr_8000_Reverse.copy()
Arr_8000_Rand_quick = Arr_8000_Rand.copy()
#break
Arr_1000_Sorted_heap = Arr_1000_Sorted.copy()
Arr_1000_Reverse_heap = Arr_1000_Reverse.copy()
Arr_1000_Rand_heap = Arr_1000_Rand.copy()

Arr_2000_Sorted_heap = Arr_2000_Sorted.copy()
Arr_2000_Reverse_heap = Arr_2000_Reverse.copy()
Arr_2000_Rand_heap = Arr_2000_Rand.copy()

Arr_4000_Sorted_heap = Arr_4000_Sorted.copy()
Arr_4000_Reverse_heap = Arr_4000_Reverse.copy()
Arr_4000_Rand_heap = Arr_4000_Rand.copy()

Arr_8000_Sorted_heap = Arr_8000_Sorted.copy()
Arr_8000_Reverse_heap = Arr_8000_Reverse.copy()
Arr_8000_Rand_heap = Arr_8000_Rand.copy()
#break
Arr_1000_Sorted_merge = Arr_1000_Sorted.copy()
Arr_1000_Reverse_merge = Arr_1000_Reverse.copy()
Arr_1000_Rand_merge = Arr_1000_Rand.copy()

Arr_2000_Sorted_merge = Arr_2000_Sorted.copy()
Arr_2000_Reverse_merge = Arr_2000_Reverse.copy()
Arr_2000_Rand_merge = Arr_2000_Rand.copy()

Arr_4000_Sorted_merge = Arr_4000_Sorted.copy()
Arr_4000_Reverse_merge = Arr_4000_Reverse.copy()
Arr_4000_Rand_merge = Arr_4000_Rand.copy()

Arr_8000_Sorted_merge = Arr_8000_Sorted.copy()
Arr_8000_Reverse_merge = Arr_8000_Reverse.copy()
Arr_8000_Rand_merge = Arr_8000_Rand.copy()

# Call to the bubble sort function with all 12 copies of the 12 original arrays and insert the results in a dataframe table
# Arr of size 1000
start_time_sorted = time.time_ns()
Arr_1000_Sorted_bubble_comp = bubble_sort(Arr_1000_Sorted_bubble)
end_time_sorted = time.time_ns()

start_time_rev = time.time_ns()
Arr_1000_Reverse_bubble_comp = bubble_sort(Arr_1000_Reverse_bubble)
end_time_rev = time.time_ns()

start_time_rand = time.time_ns()
Arr_1000_Rand_bubble_comp = bubble_sort(Arr_1000_Rand_bubble)
end_time_rand = time.time_ns()


data_b1 = [{'Algorithm': 'Bubble Sort_Sorted_1000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_1000_Sorted_bubble_comp},
        
        {'Algorithm': 'Bubble Sort_Reverse_1000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_1000_Reverse_bubble_comp},
        
        {'Algorithm': 'Bubble Sort_Rand_1000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_1000_Rand_bubble_comp}]

df_new_b1 = pd.concat([pd.DataFrame([d]) for d in data_b1], ignore_index=True)
df = pd.concat([df, df_new_b1], ignore_index=True)

# Arr of size 2000
start_time_sorted = time.time_ns()
Arr_2000_Sorted_bubble_comp = bubble_sort(Arr_2000_Sorted_bubble)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_2000_Reverse_bubble_comp = bubble_sort(Arr_2000_Reverse_bubble)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_2000_Rand_bubble_comp = bubble_sort(Arr_2000_Rand_bubble)
end_time_rand = time.time_ns()


data_b2 = [{'Algorithm': 'Bubble Sort_Sorted_2000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_2000_Sorted_bubble_comp},
        
        {'Algorithm': 'Bubble Sort_Reverse_2000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_2000_Reverse_bubble_comp},
        
        {'Algorithm': 'Bubble Sort_Rand_2000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_2000_Rand_bubble_comp}]

df_new_b2 = pd.concat([pd.DataFrame([d]) for d in data_b2], ignore_index=True)
df = pd.concat([df, df_new_b2], ignore_index=True)

# Arr of size 4000
start_time_sorted = time.time_ns()
Arr_4000_Sorted_bubble_comp = bubble_sort(Arr_4000_Sorted_bubble)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_4000_Reverse_bubble_comp = bubble_sort(Arr_4000_Reverse_bubble)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_4000_Rand_bubble_comp = bubble_sort(Arr_4000_Rand_bubble)
end_time_rand = time.time_ns()


data_b3 = [{'Algorithm': 'Bubble Sort_Sorted_4000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_4000_Sorted_bubble_comp},
        
        {'Algorithm': 'Bubble Sort_Reverse_4000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_4000_Reverse_bubble_comp},
        
        {'Algorithm': 'Bubble Sort_Rand_4000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_4000_Rand_bubble_comp}]

df_new_b3 = pd.concat([pd.DataFrame([d]) for d in data_b3], ignore_index=True)
df = pd.concat([df, df_new_b3], ignore_index=True)

# Arr of size 8000
start_time_sorted = time.time_ns()
Arr_8000_Sorted_bubble_comp = bubble_sort(Arr_8000_Sorted_bubble)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_8000_Reverse_bubble_comp = bubble_sort(Arr_8000_Reverse_bubble)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_8000_Rand_bubble_comp = bubble_sort(Arr_8000_Rand_bubble)
end_time_rand = time.time_ns()


data_b4 = [{'Algorithm': 'Bubble Sort_Sorted_8000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_8000_Sorted_bubble_comp},
        
        {'Algorithm': 'Bubble Sort_Reverse_8000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_8000_Reverse_bubble_comp},
        
        {'Algorithm': 'Bubble Sort_Rand_8000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_8000_Rand_bubble_comp}]

df_new_b4 = pd.concat([pd.DataFrame([d]) for d in data_b4], ignore_index=True)
df = pd.concat([df, df_new_b4], ignore_index=True)

# Call to the insertion sort function with all 12 copies of the 12 original arrays and insert the results in a dataframe table
# Arr of size 1000
start_time_sorted = time.time_ns()
Arr_1000_Sorted_insertion_comp = insertion_sort(Arr_1000_Sorted_insert)
end_time_sorted = time.time_ns()

start_time_rev = time.time_ns()
Arr_1000_Reverse_insertion_comp = insertion_sort(Arr_1000_Reverse_insert)
end_time_rev = time.time_ns()

start_time_rand = time.time_ns()
Arr_1000_Rand_insertion_comp = insertion_sort(Arr_1000_Rand_insert)
end_time_rand = time.time_ns()


data_i1 = [{'Algorithm': 'Insertion Sort_Sorted_1000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_1000_Sorted_insertion_comp},
        
        {'Algorithm': 'Insertion Sort_Reverse_1000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_1000_Reverse_insertion_comp},
        
        {'Algorithm': 'Insertion Sort_Rand_1000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_1000_Rand_insertion_comp}]

df_new_i1 = pd.concat([pd.DataFrame([d]) for d in data_i1], ignore_index=True)
df = pd.concat([df, df_new_i1], ignore_index=True)

# Arr of size 2000
start_time_sorted = time.time_ns()
Arr_2000_Sorted_insertion_comp = insertion_sort(Arr_2000_Sorted_insert)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_2000_Reverse_insertion_comp = insertion_sort(Arr_2000_Reverse_insert)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_2000_Rand_insertion_comp = insertion_sort(Arr_2000_Rand_insert)
end_time_rand = time.time_ns()


data_i2 = [{'Algorithm': 'Insertion Sort_Sorted_2000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_2000_Sorted_insertion_comp},
        
        {'Algorithm': 'Insertion Sort_Reverse_2000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_2000_Reverse_insertion_comp},
        
        {'Algorithm': 'Insertion Sort_Rand_2000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_2000_Rand_insertion_comp}]

df_new_i2 = pd.concat([pd.DataFrame([d]) for d in data_i2], ignore_index=True)
df = pd.concat([df, df_new_i2], ignore_index=True)

# Arr of size 4000
start_time_sorted = time.time_ns()
Arr_4000_Sorted_insertion_comp = insertion_sort(Arr_4000_Sorted_insert)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_4000_Reverse_insertion_comp = insertion_sort(Arr_4000_Reverse_insert)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_4000_Rand_insertion_comp = insertion_sort(Arr_4000_Rand_insert)
end_time_rand = time.time_ns()


data_i3 = [{'Algorithm': 'Insertion Sort_Sorted_4000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_4000_Sorted_insertion_comp},
        
        {'Algorithm': 'Insertion Sort_Reverse_4000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_4000_Reverse_insertion_comp},
        
        {'Algorithm': 'Insertion Sort_Rand_4000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_4000_Rand_insertion_comp}]

df_new_i3 = pd.concat([pd.DataFrame([d]) for d in data_i3], ignore_index=True)
df = pd.concat([df, df_new_i3], ignore_index=True)

# Arr of size 8000
start_time_sorted = time.time_ns()
Arr_8000_Sorted_insertion_comp = insertion_sort(Arr_8000_Sorted_insert)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_8000_Reverse_insertion_comp = insertion_sort(Arr_8000_Reverse_insert)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_8000_Rand_insertion_comp = insertion_sort(Arr_8000_Rand_insert)
end_time_rand = time.time_ns()


data_i4 = [{'Algorithm': 'Insertion Sort_Sorted_8000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_8000_Sorted_insertion_comp},
        
        {'Algorithm': 'Insertion Sort_Reverse_8000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_8000_Reverse_insertion_comp},
        
        {'Algorithm': 'Insertion Sort_Rand_8000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_8000_Rand_insertion_comp}]

df_new_i4 = pd.concat([pd.DataFrame([d]) for d in data_i4], ignore_index=True)
df = pd.concat([df, df_new_i4], ignore_index=True)

# Call to the quick sort function with all 12 copies of the 12 original arrays and insert the results in a dataframe table
# Arr of size 1000
start_time_sorted = time.time_ns()
Arr_1000_Sorted_quick_comp = quicksort(Arr_1000_Sorted_quick)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_1000_Reverse_quick_comp = quicksort(Arr_1000_Reverse_quick)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_1000_Rand_quick_comp = quicksort(Arr_1000_Rand_quick)
end_time_rand = time.time_ns()


data_q1 = [{'Algorithm': 'Quick Sort_Sorted_1000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_1000_Sorted_quick_comp},
        
        {'Algorithm': 'Quick Sort_Reverse_1000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_1000_Reverse_quick_comp},
        
        {'Algorithm': 'Quick Sort_Rand_1000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_1000_Rand_quick_comp}]

df_new_q1 = pd.concat([pd.DataFrame([d]) for d in data_q1], ignore_index=True)
df = pd.concat([df, df_new_q1], ignore_index=True)

# Arr of size 2000
start_time_sorted = time.time_ns()
Arr_2000_Sorted_quick_comp = quicksort(Arr_2000_Sorted_quick)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_2000_Reverse_quick_comp = quicksort(Arr_2000_Reverse_quick)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_2000_Rand_quick_comp = quicksort(Arr_2000_Rand_quick)
end_time_rand = time.time_ns()


data_q2 = [{'Algorithm': 'Quick Sort_Sorted_2000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_2000_Sorted_quick_comp},
        
        {'Algorithm': 'Quick Sort_Reverse_2000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_2000_Reverse_quick_comp},
        
        {'Algorithm': 'Quick Sort_Rand_2000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_2000_Rand_quick_comp}]

df_new_q2 = pd.concat([pd.DataFrame([d]) for d in data_q2], ignore_index=True)
df = pd.concat([df, df_new_q2], ignore_index=True)

# Arr of size 4000
start_time_sorted = time.time_ns()
Arr_4000_Sorted_quick_comp = quicksort(Arr_4000_Sorted_quick)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_4000_Reverse_quick_comp = quicksort(Arr_4000_Reverse_quick)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_4000_Rand_quick_comp = quicksort(Arr_4000_Rand_quick)
end_time_rand = time.time_ns()


data_q3 = [{'Algorithm': 'Quick Sort_Sorted_4000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_4000_Sorted_quick_comp},
        
        {'Algorithm': 'Quick Sort_Reverse_4000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_4000_Reverse_quick_comp},
        
        {'Algorithm': 'Quick Sort_Rand_4000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_4000_Rand_quick_comp}]

df_new_q3 = pd.concat([pd.DataFrame([d]) for d in data_q3], ignore_index=True)
df = pd.concat([df, df_new_q3], ignore_index=True)

# Arr of size 8000
start_time_sorted = time.time_ns()
Arr_8000_Sorted_quick_comp = quicksort(Arr_8000_Sorted_quick)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_8000_Reverse_quick_comp = quicksort(Arr_8000_Reverse_quick)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_8000_Rand_quick_comp = quicksort(Arr_8000_Rand_quick)
end_time_rand = time.time_ns()


data_q4 = [{'Algorithm': 'Quick Sort_Sorted_8000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_8000_Sorted_quick_comp},
        
        {'Algorithm': 'Quick Sort_Reverse_8000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_8000_Reverse_quick_comp},
        
        {'Algorithm': 'Quick Sort_Rand_8000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_8000_Rand_quick_comp}]

df_new_q4 = pd.concat([pd.DataFrame([d]) for d in data_q4], ignore_index=True)
df = pd.concat([df, df_new_q4], ignore_index=True)

# Call to the heap sort function with all 12 copies of the 12 original arrays and insert the results in a dataframe table
# Arr of size 1000
start_time_sorted = time.time_ns()
Arr_1000_Sorted_heap_comp = heap_sort(Arr_1000_Sorted_heap)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_1000_Reverse_heap_comp = heap_sort(Arr_1000_Reverse_heap)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_1000_Rand_heap_comp = heap_sort(Arr_1000_Rand_heap)
end_time_rand = time.time_ns()


data_h1 = [{'Algorithm': 'Heap Sort_Sorted_1000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_1000_Sorted_heap_comp},
        
        {'Algorithm': 'Heap Sort_Reverse_1000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_1000_Reverse_heap_comp},
        
        {'Algorithm': 'Heap Sort_Rand_1000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_1000_Rand_heap_comp}]

df_new_h1 = pd.concat([pd.DataFrame([d]) for d in data_h1], ignore_index=True)
df = pd.concat([df, df_new_h1], ignore_index=True)

# Arr of size 2000
start_time_sorted = time.time_ns()
Arr_2000_Sorted_heap_comp = heap_sort(Arr_2000_Sorted_heap)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_2000_Reverse_heap_comp = heap_sort(Arr_2000_Reverse_heap)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_2000_Rand_heap_comp = heap_sort(Arr_2000_Rand_heap)
end_time_rand = time.time_ns()


data_h2 = [{'Algorithm': 'HeapSort_Sorted_2000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_2000_Sorted_heap_comp},
        
        {'Algorithm': 'HeapSort_Reverse_2000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_2000_Reverse_heap_comp},
        
        {'Algorithm': 'HeapSort_Rand_2000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_2000_Rand_heap_comp}]

df_new_h2 = pd.concat([pd.DataFrame([d]) for d in data_h2], ignore_index=True)
df = pd.concat([df, df_new_h2], ignore_index=True)

# Arr of size 4000
start_time_sorted = time.time_ns()
Arr_4000_Sorted_heap_comp = heap_sort(Arr_4000_Sorted_heap)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_4000_Reverse_heap_comp = heap_sort(Arr_4000_Reverse_heap)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_4000_Rand_heap_comp = heap_sort(Arr_4000_Rand_heap)
end_time_rand = time.time_ns()


data3 = [{'Algorithm': 'HeapSort_Sorted_4000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_4000_Sorted_heap_comp},
        
        {'Algorithm': 'HeapSort_Reverse_4000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_4000_Reverse_heap_comp},
        
        {'Algorithm': 'HeapSort_Rand_4000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_4000_Rand_heap_comp}]

df_new_3 = pd.concat([pd.DataFrame([d]) for d in data3], ignore_index=True)
df = pd.concat([df, df_new_3], ignore_index=True)

# Arr of size 8000
start_time_sorted = time.time_ns()
Arr_8000_Sorted_heap_comp = heap_sort(Arr_8000_Sorted_heap)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_8000_Reverse_heap_comp = heap_sort(Arr_8000_Reverse_heap)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_8000_Rand_heap_comp = heap_sort(Arr_8000_Rand_heap)
end_time_rand = time.time_ns()


data4 = [{'Algorithm': 'HeapSort_Sorted_8000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_8000_Sorted_heap_comp},
        
        {'Algorithm': 'HeapSort_Reverse_8000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_8000_Reverse_heap_comp},
        
        {'Algorithm': 'HeapSort_Rand_8000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_8000_Rand_heap_comp}]

df_new_4 = pd.concat([pd.DataFrame([d]) for d in data4], ignore_index=True)
df = pd.concat([df, df_new_4], ignore_index=True)

# Call to the merge-3-way sort function with all 12 copies of the 12 original arrays and insert the results in a dataframe table
# Arr of size 1000
start_time_sorted = time.time_ns()
Arr_1000_Sorted_merge_comp = merge_sort(Arr_1000_Sorted_merge)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_1000_Reverse_merge_comp = merge_sort(Arr_1000_Reverse_merge)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_1000_Rand_merge_comp = merge_sort(Arr_1000_Rand_merge)
end_time_rand = time.time_ns()


data_1m = [{'Algorithm': 'Merge Sort_Sorted_1000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_1000_Sorted_merge_comp},
        
        {'Algorithm': 'Merge Sort_Reverse_1000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_1000_Reverse_merge_comp},
        
        {'Algorithm': 'Merge Sort_Rand_1000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_1000_Rand_merge_comp}]

df_new_1m = pd.concat([pd.DataFrame([d]) for d in data_1m], ignore_index=True)
df = pd.concat([df, df_new_1m], ignore_index=True)

# Arr of size 2000
start_time_sorted = time.time_ns()
Arr_2000_Sorted_merge_comp = merge_sort(Arr_2000_Sorted_merge)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_2000_Reverse_merge_comp = merge_sort(Arr_2000_Reverse_merge)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_2000_Rand_merge_comp = merge_sort(Arr_2000_Rand_merge)
end_time_rand = time.time_ns()


data_2m = [{'Algorithm': 'Merge Sort_Sorted_2000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_2000_Sorted_merge_comp},
        
        {'Algorithm': 'Merge Sort_Reverse_2000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_2000_Reverse_merge_comp},
        
        {'Algorithm': 'Merge Sort_Rand_2000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_2000_Rand_merge_comp}]

df_new_2m = pd.concat([pd.DataFrame([d]) for d in data_2m], ignore_index=True)
df = pd.concat([df, df_new_2m], ignore_index=True)

# Arr of size 4000
start_time_sorted = time.time_ns()
Arr_4000_Sorted_merge_comp = merge_sort(Arr_4000_Sorted_merge)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_4000_Reverse_merge_comp = merge_sort(Arr_4000_Reverse_merge)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_4000_Rand_merge_comp = merge_sort(Arr_4000_Rand_merge)
end_time_rand = time.time_ns()


data_3m = [{'Algorithm': 'Merge Sort_Sorted_4000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_4000_Sorted_merge_comp},
        
        {'Algorithm': 'Merge Sort_Reverse_4000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_4000_Reverse_merge_comp},
        
        {'Algorithm': 'Merge Sort_Rand_4000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_4000_Rand_merge_comp}]

df_new_3m = pd.concat([pd.DataFrame([d]) for d in data_3m], ignore_index=True)
df = pd.concat([df, df_new_3m], ignore_index=True)

# Arr of size 8000
start_time_sorted = time.time_ns()
Arr_8000_Sorted_merge_comp = merge_sort(Arr_8000_Sorted_merge)
end_time_sorted = time.time_ns()
start_time_rev = time.time_ns()
Arr_8000_Reverse_merge_comp = merge_sort(Arr_8000_Reverse_merge)
end_time_rev = time.time_ns()
start_time_rand = time.time_ns()
Arr_8000_Rand_merge_comp = merge_sort(Arr_8000_Rand_merge)
end_time_rand = time.time_ns()


data_4m = [{'Algorithm': 'Merge Sort_Sorted_8000', 
         'Timer': end_time_sorted - start_time_sorted, 
         'Num of Comparisons': Arr_8000_Sorted_merge_comp},
        
        {'Algorithm': 'Merge Sort_Reverse_8000', 
         'Timer': end_time_rev - start_time_rev, 
         'Num of Comparisons': Arr_8000_Reverse_merge_comp},
        
        {'Algorithm': 'Merge Sort_Rand_8000', 
         'Timer': end_time_rand - start_time_rand, 
         'Num of Comparisons': Arr_8000_Rand_merge_comp}]

df_new_4m = pd.concat([pd.DataFrame([d]) for d in data_4m], ignore_index=True)
df = pd.concat([df, df_new_4m], ignore_index=True)




print(df)
