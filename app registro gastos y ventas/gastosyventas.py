import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime

# Crear la conexión a la base de datos SQLite
conn = sqlite3.connect('registros.db')
c = conn.cursor()

# Crear tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS registros
             (id INTEGER PRIMARY KEY,
             tipo TEXT,
             categoria TEXT,
             monto REAL,
             hora TIMESTAMP,
             turno TEXT)''')
conn.commit()

# Función para guardar un registro
def guardar_registro():
    tipo = tipo_combo.get()
    categoria = categoria_combo.get()
    monto = monto_entry.get()
    hora = datetime.datetime.now()
    turno = turno_combo.get()  # Obtener el turno seleccionado
    
    c.execute("INSERT INTO registros (tipo, categoria, monto, hora, turno) VALUES (?, ?, ?, ?, ?)", 
              (tipo, categoria, monto, hora, turno))
    conn.commit()
    actualizar_lista()
    limpiar_campos()

# Función para limpiar los campos después de guardar
def limpiar_campos():
    tipo_combo.set('')
    categoria_var.set('')
    monto_entry.delete(0, tk.END)
    turno_combo.set('')  # Limpiar la selección de turno

# Función para actualizar la lista de registros
def actualizar_lista():
    registros_tree.delete(*registros_tree.get_children())
    c.execute("SELECT * FROM registros")
    registros = c.fetchall()
    for registro in registros:
        registros_tree.insert('', 'end', values=registro)

# Función para agregar una nueva categoría
def agregar_categoria():
    nueva_categoria = nueva_categoria_entry.get()
    if nueva_categoria:
        categorias.append(nueva_categoria)
        categoria_combo['values'] = categorias
        categoria_combo.set(nueva_categoria)
        nueva_categoria_entry.delete(0, tk.END)

# Función para eliminar una categoría
def eliminar_categoria():
    categoria_seleccionada = categoria_combo.get()
    if categoria_seleccionada in categorias:
        categorias.remove(categoria_seleccionada)
        categoria_combo['values'] = categorias
        categoria_combo.set('')
        c.execute("DELETE FROM registros WHERE categoria=?", (categoria_seleccionada,))
        conn.commit()
        actualizar_lista()

# Crear la ventana principal
root = tk.Tk()
root.title("Registro de Gastos y Ventas")

# Variables y lista de categorías
tipo_options = ["Gasto", "Venta"]
tipo_combo = ttk.Combobox(root, values=tipo_options)
tipo_combo.set("Gasto")  # Establecer el valor inicial
tipo_combo.pack(padx=10, pady=5)

categorias = ["Alimentación", "Transporte", "Entretenimiento"]
categoria_var = tk.StringVar()
categoria_combo = ttk.Combobox(root, values=categorias)
categoria_combo.pack(padx=10, pady=5)

nueva_categoria_entry = ttk.Entry(root)
nueva_categoria_entry.pack(padx=10, pady=5)

agregar_categoria_button = ttk.Button(root, text="Agregar Categoría", command=agregar_categoria)
agregar_categoria_button.pack(padx=10, pady=5)

eliminar_categoria_button = ttk.Button(root, text="Eliminar Categoría", command=eliminar_categoria)
eliminar_categoria_button.pack(padx=10, pady=5)

# Marco para la entrada de datos
input_frame = ttk.LabelFrame(root, text="Nuevo Registro")
input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Etiqueta y entrada para monto
monto_label = ttk.Label(input_frame, text="Monto:")
monto_label.grid(row=0, column=0, padx=5, pady=5)
monto_entry = ttk.Entry(input_frame)
monto_entry.grid(row=0, column=1, padx=5, pady=5)

# Etiqueta y combobox para turno
turno_label = ttk.Label(input_frame, text="Turno:")
turno_label.grid(row=1, column=0, padx=5, pady=5)
turno_options = ["Mañana", "Siesta", "Tarde"]
turno_combo = ttk.Combobox(input_frame, values=turno_options)
turno_combo.grid(row=1, column=1, padx=5, pady=5)

# Botón para guardar el registro
guardar_button = ttk.Button(input_frame, text="Guardar", command=guardar_registro)
guardar_button.grid(row=2, columnspan=2, padx=5, pady=5)

# Marco para mostrar los registros
output_frame = ttk.LabelFrame(root, text="Registros Guardados")
output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Árbol para mostrar los registros
columns = ('ID', 'Tipo', 'Categoría', 'Monto', 'Hora', 'Turno')
registros_tree = ttk.Treeview(output_frame, columns=columns, show='headings')
for col in columns:
    registros_tree.heading(col, text=col)
registros_tree.pack(fill=tk.BOTH, expand=True)

# Actualizar la lista al iniciar
actualizar_lista()

# Ejecutar la aplicación
root.mainloop()
