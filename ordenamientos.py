def bubble_sort_step(arr, i, j):
    n = len(arr)
    if i < n - 1:
        if j < n - i - 1:
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            return False, i, j + 1  # Continúa con la siguiente comparación en la misma vuelta
        else:
            return False, i + 1, 0  # Comienza una nueva vuelta desde el inicio
    return True, i, j  # Finaliza cuando se han completado todas las vueltas


def insertion_sort_step(arr, i):
    if i < len(arr):
        key = arr[i]
        j = i - 1
        while j >= 0 and key > arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        return False, i + 1
    return True, i


def selection_sort_step(arr, i):
    n = len(arr)
    if i < n - 1:
        max_idx = i
        for j in range(i + 1, n):
            if arr[j] > arr[max_idx]:
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
        return False, i + 1
    return True, i


def quick_sort_step(arr, stack):
    if not stack:
        return True, stack, []  # Devolver una lista vacía como `current_indices`

    low, high = stack[-1]
    indices = []

    if low < high:
        pivot_index = partition(arr, low, high)
        stack.pop()
        stack.append((low, pivot_index - 1))
        stack.append((pivot_index + 1, high))
        indices = [pivot_index]  # Índice que se está comparando
    else:
        stack.pop()

    return False, stack, indices


def partition(arr, low, high):
    pivot = arr[high]  # Selecciona el último elemento como pivote
    i = low - 1  # Índice del elemento más pequeño

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Intercambia los elementos

    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # Coloca el pivote en la posición correcta
    return i + 1  # Devuelve el índice del pivote

import random

def is_sorted(arr):
    #Verifica si la lista está ordenada.
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def bogosort_step(arr):
    #por los jajas
    if is_sorted(arr):
        return True, arr
    random.shuffle(arr)
    return False, arr
