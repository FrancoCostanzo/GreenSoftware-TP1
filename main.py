import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import csv
import json
from datetime import datetime
import os
from ordenamientos import bubble_sort_step, insertion_sort_step, selection_sort_step, quick_sort_step, bogosort_step
from calculos import calcular_horas_para_compensar, iniciar_rastreador, detener_rastreador

# Variables globales
hilo_ordenamiento = None
cancelar_proceso = False


class CalculadoraEmisionesApp:
    def __init__(self, root):
        self.root = root
        self.configurar_ventana()
        self.inicializar_variables()
        self.configurar_estilo()
        self.crear_interfaz()
        self.cargar_configuracion()
        
    def configurar_ventana(self):
        """Configura la ventana principal"""
        self.root.title("🌱 Calculadora de Emisiones de CO2 - Green Software")
        self.root.state('zoomed')
        self.root.configure(bg='#f0f0f0')
        
    def inicializar_variables(self):
        """Inicializa todas las variables necesarias"""
        # Variables de datos
        self.datos = []
        self.i = 0
        self.j = 0
        self.step = 0
        self.stack = []
        self.tracker = None
        self.angulo = 0
        self.paused = False
        self.velocidad = 50  # ms entre pasos
        
        # Variables de interfaz
        self.cantidad_datos_var = tk.StringVar(value="50")
        self.metodo_ordenamiento_var = tk.StringVar(value="Bubble Sort")
        self.absorcion_arbol_var = tk.StringVar(value="30")
        self.emisiones_texto = tk.StringVar()
        self.horas_texto = tk.StringVar()
        self.estado = tk.StringVar(value="Listo para comenzar")
        self.progreso_var = tk.IntVar()
        
        # Historial de resultados
        self.historial = []
        
    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores personalizados
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), foreground='#2c3e50')
        self.style.configure('Subtitle.TLabel', font=('Helvetica', 12, 'bold'), foreground='#34495e')
        self.style.configure('Info.TLabel', font=('Helvetica', 10), foreground='#7f8c8d')
        self.style.configure('Success.TLabel', font=('Helvetica', 12, 'bold'), foreground='#27ae60')
        self.style.configure('Warning.TLabel', font=('Helvetica', 12, 'bold'), foreground='#e74c3c')
        self.style.configure('Primary.TButton', font=('Helvetica', 10, 'bold'))
        
    def crear_interfaz(self):
        """Crea toda la interfaz de usuario"""
        # Frame principal con scroll
        main_canvas = tk.Canvas(self.root, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = ttk.Frame(main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Crear secciones
        self.crear_header()
        self.crear_seccion_configuracion()
        self.crear_seccion_controles()
        self.crear_seccion_progreso()
        self.crear_seccion_resultados()
        self.crear_seccion_grafico()
        self.crear_seccion_historial()
        self.crear_menu()
        
        # Empaquetar el canvas principal
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def crear_header(self):
        """Crea el encabezado de la aplicación"""
        header_frame = ttk.Frame(self.scrollable_frame, padding="20")
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(header_frame, text="🌱 Calculadora de Emisiones de CO2", 
                 style='Title.TLabel').pack()
        ttk.Label(header_frame, text="Analiza el impacto ambiental de algoritmos de ordenamiento", 
                 style='Info.TLabel').pack(pady=(5, 0))
        
        ttk.Separator(self.scrollable_frame, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
    def crear_seccion_configuracion(self):
        """Crea la sección de configuración"""
        config_frame = ttk.LabelFrame(self.scrollable_frame, text="⚙️ Configuración", padding="15")
        config_frame.pack(fill="x", padx=20, pady=10)
        
        # Frame para organizar en columnas
        cols_frame = ttk.Frame(config_frame)
        cols_frame.pack(fill="x")
        
        # Columna 1: Datos
        col1 = ttk.Frame(cols_frame)
        col1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ttk.Label(col1, text="Cantidad de datos:", style='Subtitle.TLabel').pack(anchor="w")
        cantidad_frame = ttk.Frame(col1)
        cantidad_frame.pack(fill="x", pady=(5, 15))
        
        self.cantidad_entry = ttk.Entry(cantidad_frame, textvariable=self.cantidad_datos_var, width=10)
        self.cantidad_entry.pack(side="left")
        
        ttk.Scale(cantidad_frame, from_=10, to=1000, variable=self.cantidad_datos_var, 
                 orient="horizontal", command=self.on_scale_change).pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Columna 2: Algoritmo
        col2 = ttk.Frame(cols_frame)
        col2.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        ttk.Label(col2, text="Algoritmo de ordenamiento:", style='Subtitle.TLabel').pack(anchor="w")
        self.metodo_menu = ttk.Combobox(col2, textvariable=self.metodo_ordenamiento_var, 
                                       values=["Bubble Sort", "Insertion Sort", "Selection Sort", 
                                              "Quick Sort", "Bogosort"], state="readonly")
        self.metodo_menu.pack(fill="x", pady=(5, 15))
        
        # Configuración avanzada
        advanced_frame = ttk.LabelFrame(config_frame, text="Configuración Avanzada", padding="10")
        advanced_frame.pack(fill="x", pady=(10, 0))
        
        absorcion_frame = ttk.Frame(advanced_frame)
        absorcion_frame.pack(fill="x")
        
        ttk.Label(absorcion_frame, text="Absorción del árbol (kg CO2/año):").pack(side="left")
        ttk.Entry(absorcion_frame, textvariable=self.absorcion_arbol_var, width=10).pack(side="left", padx=(10, 0))
        
        # Control de velocidad
        velocidad_frame = ttk.Frame(advanced_frame)
        velocidad_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(velocidad_frame, text="Velocidad de visualización:").pack(side="left")
        self.velocidad_scale = ttk.Scale(velocidad_frame, from_=1, to=200, 
                                        command=self.cambiar_velocidad, orient="horizontal")
        self.velocidad_scale.set(self.velocidad)
        self.velocidad_scale.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
    def crear_seccion_controles(self):
        """Crea la sección de controles"""
        controls_frame = ttk.LabelFrame(self.scrollable_frame, text="🎮 Controles", padding="15")
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack()
        
        # Botones principales
        self.btn_iniciar = ttk.Button(buttons_frame, text="🚀 Iniciar Análisis", 
                                     command=self.procesar_datos, style='Primary.TButton')
        self.btn_iniciar.pack(side="left", padx=5)
        
        self.btn_pausar = ttk.Button(buttons_frame, text="⏸️ Pausar", 
                                    command=self.pausar_reanudar, state="disabled")
        self.btn_pausar.pack(side="left", padx=5)
        
        self.btn_cancelar = ttk.Button(buttons_frame, text="⏹️ Cancelar", 
                                      command=self.cancelar_ordenamiento, state="disabled")
        self.btn_cancelar.pack(side="left", padx=5)
        
        self.btn_exportar = ttk.Button(buttons_frame, text="💾 Exportar Resultados", 
                                      command=self.exportar_resultados)
        self.btn_exportar.pack(side="left", padx=5)
        
    def crear_seccion_progreso(self):
        """Crea la sección de progreso"""
        progress_frame = ttk.LabelFrame(self.scrollable_frame, text="📊 Progreso", padding="15")
        progress_frame.pack(fill="x", padx=20, pady=10)
        
        # Estado
        self.estado_label = ttk.Label(progress_frame, textvariable=self.estado, style='Info.TLabel')
        self.estado_label.pack(pady=(0, 10))
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progreso_var, 
                                          maximum=100, mode='determinate')
        self.progress_bar.pack(fill="x", pady=(0, 5))
        
    def crear_seccion_resultados(self):
        """Crea la sección de resultados"""
        results_frame = ttk.LabelFrame(self.scrollable_frame, text="🌱 Resultados", padding="15")
        results_frame.pack(fill="x", padx=20, pady=10)
        
        self.emisiones_label = ttk.Label(results_frame, textvariable=self.emisiones_texto, 
                                        style='Success.TLabel')
        self.emisiones_label.pack(pady=5)
        
        self.horas_label = ttk.Label(results_frame, textvariable=self.horas_texto, 
                                   style='Success.TLabel')
        self.horas_label.pack(pady=5)
        
    def crear_seccion_grafico(self):
        """Crea la sección del gráfico"""
        graph_frame = ttk.LabelFrame(self.scrollable_frame, text="📈 Visualización", padding="15")
        graph_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configurar matplotlib con tema oscuro
        plt.style.use('default')
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.fig.patch.set_facecolor('#f0f0f0')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def crear_seccion_historial(self):
        """Crea la sección del historial"""
        history_frame = ttk.LabelFrame(self.scrollable_frame, text="📋 Historial", padding="15")
        history_frame.pack(fill="x", padx=20, pady=10)
        
        # Treeview para mostrar historial
        columns = ('Fecha', 'Algoritmo', 'Datos', 'Emisiones (kg)', 'Tiempo Compensación (h)')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120)
            
        scrollbar_hist = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar_hist.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar_hist.pack(side="right", fill="y")
        
    def crear_menu(self):
        """Crea el menú de la aplicación"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Guardar Configuración", command=self.guardar_configuracion)
        file_menu.add_command(label="Cargar Configuración", command=self.cargar_configuracion_archivo)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar Historial", command=self.exportar_historial)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Sobre la aplicación", command=self.mostrar_acerca_de)
        help_menu.add_command(label="Guía de uso", command=self.mostrar_ayuda)


        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Sobre la aplicación", command=self.mostrar_acerca_de)
        help_menu.add_command(label="Guía de uso", command=self.mostrar_ayuda)
        
    def on_scale_change(self, value):
        """Actualiza el entry cuando cambia el scale"""
        self.cantidad_datos_var.set(str(int(float(value))))
        
    def cambiar_velocidad(self, value):
        """Cambia la velocidad de visualización"""
        self.velocidad = 201 - int(float(value))  # Invertir para que mayor valor = más rápido
        
    def validar_entrada(self):
        """Valida que los datos de entrada sean correctos"""
        try:
            cantidad = int(self.cantidad_datos_var.get())
            if cantidad < 10 or cantidad > 1000:
                raise ValueError("La cantidad debe estar entre 10 y 1000")
                
            absorcion = float(self.absorcion_arbol_var.get())
            if absorcion <= 0:
                raise ValueError("La absorción debe ser mayor a 0")
                
            return True
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
            return False
            
    def procesar_datos(self):
        """Inicia el proceso de análisis"""
        if not self.validar_entrada():
            return
            
        global hilo_ordenamiento, cancelar_proceso
        cancelar_proceso = False
        
        # Preparar datos
        cantidad_datos = int(self.cantidad_datos_var.get())
        self.datos = [random.randint(0, 100000) for _ in range(cantidad_datos)]
        self.i = 0
        self.j = 0
        self.step = 0
        self.stack = [(0, len(self.datos) - 1)]
        
        # Actualizar interfaz
        self.estado.set("Iniciando análisis...")
        self.progreso_var.set(0)
        self.btn_iniciar.config(state="disabled")
        self.btn_pausar.config(state="normal", text="⏸️ Pausar")
        self.btn_cancelar.config(state="normal")
        
        # Iniciar rastreador
        self.tracker = iniciar_rastreador()
        self.tiempo_inicio = time.time()
        
        # Lanzar hilo de procesamiento
        hilo_ordenamiento = threading.Thread(target=self.actualizar_ordenamiento)
        hilo_ordenamiento.daemon = True
        hilo_ordenamiento.start()
        
    def pausar_reanudar(self):
        """Pausa o reanuda el procesamiento"""
        self.paused = not self.paused
        if self.paused:
            self.btn_pausar.config(text="▶️ Reanudar")
            self.estado.set("Procesamiento pausado")
        else:
            self.btn_pausar.config(text="⏸️ Pausar")
            self.estado.set("Procesamiento reanudado")
            
    def cancelar_ordenamiento(self):
        """Cancela el procesamiento actual"""
        global cancelar_proceso
        cancelar_proceso = True
        self.estado.set("Cancelando...")
        self.restablecer_controles()
        
    def restablecer_controles(self):
        """Restablece el estado de los controles"""
        self.btn_iniciar.config(state="normal")
        self.btn_pausar.config(state="disabled")
        self.btn_cancelar.config(state="disabled")
        self.paused = False
        
    def actualizar_ordenamiento(self):
        """Método principal de ordenamiento ejecutado en hilo separado"""
        metodo = self.metodo_ordenamiento_var.get()
        pasos_totales = self.estimar_pasos_totales(metodo)
        pasos_actuales = 0
        
        try:
            while True:
                if cancelar_proceso:
                    self.root.after(0, lambda: self.estado.set("Proceso cancelado"))
                    self.root.after(0, self.restablecer_controles)
                    return
                    
                while self.paused:
                    time.sleep(0.1)
                    if cancelar_proceso:
                        return
                        
                # Ejecutar paso del algoritmo
                if metodo == "Bubble Sort":
                    completo, self.i, self.j = bubble_sort_step(self.datos, self.i, self.j)
                    indices_a_colorear = [self.j, self.j + 1] if self.j + 1 < len(self.datos) else [self.j]
                elif metodo == "Insertion Sort":
                    completo, self.i = insertion_sort_step(self.datos, self.i)
                    indices_a_colorear = [self.i] if self.i < len(self.datos) else []
                elif metodo == "Selection Sort":
                    completo, self.i = selection_sort_step(self.datos, self.i)
                    indices_a_colorear = [self.i] if self.i < len(self.datos) else []
                elif metodo == "Quick Sort":
                    completo, self.stack, indices_a_colorear = quick_sort_step(self.datos, self.stack)
                elif metodo == "Bogosort":
                    completo, self.datos = bogosort_step(self.datos)
                    indices_a_colorear = list(range(len(self.datos))) if not completo else []
                    
                # Actualizar gráfico y progreso
                pasos_actuales += 1
                progreso = min(100, (pasos_actuales / pasos_totales) * 100) if pasos_totales > 0 else 0
                
                self.root.after(0, lambda p=progreso: self.progreso_var.set(int(p)))
                self.root.after(0, lambda: self.actualizar_grafico(indices_a_colorear, metodo))
                self.root.after(0, lambda: self.estado.set(f"Procesando... Paso {pasos_actuales}"))
                
                if completo:
                    self.finalizar_procesamiento()
                    break
                    
                time.sleep(self.velocidad / 1000.0)
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}"))
            self.root.after(0, self.restablecer_controles)
            
    def estimar_pasos_totales(self, metodo):
        """Estima el número total de pasos para el algoritmo"""
        n = len(self.datos)
        if metodo == "Bubble Sort":
            return n * (n - 1) // 2
        elif metodo == "Insertion Sort":
            return n
        elif metodo == "Selection Sort":
            return n
        elif metodo == "Quick Sort":
            return n * 2  # Estimación aproximada
        elif metodo == "Bogosort":
            return 1000  # Imposible de estimar, usamos valor arbitrario
        return n
        
    def actualizar_grafico(self, indices_a_colorear, metodo):
        """Actualiza la visualización del gráfico"""
        try:
            self.ax.clear()
            
            # Crear barras base
            bars = self.ax.bar(range(len(self.datos)), self.datos, color='#3498db', 
                              edgecolor='white', linewidth=0.5, alpha=0.8)
            
            # Colorear barras específicas
            for idx in indices_a_colorear:
                if 0 <= idx < len(bars):
                    bars[idx].set_color('#e74c3c')
                    bars[idx].set_alpha(1.0)
                    
            self.ax.set_xlabel('Índice', fontsize=12)
            self.ax.set_ylabel('Valor', fontsize=12)
            self.ax.set_title(f'Ordenamiento: {metodo}', fontsize=14, fontweight='bold')
            self.ax.grid(True, alpha=0.3)
            
            self.canvas.draw_idle()
        except Exception as e:
            print(f"Error actualizando gráfico: {e}")
            
    def finalizar_procesamiento(self):
        """Finaliza el procesamiento y muestra resultados"""
        try:
            # Detener rastreador y calcular emisiones
            emisiones_totales_kg = detener_rastreador(self.tracker)
            absorcion = float(self.absorcion_arbol_var.get())
            horas_para_compensar = calcular_horas_para_compensar(emisiones_totales_kg, absorcion)
            tiempo_total = time.time() - self.tiempo_inicio
            
            # Actualizar interfaz
            self.emisiones_texto.set(f"💨 Emisiones totales de CO2: {emisiones_totales_kg:.6f} kg")
            self.horas_texto.set(f"🌳 Tiempo de compensación: {horas_para_compensar:.2f} horas")
            self.estado.set(f"✅ Análisis completado en {tiempo_total:.2f} segundos")
            self.progreso_var.set(100)
            
            # Añadir al historial
            resultado = {
                'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'algoritmo': self.metodo_ordenamiento_var.get(),
                'datos': len(self.datos),
                'emisiones': emisiones_totales_kg,
                'horas_compensacion': horas_para_compensar,
                'tiempo_ejecucion': tiempo_total
            }
            
            self.historial.append(resultado)
            self.actualizar_historial_visual()
            
            # Restablecer controles
            self.restablecer_controles()
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Análisis Completado", 
                              f"El análisis se completó exitosamente.\n"
                              f"Emisiones: {emisiones_totales_kg:.6f} kg CO2\n"
                              f"Tiempo de compensación: {horas_para_compensar:.2f} horas")
                              
        except Exception as e:
            messagebox.showerror("Error", f"Error finalizando el procesamiento: {str(e)}")
            self.restablecer_controles()
            
    def actualizar_historial_visual(self):
        """Actualiza la visualización del historial"""
        # Limpiar historial actual
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Añadir entradas (últimas 10)
        for resultado in self.historial[-10:]:
            self.history_tree.insert('', 'end', values=(
                resultado['fecha'],
                resultado['algoritmo'],
                resultado['datos'],
                f"{resultado['emisiones']:.6f}",
                f"{resultado['horas_compensacion']:.2f}"
            ))
            
    def exportar_resultados(self):
        """Exporta los resultados actuales a CSV"""
        if not self.historial:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar resultados"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['fecha', 'algoritmo', 'datos', 'emisiones', 'horas_compensacion', 'tiempo_ejecucion']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for resultado in self.historial:
                        writer.writerow(resultado)
                        
                messagebox.showinfo("Éxito", f"Resultados exportados a: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error exportando resultados: {str(e)}")
                
    def exportar_historial(self):
        """Exporta todo el historial a CSV"""
        self.exportar_resultados()
        
    def guardar_configuracion(self):
        """Guarda la configuración actual"""
        config = {
            'cantidad_datos': self.cantidad_datos_var.get(),
            'metodo_ordenamiento': self.metodo_ordenamiento_var.get(),
            'absorcion_arbol': self.absorcion_arbol_var.get(),
            'velocidad': self.velocidad
        }
        
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            messagebox.showinfo("Éxito", "Configuración guardada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando configuración: {str(e)}")
            
    def cargar_configuracion(self):
        """Carga la configuración guardada"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    
                self.cantidad_datos_var.set(config.get('cantidad_datos', '50'))
                self.metodo_ordenamiento_var.set(config.get('metodo_ordenamiento', 'Bubble Sort'))
                self.absorcion_arbol_var.set(config.get('absorcion_arbol', '30'))
                self.velocidad = config.get('velocidad', 50)
                
                if hasattr(self, 'velocidad_scale'):
                    self.velocidad_scale.set(201 - self.velocidad)
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            
    def cargar_configuracion_archivo(self):
        """Carga configuración desde archivo"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Cargar configuración"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                    
                self.cantidad_datos_var.set(config.get('cantidad_datos', '50'))
                self.metodo_ordenamiento_var.set(config.get('metodo_ordenamiento', 'Bubble Sort'))
                self.absorcion_arbol_var.set(config.get('absorcion_arbol', '30'))
                self.velocidad = config.get('velocidad', 50)
                
                if hasattr(self, 'velocidad_scale'):
                    self.velocidad_scale.set(201 - self.velocidad)
                    
                messagebox.showinfo("Éxito", "Configuración cargada exitosamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando configuración: {str(e)}")
                
    def mostrar_acerca_de(self):
        """Muestra información sobre la aplicación"""
        about_text = """
🌱 Calculadora de Emisiones de CO2 - Green Software
Versión 2.0

Esta aplicación analiza el impacto ambiental de diferentes 
algoritmos de ordenamiento midiendo sus emisiones de CO2.

Características:
• Análisis de 5 algoritmos de ordenamiento
• Medición en tiempo real de emisiones de CO2
• Cálculo de tiempo de compensación arbórea
• Visualización gráfica interactiva
• Historial de análisis
• Exportación de resultados

Desarrollado como parte del proyecto Green Software
para concientizar sobre el impacto ambiental del desarrollo de software.

© 2025 - Proyecto Green Software
        """
        messagebox.showinfo("Acerca de", about_text)
        
    def mostrar_ayuda(self):
        """Muestra la guía de uso"""
        help_text = """
📖 Guía de Uso

1. Configuración:
   • Seleccione la cantidad de datos (10-1000)
   • Elija el algoritmo de ordenamiento
   • Configure la absorción del árbol si es necesario
   • Ajuste la velocidad de visualización

2. Análisis:
   • Haga clic en "Iniciar Análisis" para comenzar
   • Use "Pausar" para detener temporalmente
   • Use "Cancelar" para abortar el proceso

3. Resultados:
   • Vea las emisiones de CO2 generadas
   • Observe el tiempo de compensación necesario
   • Revise el historial de análisis

4. Exportación:
   • Exporte resultados individuales o historial completo
   • Los archivos se guardan en formato CSV

Algoritmos disponibles:
• Bubble Sort: O(n²) - Educativo
• Insertion Sort: O(n²) - Eficiente para arrays pequeños
• Selection Sort: O(n²) - Simple pero ineficiente
• Quick Sort: O(n log n) promedio - Muy eficiente
• Bogosort: O(n!) - Solo para propósitos educativos

¡Experimente con diferentes configuraciones para 
entender el impacto ambiental de cada algoritmo!
        """
        messagebox.showinfo("Guía de Uso", help_text)


def main():
    """Función principal"""
    root = tk.Tk()
    app = CalculadoraEmisionesApp(root)
    
    # Configurar el cierre de la aplicación
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir?"):
            global cancelar_proceso
            cancelar_proceso = True
            root.destroy()
            
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
