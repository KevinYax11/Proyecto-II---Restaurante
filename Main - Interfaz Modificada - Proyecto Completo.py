import tkinter as tk
from tkinter import ttk
from collections import deque
import time
import random

class Cliente:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono

class Pedido:
    def __init__(self, cliente, items, metodo_pago=""):
        self.cliente = cliente
        self.items = items
        self.estado = "pendiente"
        self.total = 0.0
        self.metodo_pago = metodo_pago
        self.hora_entrada = time.strftime("%H:%M:%S")
        self.hora_salida = ""

class Restaurante:
    def __init__(self):
        self.clientes = {}
        self.pedidos = deque()
        self.pedidos_entregados = []
        self.stock = {
            "Cordero en Salsa de Menta": tk.StringVar(value="15"),
            "Filete Mignon": tk.StringVar(value="15"),
            "Carpaccio de Res": tk.StringVar(value="15"),
            "Tournedos Rossini": tk.StringVar(value="15"),
            "Pescado a la Meunière": tk.StringVar(value="15"),
            "Caviar con Blinis": tk.StringVar(value="15"),
            "Vieiras a la Parrilla Con Coliflor": tk.StringVar(value="15"),
            "Pato a la Naranja": tk.StringVar(value="15"),
            "Ravioles de Trufa Negra":tk.StringVar(value="15")
        }
        self.menus = {
            "Cordero en Salsa de Menta": 75.0,
            "Filete Mignon": 105.00,
            "Carpaccio de Res": 55.00,
            "Tournedos Rossini": 83.00,
            "Pescado a la Meunière": 98.00,
            "Caviar con Blinis": 75.00,
            "Vieiras a la Parrilla Con Coliflor": 98.00,
            "Pato a la Naranja": 132.00,
            "Ravioles de Trufa Negra": 105,
        }

    def agregar_cliente(self, nombre, telefono):
        cliente = Cliente(nombre, telefono)
        self.clientes[telefono] = cliente
        print(f"Cliente {nombre} registrado con éxito.")

    def tomar_pedido(self, cliente_telefono, items, metodo_pago):
        if cliente_telefono not in self.clientes:
            print("Cliente no encontrado. Registre al cliente primero.")
            return

        cliente = self.clientes[cliente_telefono]

        for item, cantidad in items.items():
            stock_value = self.stock[item].get()
            if int(stock_value) < cantidad:
                print(f"Lo sentimos, no hay suficiente {item} en stock.")
                return

        total_pedido = sum(self.menus[item] * cantidad for item, cantidad in items.items())

        for item, cantidad in items.items():
            stock_value = self.stock[item].get()
            self.stock[item].set(int(stock_value) - cantidad)

        pedido = Pedido(cliente, items, metodo_pago)
        pedido.total = total_pedido
        self.pedidos.append((cliente_telefono, items, metodo_pago))
        print(f"Pedido de {cliente.nombre}: {items} ha sido tomado. Total a pagar: Q{total_pedido:.2f} ({metodo_pago})")

    def entregar_pedido(self, cliente_telefono, items, metodo_pago):
        if (cliente_telefono, items, metodo_pago) in self.pedidos:
            self.pedidos.remove((cliente_telefono, items, metodo_pago))
            self.pedidos_entregados.append((cliente_telefono, items, metodo_pago, time.strftime("%Y-%m-%d %H:%M:%S")))

