from codecarbon import EmissionsTracker
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calcular_horas_para_compensar(emisiones_totales_kg: float, absorcion_arbol_kg_por_ano: float = 30.0) -> float:
    """
    Calcula las horas necesarias para que un árbol compense las emisiones de CO2.
    
    Args:
        emisiones_totales_kg (float): Emisiones totales de CO2 en kilogramos
        absorcion_arbol_kg_por_ano (float): Absorción del árbol en kg de CO2 por año
                                           Por defecto 30 kg/año (árbol joven estándar)
    
    Returns:
        float: Horas de absorción necesarias para compensar las emisiones
        
    Note:
        Valores de referencia de absorción de CO2 por árbol:
        - Árbol joven (1-10 años): 10-30 kg/año
        - Árbol maduro (>20 años): 30-50 kg/año
        - Árbol grande (>50 años): 50-100 kg/año
    """
    try:
        if emisiones_totales_kg < 0:
            raise ValueError("Las emisiones no pueden ser negativas")
        if absorcion_arbol_kg_por_ano <= 0:
            raise ValueError("La absorción del árbol debe ser positiva")
            
        horas_de_absorcion = (emisiones_totales_kg / absorcion_arbol_kg_por_ano) * 365 * 24
        
        logger.info(f"Calculando compensación: {emisiones_totales_kg:.6f} kg CO2 "
                   f"con absorción de {absorcion_arbol_kg_por_ano} kg/año")
        
        return horas_de_absorcion
        
    except Exception as e:
        logger.error(f"Error en cálculo de compensación: {e}")
        raise


def calcular_equivalencias_cotidianas(emisiones_totales_kg: float) -> dict:
    """
    Calcula equivalencias cotidianas para contextualizar las emisiones de CO2.
    
    Args:
        emisiones_totales_kg (float): Emisiones totales de CO2 en kilogramos
        
    Returns:
        dict: Diccionario con equivalencias en actividades cotidianas
    """
    try:
        equivalencias = {
            # Transporte (kg CO2 por km)
            'km_coche_pequeño': emisiones_totales_kg / 0.12,  # Auto compacto
            'km_coche_promedio': emisiones_totales_kg / 0.18,  # Auto promedio
            'km_autobus': emisiones_totales_kg / 0.08,  # Autobús público
            'km_vuelo_domestico': emisiones_totales_kg / 0.25,  # Vuelo doméstico
            
            # Energía doméstica (kg CO2)
            'horas_tv': emisiones_totales_kg / 0.024,  # TV LED 40"
            'horas_computadora': emisiones_totales_kg / 0.05,  # Computadora de escritorio
            'horas_bombilla_led': emisiones_totales_kg / 0.008,  # Bombilla LED 10W
            'duchas_calientes': emisiones_totales_kg / 0.5,  # Ducha de 10 min
            
            # Alimentación (kg CO2)
            'hamburguesas': emisiones_totales_kg / 2.5,  # Hamburguesa de carne
            'litros_leche': emisiones_totales_kg / 1.0,  # Litro de leche
            'kg_arroz': emisiones_totales_kg / 2.3,  # Kilogramo de arroz
            
            # Naturaleza
            'arboles_compensadores': emisiones_totales_kg / 30,  # Árboles necesarios por año
            'metros_hielo_derretido': emisiones_totales_kg * 3.3,  # Estimación del derretimiento
        }
        
        return equivalencias
        
    except Exception as e:
        logger.error(f"Error calculando equivalencias: {e}")
        return {}


def calcular_costo_ambiental(emisiones_totales_kg: float, precio_carbono_usd: float = 50.0) -> dict:
    """
    Calcula el costo ambiental estimado de las emisiones.
    
    Args:
        emisiones_totales_kg (float): Emisiones totales de CO2 en kilogramos
        precio_carbono_usd (float): Precio del carbono en USD por tonelada
        
    Returns:
        dict: Costos ambientales en diferentes monedas y contextos
    """
    try:
        emisiones_toneladas = emisiones_totales_kg / 1000.0
        costo_usd = emisiones_toneladas * precio_carbono_usd
        
        costos = {
            'costo_usd': costo_usd,
            'costo_eur': costo_usd * 0.85,  # Conversión aproximada
            'costo_social_usd': emisiones_toneladas * 185,  # Costo social del carbono (EPA)
            'offset_credits': emisiones_toneladas,  # Créditos de carbono necesarios
        }
        
        return costos
        
    except Exception as e:
        logger.error(f"Error calculando costo ambiental: {e}")
        return {}


def iniciar_rastreador(output_dir: str = "./", project_name: str = "green-software-analysis") -> EmissionsTracker:
    """
    Inicia el rastreador de emisiones de CodeCarbon con configuración optimizada.
    
    Args:
        output_dir (str): Directorio donde guardar los resultados
        project_name (str): Nombre del proyecto para identificar el análisis
        
    Returns:
        EmissionsTracker: Instancia del rastreador iniciada
    """
    try:
        tracker = EmissionsTracker(
            output_dir=output_dir,
            project_name=project_name,
            measure_power_secs=1,  # Medir cada segundo para mayor precisión
            tracking_mode="process",  # Solo rastrear este proceso
            log_level="WARNING"  # Reducir logs de CodeCarbon
        )
        
        tracker.start()
        logger.info(f"Rastreador iniciado para proyecto: {project_name}")
        
        return tracker
        
    except Exception as e:
        logger.error(f"Error iniciando rastreador: {e}")
        raise


