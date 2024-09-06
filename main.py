import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from ordenamientos import bubble_sort_step, insertion_sort_step, selection_sort_step, quick_sort_step, bogosort_step
from calculos import calcular_horas_para_compensar, iniciar_rastreador, detener_rastreador

# Variables globales
hilo_ordenamiento = None
cancelar_proceso = False


# Funciones de interfaz
def mostrar_mensaje_cargando():
    mensaje_cargando.pack(pady=10)
    canvas_cargando.pack(pady=20)
    emisiones_label.pack_forget()
    horas_label.pack_forget()
    estado_label.pack_forget()
    ventana.after(100, animar_cargando)  # Iniciar animación


def ocultar_mensaje_cargando():
    mensaje_cargando.pack_forget()
    canvas_cargando.pack_forget()
    emisiones_label.pack(pady=5)
    horas_label.pack(pady=5)
    estado_label.pack(pady=5)


def animar_cargando():
    global angulo
    angulo = (angulo + 10) % 360
    canvas_cargando.delete("all")
    canvas_cargando.create_arc(10, 10, 110, 110, start=angulo, extent=45, fill="blue", outline="black")
    ventana.after(100, animar_cargando)


def actualizar_menu():
    metodo_ordenamiento_menu['menu'].delete(0, 'end')
    for metodo in ["Bubble Sort", "Insertion Sort", "Selection Sort", "Quick Sort", "Bogosort"]:
        metodo_ordenamiento_menu['menu'].add_command(
            label=metodo,
            command=lambda valor = metodo: metodo_ordenamiento_var.set(valor)
        )


def procesar_datos():
    global datos, i, j, tracker, metodo_ordenamiento, step, stack, hilo_ordenamiento, cancelar_proceso
    cancelar_proceso = False  # Reiniciar la bandera de cancelación
    cantidad_datos = int(cantidad_datos_var.get())
    datos = [random.randint(0, 100000) for _ in range(cantidad_datos)]
    i = 0
    j = 0
    step = 0
    stack = [(0, len(datos) - 1)]  # Para Quick Sort

    tracker = iniciar_rastreador()
    estado.set("Ordenando datos y rastreando emisiones...")

    mostrar_mensaje_cargando()  # Mostrar mensaje de cargando

    # Iniciar el proceso de ordenamiento en un hilo separado
    hilo_ordenamiento = threading.Thread(target=actualizar_ordenamiento)
    hilo_ordenamiento.start()


def cancelar_ordenamiento():
    global cancelar_proceso
    cancelar_proceso = True
    estado.set("Proceso cancelado.")
    ocultar_mensaje_cargando()  # Ocultar mensaje de cargando


def actualizar_ordenamiento():
    global i, j, step, tracker, stack, datos

    metodo_ordenamiento = metodo_ordenamiento_var.get()  # Obtener el método seleccionado

    while True:
        if cancelar_proceso:
            return  # Terminar el hilo si se canceló el proceso

        if metodo_ordenamiento == "Bubble Sort":
            completo, i, j = bubble_sort_step(datos, i, j)
            indices_a_colorear = [j, j + 1]
        elif metodo_ordenamiento == "Insertion Sort":
            completo, i = insertion_sort_step(datos, i)
            indices_a_colorear = [i]
        elif metodo_ordenamiento == "Selection Sort":
            completo, i = selection_sort_step(datos, i)
            indices_a_colorear = [i]
        elif metodo_ordenamiento == "Quick Sort":
            completo, stack, indices_a_colorear = quick_sort_step(datos, stack)
        elif metodo_ordenamiento == "Bogosort":
            completo, datos = bogosort_step(datos)
            indices_a_colorear = range(len(datos)) if not completo else []

        plt.clf()
        plt.bar(range(len(datos)), datos, color="blue", edgecolor="black")

        # Colorear las barras
        for idx in indices_a_colorear:
            if idx < len(datos):
                plt.bar(idx, datos[idx], color="red", edgecolor="black")

        plt.xlabel('Índice')
        plt.ylabel('Valor')
        plt.title(f'Ordenamiento por {metodo_ordenamiento}')
        canvas.draw()

        if completo:
            emisiones_totales_kg = detener_rastreador(tracker)
            calcular_emisiones(emisiones_totales_kg)
            ocultar_mensaje_cargando()  # Ocultar mensaje de cargando
            break


def calcular_emisiones(emisiones_totales_kg):
    emisiones_texto.set(f"Emisiones totales de CO2: {emisiones_totales_kg:.6f} kg")
    horas_para_compensar = calcular_horas_para_compensar(emisiones_totales_kg)
    horas_texto.set(
        f"Un árbol deberá absorber CO2 durante aproximadamente {horas_para_compensar:.6f} horas para compensar las "
        f"emisiones generadas por este proceso.")
    estado.set("Cálculo completado.")


# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Calculadora de Emisiones de CO2")
ventana.state('zoomed')  # Poner la ventana en modo pantalla completa con los controles visibles

instrucciones = ttk.Label(ventana,
                          text="Selecciona la cantidad de datos, el método de ordenamiento y haz clic en calcular.")
instrucciones.pack(pady=10)

ttk.Label(ventana, text="Cantidad de datos:").pack(pady=5)
cantidad_datos_var = tk.StringVar(value="50")
cantidad_datos_entry = ttk.Entry(ventana, textvariable=cantidad_datos_var)
cantidad_datos_entry.pack(pady=5)

ttk.Label(ventana, text="Método de ordenamiento:").pack(pady=5)
metodo_ordenamiento_var = tk.StringVar(value="Bubble Sort")
metodo_ordenamiento_menu = ttk.OptionMenu(ventana, metodo_ordenamiento_var, "Bubble Sort")
metodo_ordenamiento_menu.pack(pady=5)
actualizar_menu()

# Botones para iniciar y cancelar el proceso
boton_calcular = ttk.Button(ventana, text="Calcular Emisiones", command=procesar_datos)
boton_calcular.pack(pady=10)

boton_cancelar = ttk.Button(ventana, text="Cancelar", command=cancelar_ordenamiento)
boton_cancelar.pack(pady=10)

# Elementos de carga
mensaje_cargando = ttk.Label(ventana, text="Cargando, por favor espere...", font=("Helvetica", 16, "bold"),
                             foreground="red")
canvas_cargando = tk.Canvas(ventana, width=120, height=120)

emisiones_texto = tk.StringVar()
emisiones_label = ttk.Label(ventana, textvariable=emisiones_texto, font=("Helvetica", 14, "bold"), foreground="green")
emisiones_label.pack(pady=5)

horas_texto = tk.StringVar()
horas_label = ttk.Label(ventana, textvariable=horas_texto, font=("Helvetica", 14, "bold"), foreground="green")
horas_label.pack(pady=5)

estado = tk.StringVar()
estado_label = ttk.Label(ventana, textvariable=estado, font=("Helvetica", 14, "bold"), foreground="blue")
estado_label.pack(pady=5)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack()

datos = []
i = 0
j = 0
step = 0
stack = []
tracker = None
angulo = 0  # Inicializar el ángulo para la animación

ventana.mainloop()
