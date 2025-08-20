# 🌱 Green Software - Calculadora de Emisiones CO2

Una aplicación de escritorio interactiva para analizar el impacto ambiental de diferentes algoritmos de ordenamiento, midiendo sus emisiones de CO2 y calculando el tiempo necesario para su compensación natural.

## 🚀 Características Principales

### 🔬 Análisis de Algoritmos
- **5 algoritmos de ordenamiento**: Bubble Sort, Insertion Sort, Selection Sort, Quick Sort, y Bogosort
- **Análisis en tiempo real** de emisiones de CO2 usando [CodeCarbon](https://codecarbon.io/)
- **Visualización interactiva** del proceso de ordenamiento
- **Métricas de rendimiento** detalladas

### 🌍 Impacto Ambiental
- Medición precisa de emisiones de CO2
- Cálculo de tiempo de compensación arbórea
- Equivalencias con actividades cotidianas
- Análisis de costo ambiental

### 📊 Visualización y Reportes
- Gráficos interactivos con Matplotlib
- Historial de análisis
- Exportación a CSV, JSON y HTML
- Comparaciones entre algoritmos

### ⚙️ Interfaz Avanzada
- Diseño moderno con tkinter
- Control de velocidad de visualización
- Pausa/reanudación de procesos
- Configuración personalizable
- Tooltips informativos

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Dependencias
```bash
pip install codecarbon matplotlib tkinter
```

### Instalación desde código fuente
1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/green-software-tp1.git
cd green-software-tp1
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python main.py
```

## 📖 Guía de Uso

### 1. Configuración Inicial
- **Cantidad de datos**: Seleccione entre 10 y 1,000 elementos
- **Algoritmo**: Elija el algoritmo a analizar
- **Absorción del árbol**: Configure la capacidad de absorción (por defecto 30 kg CO2/año)
- **Velocidad**: Ajuste la velocidad de visualización

### 2. Ejecutar Análisis
- Haga clic en **"🚀 Iniciar Análisis"** para comenzar
- Use **"⏸️ Pausar"** para detener temporalmente
- Use **"⏹️ Cancelar"** para abortar el proceso

### 3. Resultados
- Observe las emisiones de CO2 generadas
- Revise el tiempo de compensación necesario
- Analice la visualización del ordenamiento
- Consulte el historial de análisis

### 4. Exportación
- **CSV**: Para análisis en hojas de cálculo
- **JSON**: Para procesamiento programático
- **HTML**: Reportes visuales completos

## 🧮 Algoritmos Soportados

| Algoritmo | Complejidad Temporal | Complejidad Espacial | Uso Recomendado |
|-----------|---------------------|---------------------|----------------|
| **Bubble Sort** | O(n²) | O(1) | Educativo, arrays muy pequeños |
| **Insertion Sort** | O(n²) | O(1) | Arrays pequeños, datos parcialmente ordenados |
| **Selection Sort** | O(n²) | O(1) | Memoria limitada |
| **Quick Sort** | O(n log n) promedio | O(log n) | Uso general, arrays grandes |
| **Bogosort** | O(n!) | O(1) | Solo educativo/experimental |

### 🌱 Eficiencia Ambiental
- **🟢 Altamente Eficiente**: Quick Sort
- **🟡 Moderadamente Eficiente**: Insertion Sort
- **🟠 Poco Eficiente**: Bubble Sort, Selection Sort
- **🔴 Extremadamente Ineficiente**: Bogosort (evitar siempre)

## 📊 Métricas y Análisis

### Emisiones de CO2
- Medición en tiempo real usando sensores de hardware
- Cálculo basado en el consumo energético del procesador
- Consideración de la matriz energética local

### Compensación Arbórea
- Cálculo basado en la absorción anual promedio de un árbol
- Valores configurables (10-100 kg CO2/año)
- Conversión a horas, días y años de absorción

### Equivalencias Cotidianas
- Kilometraje en automóvil
- Horas de dispositivos electrónicos
- Streaming de video
- Y más comparaciones útiles

## ⚙️ Configuración Avanzada

### Archivo de Configuración
La aplicación utiliza `config.json` para persistir configuraciones:

```json
{
  "data_count": 50,
  "algorithm": "Quick Sort",
  "tree_absorption": 30.0,
  "visualization_speed": 50,
  "auto_save_results": true,
  "show_detailed_stats": false
}
```

### Variables de Entorno
- `GREEN_SOFTWARE_DEBUG`: Habilita modo debug
- `CODECARBON_LOG_LEVEL`: Nivel de logging de CodeCarbon

## 🔧 Desarrollo

### Estructura del Proyecto
```
green-software-tp1/
├── main.py                 # Aplicación principal
├── calculos.py            # Cálculos de emisiones y compensación
├── ordenamientos.py       # Implementación de algoritmos
├── utils.py               # Utilidades y herramientas
├── config_default.json    # Configuración por defecto
├── requirements.txt       # Dependencias Python
└── README.md             # Este archivo
```

### Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

### Tests
```bash
python -m pytest tests/
```

## 📈 Casos de Uso

### 🎓 Educativo
- Enseñanza de algoritmos de ordenamiento
- Demostración de complejidad computacional
- Concienciación sobre impacto ambiental del software

### 🔬 Investigación
- Análisis comparativo de algoritmos
- Estudios de eficiencia energética
- Investigación en Green Software Engineering

### 🏢 Empresarial
- Auditoría de algoritmos en producción
- Optimización basada en criterios ambientales
- Reportes de sostenibilidad

## 🌟 Características Técnicas

### Tecnologías Utilizadas
- **Python 3.8+**: Lenguaje principal
- **tkinter**: Interfaz gráfica nativa
- **matplotlib**: Visualización de datos
- **CodeCarbon**: Medición de emisiones
- **JSON/CSV**: Exportación de datos

### Rendimiento
- Análisis en tiempo real
- Procesamiento asíncrono
- Interfaz responsive
- Manejo eficiente de memoria

### Compatibilidad
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+)
- ✅ Python 3.8-3.11

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙋‍♂️ Soporte

### Problemas Comunes

**Error de importación de matplotlib**
```bash
pip install matplotlib
# o en Ubuntu/Debian:
sudo apt-get install python3-matplotlib
```

**CodeCarbon no funciona**
- Asegúrese de tener permisos de lectura de hardware
- En Linux, puede requerir instalación de bibliotecas adicionales

**Interfaz no responde**
- Reduzca la cantidad de datos
- Aumente la velocidad de visualización
- Cierre otras aplicaciones que consuman recursos

### Contacto
- 📧 Email: [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/green-software-tp1/issues)
- 💬 Discusiones: [GitHub Discussions](https://github.com/tu-usuario/green-software-tp1/discussions)

## 🎯 Roadmap

### Versión 2.1 (Próximamente)
- [ ] Más algoritmos de ordenamiento
- [ ] Análisis de algoritmos de búsqueda
- [ ] Integración con bases de datos
- [ ] API REST para análisis remoto

### Versión 2.2 (Planificado)
- [ ] Machine Learning para predicción de consumo
- [ ] Dashboard web complementario
- [ ] Integración con sistemas de CI/CD
- [ ] Métricas de sostenibilidad empresarial

---

## 🌍 Contribuye a un Futuro más Verde

Este proyecto es parte del movimiento **Green Software Engineering**, que busca crear software más sostenible y consciente del medio ambiente. Cada línea de código cuenta para construir un futuro digital más verde.

**¡Gracias por usar Green Software!** 🌱

---

*Desarrollado con 💚 para un planeta más sostenible*
