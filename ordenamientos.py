import random
from typing import List, Tuple, Union
import logging

# Configurar logging
logger = logging.getLogger(__name__)


def bubble_sort_step(arr: List[int], i: int, j: int) -> Tuple[bool, int, int]:
    """
    Ejecuta un paso del algoritmo Bubble Sort.
    
    Bubble Sort compara elementos adyacentes e intercambia si están en orden incorrecto.
    Complejidad temporal: O(n²)
    Complejidad espacial: O(1)
    
    Args:
        arr (List[int]): Array a ordenar (se modifica in-place)
        i (int): Índice de la pasada actual
        j (int): Índice de comparación actual
        
    Returns:
        Tuple[bool, int, int]: (completo, nuevo_i, nuevo_j)
    """
    n = len(arr)
    
    if i < n - 1:
        if j < n - i - 1:
            # Comparar e intercambiar elementos adyacentes si es necesario
            if arr[j] > arr[j + 1]:  # Cambio: ordenamiento ascendente
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            return False, i, j + 1  # Continúa con la siguiente comparación
        else:
            return False, i + 1, 0  # Nueva pasada desde el inicio
    
    logger.debug(f"Bubble Sort completado en {i} pasadas")
    return True, i, j  # Algoritmo completado


def insertion_sort_step(arr: List[int], i: int) -> Tuple[bool, int]:
    """
    Ejecuta un paso del algoritmo Insertion Sort.
    
    Insertion Sort construye la lista ordenada elemento por elemento,
    insertando cada nuevo elemento en su posición correcta.
    Complejidad temporal: O(n²) peor caso, O(n) mejor caso
    Complejidad espacial: O(1)
    
    Args:
        arr (List[int]): Array a ordenar (se modifica in-place)
        i (int): Índice del elemento actual a insertar
        
    Returns:
        Tuple[bool, int]: (completo, nuevo_i)
    """
    if i < len(arr):
        key = arr[i]
        j = i - 1
        
        # Mover elementos mayores que key una posición hacia adelante
        while j >= 0 and key < arr[j]:  # Cambio: ordenamiento ascendente
            arr[j + 1] = arr[j]
            j -= 1
            
        arr[j + 1] = key
        return False, i + 1
    
    logger.debug(f"Insertion Sort completado procesando {i} elementos")
    return True, i


def selection_sort_step(arr: List[int], i: int) -> Tuple[bool, int]:
    """
    Ejecuta un paso del algoritmo Selection Sort.
    
    Selection Sort encuentra el elemento mínimo/máximo en la porción no ordenada
    y lo coloca en la posición correcta.
    Complejidad temporal: O(n²)
    Complejidad espacial: O(1)
    
    Args:
        arr (List[int]): Array a ordenar (se modifica in-place)
        i (int): Índice de la posición a llenar
        
    Returns:
        Tuple[bool, int]: (completo, nuevo_i)
    """
    n = len(arr)
    
    if i < n - 1:
        # Encontrar el índice del elemento mínimo en la porción no ordenada
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:  # Cambio: ordenamiento ascendente
                min_idx = j
                
        # Intercambiar el elemento mínimo con el elemento en la posición i
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            
        return False, i + 1
    
    logger.debug(f"Selection Sort completado en {i} intercambios")
    return True, i


def quick_sort_step(arr: List[int], stack: List[Tuple[int, int]]) -> Tuple[bool, List[Tuple[int, int]], List[int]]:
    """
    Ejecuta un paso del algoritmo Quick Sort iterativo.
    
    Quick Sort es un algoritmo divide y vencerás que selecciona un pivote
    y particiona el array alrededor de él.
    Complejidad temporal: O(n log n) promedio, O(n²) peor caso
    Complejidad espacial: O(log n)
    
    Args:
        arr (List[int]): Array a ordenar (se modifica in-place)
        stack (List[Tuple[int, int]]): Pila de sub-arrays pendientes
        
    Returns:
        Tuple[bool, List[Tuple[int, int]], List[int]]: 
        (completo, nueva_stack, indices_modificados)
    """
    if not stack:
        logger.debug("Quick Sort completado - stack vacía")
        return True, stack, []

    low, high = stack[-1]
    indices_modificados = []

    if low < high:
        # Particionar el array y obtener el índice del pivote
        pivot_index = partition(arr, low, high)
        stack.pop()
        
        # Añadir sub-arrays a la pila si tienen más de un elemento
        if low < pivot_index - 1:
            stack.append((low, pivot_index - 1))
        if pivot_index + 1 < high:
            stack.append((pivot_index + 1, high))
            
        indices_modificados = [pivot_index]
    else:
        stack.pop()

    return len(stack) == 0, stack, indices_modificados


def partition(arr: List[int], low: int, high: int) -> int:
    """
    Función auxiliar para particionar el array en Quick Sort.
    
    Utiliza el último elemento como pivote y reorganiza el array
    de modo que elementos menores estén a la izquierda y mayores a la derecha.
    
    Args:
        arr (List[int]): Array a particionar
        low (int): Índice inferior del rango
        high (int): Índice superior del rango
        
    Returns:
        int: Índice final del pivote
    """
    pivot = arr[high]  # Usar último elemento como pivote
    i = low - 1  # Índice del elemento menor

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Colocar el pivote en su posición correcta
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def bogosort_step(arr: List[int]) -> Tuple[bool, List[int]]:
    """
    Ejecuta un paso del algoritmo Bogosort (algoritmo joke).
    
    Bogosort baraja aleatoriamente el array hasta que esté ordenado.
    Complejidad temporal: O(n!) promedio - EXTREMADAMENTE INEFICIENTE
    Complejidad espacial: O(1)
    
    ADVERTENCIA: Solo para fines educativos. No usar en producción.
    
    Args:
        arr (List[int]): Array a "ordenar"
        
    Returns:
        Tuple[bool, List[int]]: (completo, array_modificado)
    """
    if is_sorted(arr):
        logger.debug(f"Bogosort completado después de una verificación")
        return True, arr
    
    # Barajar aleatoriamente y esperar lo mejor
    random.shuffle(arr)
    return False, arr


