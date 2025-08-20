"""
Utilidades adicionales para la aplicación Green Software.
Contiene funciones de ayuda, validaciones y herramientas de análisis.
"""

import os
import json
import csv
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataValidator:
    """Clase para validar datos de entrada de la aplicación."""
    
    @staticmethod
    def validate_data_count(value: str) -> tuple[bool, str]:
        """
        Valida la cantidad de datos.
        
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        try:
            count = int(value)
            if count < 10:
                return False, "La cantidad mínima es 10"
            if count > 10000:
                return False, "La cantidad máxima es 10,000 para evitar problemas de rendimiento"
            return True, ""
        except ValueError:
            return False, "Debe ser un número entero válido"
    
    @staticmethod
    def validate_tree_absorption(value: str) -> tuple[bool, str]:
        """
        Valida el valor de absorción del árbol.
        
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        try:
            absorption = float(value)
            if absorption <= 0:
                return False, "La absorción debe ser mayor a 0"
            if absorption > 200:
                return False, "Valor muy alto. Un árbol típico absorbe entre 10-100 kg CO2/año"
            return True, ""
        except ValueError:
            return False, "Debe ser un número decimal válido"


class ConfigManager:
    """Administrador de configuración de la aplicación."""
    
    DEFAULT_CONFIG = {
        'data_count': 50,
        'algorithm': 'Quick Sort',
        'tree_absorption': 30.0,
        'visualization_speed': 50,
        'theme': 'default',
        'auto_save_results': True,
        'show_detailed_stats': False
    }
    
    def __init__(self, config_file: str = 'green_software_config.json'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde archivo o usa valores por defecto."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Fusionar con valores por defecto para claves faltantes
                    return {**self.DEFAULT_CONFIG, **config}
            return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> bool:
        """Guarda la configuración actual al archivo."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Obtiene un valor de configuración."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Establece un valor de configuración."""
        self.config[key] = value
    
    def reset_to_defaults(self):
        """Restablece la configuración a valores por defecto."""
        self.config = self.DEFAULT_CONFIG.copy()


class ResultsExporter:
    """Exportador de resultados en diferentes formatos."""
    
    @staticmethod
    def export_to_csv(results: List[Dict], filename: str) -> bool:
        """
        Exporta resultados a formato CSV.
        
        Args:
            results: Lista de diccionarios con resultados
            filename: Nombre del archivo de salida
            
        Returns:
            bool: True si la exportación fue exitosa
        """
        try:
            if not results:
                return False
                
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = results[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for result in results:
                    writer.writerow(result)
                    
            logger.info(f"Resultados exportados a {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error exportando a CSV: {e}")
            return False
    
    @staticmethod
    def export_to_json(results: List[Dict], filename: str, pretty: bool = True) -> bool:
        """
        Exporta resultados a formato JSON.
        
        Args:
            results: Lista de diccionarios con resultados
            filename: Nombre del archivo de salida
            pretty: Si usar formato legible
            
        Returns:
            bool: True si la exportación fue exitosa
        """
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                if pretty:
                    json.dump(results, jsonfile, indent=2, ensure_ascii=False, default=str)
                else:
                    json.dump(results, jsonfile, ensure_ascii=False, default=str)
                    
            logger.info(f"Resultados exportados a {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error exportando a JSON: {e}")
            return False
    
    @staticmethod
    def generate_report_html(results: List[Dict], filename: str) -> bool:
        """
        Genera un reporte HTML con los resultados.
        
        Args:
            results: Lista de diccionarios con resultados
            filename: Nombre del archivo HTML de salida
            
        Returns:
            bool: True si la generación fue exitosa
        """
        try:
            html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Emisiones CO2 - Green Software</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #27ae60, #2ecc71);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #34495e;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .summary-card {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #3498db;
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
        }}
        .summary-card .value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #27ae60;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            text-align: center;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌱 Reporte de Emisiones CO2</h1>
        <p>Análisis de Impacto Ambiental de Algoritmos de Ordenamiento</p>
    </div>
    
    <div class="container">
        <div class="summary">
            <div class="summary-card">
                <h3>Total de Análisis</h3>
                <div class="value">{len(results)}</div>
            </div>
            <div class="summary-card">
                <h3>Emisiones Totales</h3>
                <div class="value">{sum(float(r.get('emisiones', 0)) for r in results):.6f} kg CO2</div>
            </div>
            <div class="summary-card">
                <h3>Tiempo Total Compensación</h3>
                <div class="value">{sum(float(r.get('horas_compensacion', 0)) for r in results):.2f} horas</div>
            </div>
        </div>
        
        <h2>📊 Detalle de Análisis</h2>
        <table>
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Algoritmo</th>
                    <th>Datos</th>
                    <th>Emisiones (kg CO2)</th>
                    <th>Compensación (horas)</th>
                    <th>Tiempo Ejecución (s)</th>
                </tr>
            </thead>
            <tbody>
"""
            
            for result in results:
                html_content += f"""
                <tr>
                    <td>{result.get('fecha', 'N/A')}</td>
                    <td>{result.get('algoritmo', 'N/A')}</td>
                    <td>{result.get('datos', 'N/A')}</td>
                    <td>{float(result.get('emisiones', 0)):.6f}</td>
                    <td>{float(result.get('horas_compensacion', 0)):.2f}</td>
                    <td>{float(result.get('tiempo_ejecucion', 0)):.2f}</td>
                </tr>
"""
            
            html_content += f"""
            </tbody>
        </table>
        
        <div class="timestamp">
            <p>Reporte generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Aplicación Green Software - Calculadora de Emisiones CO2</p>
        </div>
    </div>
