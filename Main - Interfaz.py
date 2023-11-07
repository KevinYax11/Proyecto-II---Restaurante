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
            "Cordero en Salsa de Menta": 15,
            "Filete Mignon": 15,
            "Carpaccio de Res": 15,
            "Tournedos Rossini": 15,
            "Pescado a la Meunière": 15,
            "Caviar con Blinis": 15,
            "Vieiras a la Parrilla Con Coliflor": 15,
            "Pato a la Naranja": 15,
            "Ravioles de Trufa Negra": 15,}

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
            if item in self.stock and cantidad > self.stock[item]:
                print(f"Lo sentimos, no hay suficiente {item} en stock.")
                return

        total_pedido = sum(self.menus[item] * cantidad for item, cantidad in items.items())

        for item, cantidad in items.items():
            self.stock[item] -= cantidad

        pedido = Pedido(cliente, items, metodo_pago)
        pedido.total = total_pedido
        self.pedidos.append((cliente_telefono, items, metodo_pago))
        print(f"Pedido de {cliente.nombre}: {items} ha sido tomado. Total a pagar: Q{total_pedido:.2f} ({metodo_pago})")

    def entregar_pedido(self, cliente_telefono, items, metodo_pago):
        if (cliente_telefono, items, metodo_pago) in self.pedidos:
            self.pedidos.remove((cliente_telefono, items, metodo_pago))
            self.pedidos_entregados.append((cliente_telefono, items, metodo_pago))

class Cantidad(Restaurante):
    def __init__(self, cantidad):
        super(self, cantidad).__init__
        print(self.stock)
class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurante App")
        self.restaurante = Restaurante()
        self.cliente_nombre = tk.StringVar()
        self.cliente_telefono = tk.StringVar()
        self.pedido_producto = tk.StringVar()
        self.pedido_cantidad = tk.StringVar()
        self.metodo_pago = tk.StringVar()  # Opción para seleccionar el método de pago en la toma de pedidos
        self.total_pedido_text = tk.StringVar()
        self.total_pedido_text.set("Total del Pedido: Q0.00")

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#007ACC", foreground="white")
        style.configure("TLabel", background="white")
        style.configure("TEntry", fieldbackground="white")

        cliente_label = ttk.Label(root, text="Registro de Cliente", font=("Helvetica", 16, "bold"))
        cliente_label.pack(pady=10)

        ttk.Label(root, text="Nombre del Cliente:", font=("Helvetica", 12)).pack()
        self.cliente_nombre_entry = ttk.Entry(root, textvariable=self.cliente_nombre, font=("Helvetica", 12))
        self.cliente_nombre_entry.pack(pady=5)



        ttk.Label(root, text="Teléfono del Cliente:", font=("Helvetica", 12)).pack()
        self.cliente_telefono_entry = ttk.Entry(root, textvariable=self.cliente_telefono, font=("Helvetica", 12))
        self.cliente_telefono_entry.pack(pady=5)

        agregar_cliente_button = ttk.Button(root, text="Agregar Cliente", command=self.agregar_cliente, style="TButton")
        agregar_cliente_button.pack(pady=10)

        pedido_label = ttk.Label(root, text="Tomar Pedido", font=("Helvetica", 16, "bold"))
        pedido_label.pack(pady=10)

        ttk.Label(root, text="Producto:", font=("Helvetica", 12)).pack()
        productos = list(self.restaurante.menus.keys())
        self.pedido_producto.set(productos[0])
        producto_menu = ttk.Combobox(root, textvariable=self.pedido_producto, values=productos, font=("Helvetica", 12))
        producto_menu.pack(pady=5)

        ttk.Label(root, text="Cantidad:", font=("Helvetica", 12)).pack()
        self.pedido_cantidad_entry = ttk.Entry(root, textvariable=self.pedido_cantidad, font=("Helvetica", 12))
        self.pedido_cantidad_entry.pack(pady=5)

        ttk.Label(root, text="Método de Pago:", font=("Helvetica", 12)).pack()
        self.metodo_pago.set("Efectivo")
        metodo_pago_menu = ttk.Combobox(root, textvariable=self.metodo_pago, values=["Efectivo", "Tarjeta"], font=("Helvetica", 12))
        metodo_pago_menu.pack(pady=5)

        tomar_pedido_button = ttk.Button(root, text="Tomar Pedido", command=self.tomar_pedido, style="TButton")
        tomar_pedido_button.pack(pady=10)

        total_pedido_label = ttk.Label(root, textvariable=self.total_pedido_text, font=("Helvetica", 14, "bold"))
        total_pedido_label.pack()

        self.mensaje_registro_label = ttk.Label(root, text="", font=("Helvetica", 12))
        self.mensaje_registro_label.pack()

        entregados_label = ttk.Label(root, text="Pedidos Entregados", font=("Helvetica", 16, "bold"))
        entregados_label.pack(pady=10)

        self.pedidos_entregados_text = tk.Text(root, wrap=tk.WORD, width=50, height=10, font=("Helvetica", 12))
        self.pedidos_entregados_text.pack()

    def agregar_cliente(self):
        nombre = self.cliente_nombre.get()
        telefono = self.cliente_telefono.get()

        if nombre and telefono:
            self.restaurante.agregar_cliente(nombre, telefono)
            self.cliente_nombre.set("")
            self.cliente_telefono.set("")
            self.cliente_actual = telefono
            self.pedidos_cliente_actual = {}

            mensaje = f"Cliente {nombre} registrado con éxito."
            self.mensaje_registro_label.config(text=mensaje)

    def tomar_pedido(self):
        producto = self.pedido_producto.get()
        cantidad = int(self.pedido_cantidad.get())
        metodo_pago = self.metodo_pago.get()

        if producto and cantidad > 0 and self.cliente_actual:
            if producto in self.restaurante.menus:
                pedido = {producto: cantidad}
                self.restaurante.tomar_pedido(self.cliente_actual, pedido, metodo_pago)
                time.sleep(random.randint(1, 5))
                self.entregar_pedido(self.cliente_actual, pedido, metodo_pago)

    def entregar_pedido(self, cliente_telefono, items, metodo_pago):
        self.restaurante.entregar_pedido(cliente_telefono, items, metodo_pago)
        self.mostrar_pedidos_entregados()

    def mostrar_pedidos_entregados(self):
        self.pedidos_entregados_text.delete(1.0, tk.END)
        for cliente_telefono, items, metodo_pago in self.restaurante.pedidos_entregados:
            total_pedido = sum(self.restaurante.menus[item] * cantidad for item, cantidad in items.items())
            mensaje = f"Cliente {self.restaurante.clientes[cliente_telefono].nombre}"
            mensaje += f"Numero De Telefono Cliente,({cliente_telefono}):\n"
            mensaje += "\n".join([f"{item}: {cantidad}" for item, cantidad in items.items()])
            mensaje += f"\nTotal del Pedido: Q{total_pedido:.2f} ({metodo_pago})"
            mensaje += "\n----------------\n"
            self.pedidos_entregados_text.insert(tk.END, mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()
