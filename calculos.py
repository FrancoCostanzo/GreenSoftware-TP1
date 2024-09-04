from codecarbon import EmissionsTracker


def calcular_horas_para_compensar(emisiones_totales_kg, absorcion_arbol_kg_por_ano = 30): # 30 kg por año, siendo un arbol bebe
    horas_de_procesamiento = emisiones_totales_kg * 365 / absorcion_arbol_kg_por_ano
    return horas_de_procesamiento
# Hay que revisar esot, no se si esta bien

def iniciar_rastreador():
    tracker = EmissionsTracker()
    tracker.start()
    return tracker


def detener_rastreador(tracker):
    emisiones_totales_kg = tracker.stop()
    return emisiones_totales_kg