</body>
</html>
"""
            
            with open(filename, 'w', encoding='utf-8') as htmlfile:
                htmlfile.write(html_content)
                
            logger.info(f"Reporte HTML generado: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error generando reporte HTML: {e}")
            return False


class PerformanceMonitor:
    """Monitor de rendimiento para la aplicación."""
    
    def __init__(self):
        self.metrics = {
            'execution_times': [],
            'memory_usage': [],
            'cpu_usage': [],
            'algorithm_performance': {}
        }
    
    def record_execution(self, algorithm: str, data_size: int, 
                        execution_time: float, emissions: float):
        """Registra una ejecución para análisis posterior."""
        self.metrics['execution_times'].append({
            'timestamp': datetime.now(),
            'algorithm': algorithm,
            'data_size': data_size,
            'execution_time': execution_time,
            'emissions': emissions,
            'efficiency': emissions / execution_time if execution_time > 0 else 0
        })
        
        # Actualizar métricas por algoritmo
        if algorithm not in self.metrics['algorithm_performance']:
            self.metrics['algorithm_performance'][algorithm] = {
                'total_runs': 0,
                'total_time': 0,
                'total_emissions': 0,
                'avg_efficiency': 0
            }
        
        perf = self.metrics['algorithm_performance'][algorithm]
        perf['total_runs'] += 1
        perf['total_time'] += execution_time
        perf['total_emissions'] += emissions
        perf['avg_efficiency'] = perf['total_emissions'] / perf['total_time']
    
    def get_algorithm_ranking(self) -> List[Dict]:
        """Obtiene un ranking de algoritmos por eficiencia ambiental."""
        rankings = []
        
        for algo, perf in self.metrics['algorithm_performance'].items():
            if perf['total_runs'] > 0:
                rankings.append({
                    'algorithm': algo,
                    'runs': perf['total_runs'],
                    'avg_time': perf['total_time'] / perf['total_runs'],
                    'avg_emissions': perf['total_emissions'] / perf['total_runs'],
                    'efficiency_score': 1 / perf['avg_efficiency'] if perf['avg_efficiency'] > 0 else 0
                })
        
        # Ordenar por score de eficiencia (mayor es mejor)
        return sorted(rankings, key=lambda x: x['efficiency_score'], reverse=True)
    
    def generate_performance_chart(self, filename: str) -> bool:
        """Genera un gráfico de rendimiento."""
        try:
            if not self.metrics['execution_times']:
                return False
            
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # Gráfico 1: Tiempo de ejecución vs tamaño de datos
            times_data = self.metrics['execution_times']
            sizes = [d['data_size'] for d in times_data]
            times = [d['execution_time'] for d in times_data]
            
            ax1.scatter(sizes, times, alpha=0.6, c='blue')
            ax1.set_xlabel('Tamaño de Datos')
            ax1.set_ylabel('Tiempo de Ejecución (s)')
            ax1.set_title('Tiempo de Ejecución vs Tamaño de Datos')
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Emisiones vs tiempo de ejecución
            emissions = [d['emissions'] for d in times_data]
            
            ax2.scatter(times, emissions, alpha=0.6, c='red')
            ax2.set_xlabel('Tiempo de Ejecución (s)')
            ax2.set_ylabel('Emisiones CO2 (kg)')
            ax2.set_title('Emisiones vs Tiempo de Ejecución')
            ax2.grid(True, alpha=0.3)
            
            # Gráfico 3: Eficiencia por algoritmo
            ranking = self.get_algorithm_ranking()
            if ranking:
                algorithms = [r['algorithm'] for r in ranking]
                scores = [r['efficiency_score'] for r in ranking]
                
                bars = ax3.bar(range(len(algorithms)), scores, color=['#27ae60', '#3498db', '#e74c3c', '#f39c12', '#9b59b6'])
                ax3.set_xlabel('Algoritmos')
                ax3.set_ylabel('Score de Eficiencia')
                ax3.set_title('Eficiencia Ambiental por Algoritmo')
                ax3.set_xticks(range(len(algorithms)))
                ax3.set_xticklabels(algorithms, rotation=45)
                ax3.grid(True, alpha=0.3, axis='y')
                
                # Añadir valores en las barras
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax3.text(bar.get_x() + bar.get_width()/2., height,
                            f'{scores[i]:.2f}', ha='center', va='bottom')
            
            # Gráfico 4: Histograma de emisiones
            ax4.hist(emissions, bins=20, alpha=0.7, color='green', edgecolor='black')
            ax4.set_xlabel('Emisiones CO2 (kg)')
            ax4.set_ylabel('Frecuencia')
            ax4.set_title('Distribución de Emisiones')
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Gráfico de rendimiento guardado: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error generando gráfico de rendimiento: {e}")
            return False


def format_file_size(size_bytes: int) -> str:
    """Formatea un tamaño de archivo en bytes a formato legible."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def format_time_duration(seconds: float) -> str:
    """Formatea una duración en segundos a formato legible."""
    if seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} segundos"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        return f"{hours}h {remaining_minutes}m"


def calculate_carbon_footprint_comparison(emissions_kg: float) -> Dict[str, str]:
    """
    Calcula comparaciones del footprint de carbono con actividades cotidianas.
    
    Args:
        emissions_kg: Emisiones en kilogramos de CO2
        
    Returns:
        Dict con comparaciones formateadas
    """
    comparisons = {
        'smartphone_charging': f"{emissions_kg / 0.008:.1f} cargas completas de smartphone",
        'led_bulb_hours': f"{emissions_kg / 0.007:.1f} horas de bombilla LED encendida",
        'car_km': f"{emissions_kg / 0.12:.2f} km recorridos en auto compacto",
        'tree_hours': f"{emissions_kg / (30/365/24):.1f} horas de absorción de un árbol",
        'streaming_hours': f"{emissions_kg / 0.036:.1f} horas de streaming en HD"
    }
    
    return comparisons