def detener_rastreador(tracker: EmissionsTracker) -> float:
    """
    Detiene el rastreador de emisiones y retorna las emisiones totales.
    
    Args:
        tracker (EmissionsTracker): Instancia del rastreador activo
        
    Returns:
        float: Emisiones totales de CO2 en kilogramos
    """
    try:
        if tracker is None:
            raise ValueError("El rastreador no puede ser None")
            
        emisiones_totales_kg = tracker.stop()
        
        if emisiones_totales_kg is None:
            emisiones_totales_kg = 0.0
            logger.warning("El rastreador devolvió None, usando valor 0.0")
            
        logger.info(f"Rastreador detenido. Emisiones: {emisiones_totales_kg:.6f} kg CO2")
        
        return emisiones_totales_kg
        
    except Exception as e:
        logger.error(f"Error deteniendo rastreador: {e}")
        return 0.0


def generar_reporte_completo(emisiones_kg: float, algoritmo: str, datos_count: int, 
                           tiempo_ejecucion: float, absorcion_arbol: float = 30.0) -> dict:
    """
    Genera un reporte completo del análisis de emisiones.
    
    Args:
        emisiones_kg (float): Emisiones de CO2 en kilogramos
        algoritmo (str): Nombre del algoritmo analizado
        datos_count (int): Cantidad de datos procesados
        tiempo_ejecucion (float): Tiempo de ejecución en segundos
        absorcion_arbol (float): Absorción del árbol en kg/año
        
    Returns:
        dict: Reporte completo con métricas y análisis
    """
    try:
        reporte = {
            'analisis_basico': {
                'algoritmo': algoritmo,
                'datos_procesados': datos_count,
                'tiempo_ejecucion_segundos': tiempo_ejecucion,
                'emisiones_kg_co2': emisiones_kg,
                'intensidad_carbono_kg_por_dato': emisiones_kg / datos_count if datos_count > 0 else 0,
                'eficiencia_carbono_kg_por_segundo': emisiones_kg / tiempo_ejecucion if tiempo_ejecucion > 0 else 0
            },
            'compensacion_ambiental': {
                'horas_absorcion_arbol': calcular_horas_para_compensar(emisiones_kg, absorcion_arbol),
                'dias_absorcion_arbol': calcular_horas_para_compensar(emisiones_kg, absorcion_arbol) / 24,
                'arboles_necesarios_un_año': emisiones_kg / absorcion_arbol
            },
            'equivalencias_cotidianas': calcular_equivalencias_cotidianas(emisiones_kg),
            'impacto_economico': calcular_costo_ambiental(emisiones_kg),
            'recomendaciones': generar_recomendaciones(algoritmo, emisiones_kg, datos_count)
        }
        
        return reporte
        
    except Exception as e:
        logger.error(f"Error generando reporte: {e}")
        return {}


def generar_recomendaciones(algoritmo: str, emisiones_kg: float, datos_count: int) -> list:
    """
    Genera recomendaciones basadas en el análisis.
    
    Args:
        algoritmo (str): Algoritmo analizado
        emisiones_kg (float): Emisiones generadas
        datos_count (int): Cantidad de datos
        
    Returns:
        list: Lista de recomendaciones
    """
    recomendaciones = []
    
    try:
        # Recomendaciones por algoritmo
        if algoritmo == "Bogosort":
            recomendaciones.append("⚠️ Bogosort es extremadamente ineficiente. Use solo para fines educativos.")
            recomendaciones.append("💡 Para datos grandes, prefiera Quick Sort o Merge Sort.")
            
        elif algoritmo in ["Bubble Sort", "Selection Sort", "Insertion Sort"]:
            if datos_count > 100:
                recomendaciones.append("⚡ Para conjuntos de datos grandes, considere algoritmos O(n log n) como Quick Sort.")
            recomendaciones.append("✅ Este algoritmo es educativo pero ineficiente para producción.")
            
        elif algoritmo == "Quick Sort":
            recomendaciones.append("✅ Excelente elección para la mayoría de casos de uso.")
            
        # Recomendaciones por intensidad de emisiones
        intensidad = emisiones_kg / datos_count if datos_count > 0 else 0
        
        if intensidad > 0.001:  # Alta intensidad de carbono
            recomendaciones.append("🌱 Considere optimizar su código para reducir el impacto ambiental.")
            recomendaciones.append("💚 Use algoritmos más eficientes para conjuntos de datos grandes.")
            
        # Recomendaciones generales
        recomendaciones.append("🌿 Considere ejecutar análisis intensivos durante horas de baja demanda energética.")
        recomendaciones.append("♻️ Implemente caché y memoización para evitar recálculos innecesarios.")
        
        if datos_count > 1000:
            recomendaciones.append("📊 Para análisis frecuentes, considere implementar procesamiento por lotes.")
            
        return recomendaciones
        
    except Exception as e:
        logger.error(f"Error generando recomendaciones: {e}")
        return ["Error generando recomendaciones"]