def is_sorted(arr: List[int], ascending: bool = True) -> bool:
    """
    Verifica si un array está ordenado.
    
    Args:
        arr (List[int]): Array a verificar
        ascending (bool): True para orden ascendente, False para descendente
        
    Returns:
        bool: True si está ordenado, False en caso contrario
    """
    if len(arr) <= 1:
        return True
    
    if ascending:
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    else:
        return all(arr[i] >= arr[i + 1] for i in range(len(arr) - 1))


def get_algorithm_info(algorithm_name: str) -> dict:
    """
    Obtiene información detallada sobre un algoritmo de ordenamiento.
    
    Args:
        algorithm_name (str): Nombre del algoritmo
        
    Returns:
        dict: Información del algoritmo incluyendo complejidades y características
    """
    algorithms_info = {
        "Bubble Sort": {
            "description": "Compara elementos adyacentes y los intercambia si están desordenados",
            "time_complexity": {
                "best": "O(n)",
                "average": "O(n²)",
                "worst": "O(n²)"
            },
            "space_complexity": "O(1)",
            "stable": True,
            "in_place": True,
            "adaptive": True,
            "use_cases": "Educativo, arrays muy pequeños",
            "carbon_efficiency": "Baja - O(n²) operaciones"
        },
        
        "Insertion Sort": {
            "description": "Construye la lista ordenada elemento por elemento",
            "time_complexity": {
                "best": "O(n)",
                "average": "O(n²)",
                "worst": "O(n²)"
            },
            "space_complexity": "O(1)",
            "stable": True,
            "in_place": True,
            "adaptive": True,
            "use_cases": "Arrays pequeños, datos parcialmente ordenados",
            "carbon_efficiency": "Media - Eficiente para datos pequeños"
        },
        
        "Selection Sort": {
            "description": "Selecciona repetidamente el elemento mínimo/máximo",
            "time_complexity": {
                "best": "O(n²)",
                "average": "O(n²)",
                "worst": "O(n²)"
            },
            "space_complexity": "O(1)",
            "stable": False,
            "in_place": True,
            "adaptive": False,
            "use_cases": "Cuando el espacio de memoria es limitado",
            "carbon_efficiency": "Baja - Siempre O(n²) operaciones"
        },
        
        "Quick Sort": {
            "description": "Divide y vencerás usando particionado con pivote",
            "time_complexity": {
                "best": "O(n log n)",
                "average": "O(n log n)",
                "worst": "O(n²)"
            },
            "space_complexity": "O(log n)",
            "stable": False,
            "in_place": True,
            "adaptive": False,
            "use_cases": "Uso general, arrays grandes",
            "carbon_efficiency": "Alta - Excelente para la mayoría de casos"
        },
        
        "Bogosort": {
            "description": "Baraja aleatoriamente hasta que esté ordenado",
            "time_complexity": {
                "best": "O(n)",
                "average": "O(n!)",
                "worst": "O(∞)"
            },
            "space_complexity": "O(1)",
            "stable": False,
            "in_place": True,
            "adaptive": False,
            "use_cases": "Solo educativo/experimental",
            "carbon_efficiency": "EXTREMADAMENTE BAJA - Evitar siempre"
        }
    }
    
    return algorithms_info.get(algorithm_name, {
        "description": "Algoritmo no reconocido",
        "carbon_efficiency": "Desconocida"
    })


def estimate_carbon_impact(algorithm_name: str, data_size: int) -> dict:
    """
    Estima el impacto de carbono relativo de un algoritmo.
    
    Args:
        algorithm_name (str): Nombre del algoritmo
        data_size (int): Tamaño del conjunto de datos
        
    Returns:
        dict: Estimación de impacto incluyendo operaciones esperadas
    """
    try:
        n = data_size
        
        operations_estimate = {
            "Bubble Sort": n * n // 2,  # O(n²)
            "Insertion Sort": n * n // 4,  # O(n²) pero más eficiente
            "Selection Sort": n * n // 2,  # O(n²)
            "Quick Sort": n * (n.bit_length() - 1) if n > 0 else 0,  # O(n log n) aproximado
            "Bogosort": n * 3628800 if n <= 10 else float('inf')  # O(n!) - solo para n pequeño
        }
        
        ops = operations_estimate.get(algorithm_name, n * n)
        
        # Clasificar impacto
        if ops == float('inf'):
            impact_level = "CRÍTICO"
            efficiency_score = 0
        elif ops > n * n:
            impact_level = "ALTO"
            efficiency_score = max(1, 10 - (ops // (n * n)))
        elif ops > n * (n.bit_length() if n > 0 else 1):
            impact_level = "MEDIO"
            efficiency_score = 6
        else:
            impact_level = "BAJO"
            efficiency_score = 9
            
        return {
            "estimated_operations": ops,
            "carbon_impact_level": impact_level,
            "efficiency_score": efficiency_score,  # 0-10 escala
            "recommendation": "USAR" if efficiency_score >= 7 else "EVITAR" if efficiency_score <= 3 else "CONSIDERAR"
        }
        
    except Exception as e:
        logger.error(f"Error estimando impacto de carbono: {e}")
        return {
            "estimated_operations": 0,
            "carbon_impact_level": "DESCONOCIDO",
            "efficiency_score": 5,
            "recommendation": "REVISAR"
        }
