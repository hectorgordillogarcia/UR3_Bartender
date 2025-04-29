import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import threading
import time
from tkinter import PhotoImage

# Archivos para guardar las selecciones y la elección actual
contador_file = "contador.json"
eleccion_file = "eleccion.json"

# Cargar contador
def cargar_contador():
    try:
        with open(contador_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"cocacola": 0, "aquarius": 0, "fanta": 0}

contador = cargar_contador()

# Función para verificar estado del brazo
def brazo_ocupado():
    try:
        with open(eleccion_file, "r") as f:
            data = json.load(f)
            return data.get("estado") == "ocupado"
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return False

# Función para actualizar los contadores en la interfaz
def actualizar_contadores():
    for bebida, label in contadores_labels.items():
        label.config(text=f"{bebida}: {contador[bebida]} veces")

# Función para actualizar la GUI desde el hilo principal
def actualizar_gui(bebida):
    contador[bebida] += 1
    with open(contador_file, "w") as f:
        json.dump(contador, f)
    actualizar_contadores()
    messagebox.showinfo("Completado", f"¡{bebida} entregada! Contador actualizado.")
    for boton in botones.values():
        boton.config(state=tk.NORMAL)
    label_estado.config(text="Estado: Brazo listo", fg="green")

# Hilo para monitorear el brazo
def monitorear_brazo(bebida):
    while brazo_ocupado():
        time.sleep(0.5)
    root.after(0, actualizar_gui, bebida)

# Función principal de selección
def elegir_bebida(bebida):
    bOcupado=brazo_ocupado()
    if bOcupado:
        messagebox.showwarning("Ocupado", "Espere a que termine el movimiento actual.")
        return
    
    
    
    with open(eleccion_file, "w") as f:
        json.dump({"eleccion": bebida, "estado": "ocupado"}, f)
    
    for boton in botones.values():
        boton.config(state=tk.DISABLED)
    
    label_estado.config(text=f"Estado: Moviendo {bebida}...", fg="orange")
    threading.Thread(target=monitorear_brazo, args=(bebida,)).start()

# Función para reiniciar el contador
def reiniciar_contador():
    global contador
    contador = {"cocacola": 0, "aquarius": 0, "fanta": 0}
    with open(contador_file, "w") as f:
        json.dump(contador, f)
    actualizar_contadores()
    messagebox.showinfo("Contador reiniciado", "El contador se ha reiniciado a cero.")

# Configuración de la GUI
root = tk.Tk()
root.title("Selección de Bebidas")
icon = PhotoImage(file="icono.png")  # usa PNG en lugar de ICO
root.iconphoto(True, icon)
root.geometry("450x500")
root.configure(bg="#f0f0f0")

frame_contenedor = tk.Frame(root, bg="#f0f0f0")
frame_contenedor.pack(expand=True, padx=20, pady=20)

# Título
tk.Label(frame_contenedor, 
        text="Seleccione su bebida:", 
        font=("Arial", 16, "bold"), 
        bg="#f0f0f0").pack(pady=10)

# Botones con imágenes
frame_botones = tk.Frame(frame_contenedor, bg="#f0f0f0")
frame_botones.pack(pady=15)

imagenes = {
    "cocacola": ImageTk.PhotoImage(Image.open("cocacola.png").resize((120, 120))),
    "fanta": ImageTk.PhotoImage(Image.open("fanta.png").resize((120, 120))),
    "aquarius": ImageTk.PhotoImage(Image.open("aquarius.png").resize((120, 120)))
}

botones = {}
for i, (bebida, img) in enumerate(imagenes.items()):
    boton = tk.Button(frame_botones, 
                     image=img, 
                     command=lambda b=bebida: elegir_bebida(b),
                     bg="white",
                     activebackground="#e0e0e0")
    boton.grid(row=0, column=i, padx=10)
    botones[bebida] = boton

# Contadores (en vertical)
frame_contadores = tk.Frame(frame_contenedor, bg="#f0f0f0")
frame_contadores.pack(pady=20)

contadores_labels = {}  # Diccionario para almacenar las etiquetas de los contadores
for i, bebida in enumerate(contador.keys()):
    tk.Label(frame_contadores, 
            text=f"{bebida}:", 
            font=("Arial", 12), 
            bg="#f0f0f0").grid(row=i, column=0, sticky="w")
    contadores_labels[bebida] = tk.Label(frame_contadores, 
                                        text=contador[bebida], 
                                        font=("Arial", 12, "bold"), 
                                        bg="#f0f0f0")
    contadores_labels[bebida].grid(row=i, column=1, sticky="w")

# Botón para reiniciar el contador
boton_reiniciar = tk.Button(frame_contenedor, 
                           text="Reiniciar contador", 
                           command=reiniciar_contador, 
                           bg="#ff4444", 
                           fg="white", 
                           font=("Arial", 12))
boton_reiniciar.pack(pady=10)

# Estado del sistema
label_estado = tk.Label(frame_contenedor, 
                       text="Estado: Brazo listo", 
                       font=("Arial", 12), 
                       fg="green",
                       bg="#f0f0f0")
label_estado.pack(pady=15)

# Guardar el estado al cerrar la aplicación
def on_closing():
    with open(contador_file, "w") as f:
        json.dump(contador, f)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)# Función periódica para revisar el estado del brazo
def verificar_estado_periodicamente():
    if not brazo_ocupado():
        for boton in botones.values():
            boton.config(state=tk.NORMAL)
        label_estado.config(text="Estado: Brazo listo", fg="green")
    root.after(1000, verificar_estado_periodicamente)  # Revisar cada 1 segundo

verificar_estado_periodicamente()



# Ejecutar la aplicación
root.mainloop()