class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurante App")
        self.restaurante = Restaurante()
        self.cliente_nombre = tk.StringVar()
        self.cliente_telefono = tk.StringVar()
        self.pedido_producto = tk.StringVar()
        self.pedido_cantidad = tk.StringVar()
        self.metodo_pago = tk.StringVar()
        self.total_pedido_text = tk.StringVar()
        self.total_pedido_text.set("Total del Pedido: Q0.00")

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#007ACC", foreground="white")
        style.configure("TLabel", background="white")
        style.configure("TEntry", fieldbackground="white")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10)

        # Pestaña de Registro de Cliente
        self.tab_registro_cliente = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_registro_cliente, text="Registro de Cliente")

        cliente_label = ttk.Label(self.tab_registro_cliente, text="Registro de Cliente", font=("Helvetica", 16, "bold"))
        cliente_label.pack(pady=10)

        ttk.Label(self.tab_registro_cliente, text="Nombre del Cliente:", font=("Helvetica", 12)).pack()
        self.cliente_nombre_entry = ttk.Entry(self.tab_registro_cliente, textvariable=self.cliente_nombre, font=("Helvetica", 12))
        self.cliente_nombre_entry.pack(pady=5)

        ttk.Label(self.tab_registro_cliente, text="Teléfono del Cliente:", font=("Helvetica", 12)).pack()
        self.cliente_telefono_entry = ttk.Entry(self.tab_registro_cliente, textvariable=self.cliente_telefono, font=("Helvetica", 12))
        self.cliente_telefono_entry.pack(pady=5)

        agregar_cliente_button = ttk.Button(self.tab_registro_cliente, text="Agregar Cliente", command=self.agregar_cliente, style="TButton")
        agregar_cliente_button.pack(pady=10)

        # Pestaña de Tomar Pedido
        self.tab_tomar_pedido = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tomar_pedido, text="Tomar Pedido")

        pedido_label = ttk.Label(self.tab_tomar_pedido, text="Tomar Pedido", font=("Helvetica", 16, "bold"))
        pedido_label.pack(pady=10)

        ttk.Label(self.tab_tomar_pedido, text="Producto:", font=("Helvetica", 12)).pack()
        productos = list(self.restaurante.menus.keys())
        self.pedido_producto.set(productos[0])
        producto_menu = ttk.Combobox(self.tab_tomar_pedido, textvariable=self.pedido_producto, values=productos, font=("Helvetica", 12))
        producto_menu.pack(pady=5)

        ttk.Label(self.tab_tomar_pedido, text="Cantidad:", font=("Helvetica", 12)).pack()
        self.pedido_cantidad_entry = ttk.Entry(self.tab_tomar_pedido, textvariable=self.pedido_cantidad, font=("Helvetica", 12))
        self.pedido_cantidad_entry.pack(pady=5)

        ttk.Label(self.tab_tomar_pedido, text="Método de Pago:", font=("Helvetica", 12)).pack()
        metodo_pago_menu = ttk.Combobox(self.tab_tomar_pedido, textvariable=self.metodo_pago, values=["Efectivo", "Tarjeta"], font=("Helvetica", 12))
        metodo_pago_menu.pack(pady=5)

        tomar_pedido_button = ttk.Button(self.tab_tomar_pedido, text="Tomar Pedido", command=self.tomar_pedido, style="TButton")
        tomar_pedido_button.pack(pady=10)

        total_pedido_label = ttk.Label(self.tab_tomar_pedido, textvariable=self.total_pedido_text, font=("Helvetica", 14, "bold"))
        total_pedido_label.pack()

        # Pestaña de Pedidos Entregados
        self.tab_pedidos_entregados = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pedidos_entregados, text="Pedidos Entregados")

        pedidos_entregados_label = ttk.Label(self.tab_pedidos_entregados, text="Pedidos Entregados", font=("Helvetica", 16, "bold"))
        pedidos_entregados_label.pack(pady=10)

        self.pedidos_entregados_text = tk.Text(self.tab_pedidos_entregados, height=10, width=50)
        self.pedidos_entregados_text.pack(padx=10, pady=10)

        # Pestaña de Modificar Inventario
        self.tab_modificar_inventario = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_modificar_inventario, text="Modificar Inventario")

        inventario_label = ttk.Label(self.tab_modificar_inventario, text="Modificar Inventario", font=("Helvetica", 16, "bold"))
        inventario_label.pack(pady=10)

        ttk.Label(self.tab_modificar_inventario, text="Producto:", font=("Helvetica", 12)).pack()
        self.inventario_producto = tk.StringVar(value=productos[0])
        inventario_producto_menu = ttk.Combobox(self.tab_modificar_inventario, textvariable=self.inventario_producto, values=productos, font=("Helvetica", 12))
        inventario_producto_menu.pack(pady=5)

        ttk.Label(self.tab_modificar_inventario, text="Cantidad A Agregar:", font=("Helvetica", 12)).pack()
        self.inventario_cantidad = ttk.Entry(self.tab_modificar_inventario, font=("Helvetica", 12))
        self.inventario_cantidad.pack(pady=5)

        modificar_inventario_button = ttk.Button(self.tab_modificar_inventario, text="Modificar Inventario", command=self.modificar_inventario, style="TButton")
        modificar_inventario_button.pack(pady=10)

    def agregar_cliente(self):
        nombre = self.cliente_nombre.get()
        telefono = self.cliente_telefono.get()

        if nombre and telefono:
            self.restaurante.agregar_cliente(nombre, telefono)
            self.cliente_nombre.set("")
            self.cliente_telefono.set("")
            self.cliente_actual = telefono
            self.pedidos_cliente_actual = {}

    def tomar_pedido(self):
        producto = self.pedido_producto.get()
        cantidad = int(self.pedido_cantidad.get())
        metodo_pago = self.metodo_pago.get()

        if producto and cantidad > 0 and self.cliente_actual:
            if producto in self.restaurante.menus:
                pedido = {producto: cantidad}
                total_pedido = sum(self.restaurante.menus[item] * cantidad for item, cantidad in pedido.items())
                self.total_pedido_text.set(f"Total del Pedido: Q {total_pedido:.2f}")
                self.restaurante.tomar_pedido(self.cliente_actual, pedido, metodo_pago)
                time.sleep(random.randint(1, 5))
                self.entregar_pedido(self.cliente_actual, pedido, metodo_pago)

    def entregar_pedido(self, cliente_telefono, items, metodo_pago):
        self.restaurante.entregar_pedido(cliente_telefono, items, metodo_pago)
        self.mostrar_pedidos_entregados()

    def mostrar_pedidos_entregados(self):
        self.pedidos_entregados_text.delete(1.0, tk.END)
        for cliente_telefono, items, metodo_pago, fecha_entrega in self.restaurante.pedidos_entregados:
            total_pedido = sum(self.restaurante.menus[item] * cantidad for item, cantidad in items.items())
            mensaje = f"Pedido A: {self.restaurante.clientes[cliente_telefono].nombre}"
            mensaje += f"\nTeléfono Cliente: {cliente_telefono})"
            mensaje += f"\nFecha de entrega: {fecha_entrega}\n"

            # Itera sobre los elementos del pedido y agrega información detallada
            for item, cantidad in items.items():
                mensaje += f"Plato Seleccionado: {item} \nCantidad De Platillos: {cantidad}\n"

            mensaje += f"Total del Pedido: Q {total_pedido:.2f}"
            mensaje += f"\nMetodo De Pago:{metodo_pago}"
            mensaje += f"\nPedido Entregado"
            mensaje += "\n------------------------\n"

            self.pedidos_entregados_text.insert(tk.END, mensaje)

    def modificar_inventario(self):
        producto = self.inventario_producto.get()
        cantidad = int(self.inventario_cantidad.get())

        if producto in self.restaurante.stock and cantidad != 0:
            stock_value = self.restaurante.stock[producto].get()
            self.restaurante.stock[producto].set(int(stock_value) + cantidad)
            mensaje = f"Inventario de {producto} actualizado: {int(stock_value) + cantidad}"
            print(mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()
