import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QMovie
import time

class Cliente:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono

class Pedido:
    def __init__(self, cliente, items, metodo_pago=""):
        self.cliente = cliente
        self.items = items
        self.estado = "Pendiente"
        self.total = 0.0
        self.metodo_pago = metodo_pago
        self.hora_entrada = time.strftime("%H:%M:%S")
        self.hora_salida = ""

class Restaurante:
    def __init__(self):
        self.clientes = {}
        self.pedidos = []
        self.stock = {
            "Cordero en Salsa de Menta": 15,
            "Filete Mignon": 15,
            "Carpaccio de Res": 15,
            "Tournedos Rossini": 15,
            "Pescado a la Meunière": 15,
            "Caviar con Blinis": 15,
            "Vieiras a la Parrilla Con Coliflor": 15,
            "Pato a la Naranja": 15,
            "Ravioles de Trufa Negra": 15
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
            "Ravioles de Trufa Negra": 105
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
            stock_value = self.stock.get(item, 0)
            if stock_value < cantidad:
                print(f"Lo sentimos, no hay suficiente {item} en stock.")
                return

        total_pedido = sum(self.menus[item] * cantidad for item, cantidad in items.items())

        for item, cantidad in items.items():
            self.stock[item] -= cantidad

        pedido = Pedido(cliente, items, metodo_pago)
        pedido.total = total_pedido
        self.pedidos.append(pedido)
        print(f"Pedido de {cliente.nombre}: {items} ha sido tomado. Total a pagar: Q{total_pedido:.2f} ({metodo_pago})")

    def entregar_pedido(self, index):
        if 0 <= index < len(self.pedidos) and self.pedidos[index].estado == "Pendiente":
            self.pedidos[index].estado = "Entregado"
            self.pedidos[index].hora_salida = time.strftime("%H:%M:%S")

class RestauranteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Taverna Greca")
        self.setGeometry(100, 100, 850, 800)

        gif_label = QLabel(self)
        gif_movie = QMovie("Logo.gif")  # Reemplace con la ruta de su GIF
        gif_movie.start()
        gif_label.setMovie(gif_movie)

        # Ajustar automáticamente el tamaño del gif al tamaño de la ventana
        gif_label.setGeometry(0, 0, self.width(), self.height())
        gif_label.setScaledContents(True)

        self.cliente_nombre_label = QLabel("Nombre del Cliente:", self)
        self.cliente_nombre_label.move(20, 20)

        self.cliente_nombre_input = QLineEdit(self)
        self.cliente_nombre_input.move(160, 20)

        self.cliente_telefono_label = QLabel("Teléfono del Cliente:", self)
        self.cliente_telefono_label.move(20, 60)

        self.cliente_telefono_input = QLineEdit(self)
        self.cliente_telefono_input.move(160, 60)

        self.agregar_cliente_button = QPushButton("Agregar Cliente", self)
        self.agregar_cliente_button.move(20, 100)

        self.clientes_label = QLabel("Clientes Registrados:", self)
        self.clientes_label.move(20, 140)

        self.clientes_list = QTableWidget(self)
        self.clientes_list.setColumnCount(2)
        self.clientes_list.setHorizontalHeaderLabels(["Nombre", "Teléfono"])
        self.clientes_list.setGeometry(20, 170, 300, 150)

        self.tomar_pedido_label = QLabel("Tomar Pedido", self)
        self.tomar_pedido_label.move(350, 20)

        self.menu_label = QLabel("Menú", self)
        self.menu_label.move(350, 60)

        self.menu_combo = QComboBox(self)
        for item, precio in restaurante.menus.items():
            self.menu_combo.addItem(f"{item} - Q{precio:.2f}")
        self.menu_combo.setGeometry(350, 90, 200, 30)

        self.cantidad_label = QLabel("Cantidad:", self)
        self.cantidad_label.move(350, 140)

        self.cantidad_input = QLineEdit(self)
        self.cantidad_input.move(450, 140)

        self.metodo_pago_label = QLabel("Método de Pago:", self)
        self.metodo_pago_label.move(350, 180)

        self.metodo_pago_combo = QComboBox(self)
        self.metodo_pago_combo.addItems(["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito"])
        self.metodo_pago_combo.setGeometry(470, 180, 180, 30)

        self.tomar_pedido_button = QPushButton("Tomar Pedido", self)
        self.tomar_pedido_button.move(350, 220)

        self.pedidos_label = QLabel("Pendientes:", self)
        self.pedidos_label.move(350, 260)

        self.pedidos_list = QTableWidget(self)
        self.pedidos_list.setColumnCount(5)
        self.pedidos_list.setHorizontalHeaderLabels(["Cliente", "Pedido", "Método de Pago", "Estado", "Total"])
        self.pedidos_list.setGeometry(350, 290, 400, 150)

        self.entregar_pedido_button = QPushButton("Entregar Pedido", self)
        self.entregar_pedido_button.move(350, 470)

        self.entregados_label = QLabel("Entregados:", self)
        self.entregados_label.move(350, 500)

        self.entregados_list = QTableWidget(self)
        self.entregados_list.setColumnCount(5)
        self.entregados_list.setHorizontalHeaderLabels(["Cliente", "Pedido", "Método de Pago", "Estado", "Total"])
        self.entregados_list.setGeometry(350, 530, 400, 150)

        self.agregar_cliente_button.clicked.connect(self.agregar_cliente)
        self.tomar_pedido_button.clicked.connect(self.tomar_pedido)
        self.entregar_pedido_button.clicked.connect(self.entregar_pedido)

    def agregar_cliente(self):
        nombre = self.cliente_nombre_input.text()
        telefono = self.cliente_telefono_input.text()
        restaurante.agregar_cliente(nombre, telefono)
        self.clientes_list.insertRow(self.clientes_list.rowCount())
        self.clientes_list.setItem(self.clientes_list.rowCount() - 1, 0, QTableWidgetItem(nombre))
        self.clientes_list.setItem(self.clientes_list.rowCount() - 1, 1, QTableWidgetItem(str(telefono)))

    def tomar_pedido(self):
        cliente_telefono = self.cliente_telefono_input.text()
        selected_item = self.menu_combo.currentText().split(" - ")
        item = selected_item[0]
        precio = float(selected_item[1][1:])
        cantidad = int(self.cantidad_input.text())
        metodo_pago = self.metodo_pago_combo.currentText()
        restaurante.tomar_pedido(cliente_telefono, {item: cantidad}, metodo_pago)

        self.pedidos_list.insertRow(self.pedidos_list.rowCount())
        self.pedidos_list.setItem(self.pedidos_list.rowCount() - 1, 0, QTableWidgetItem(cliente_telefono))
        self.pedidos_list.setItem(self.pedidos_list.rowCount() - 1, 1, QTableWidgetItem(f"{item} ({cantidad})"))
        self.pedidos_list.setItem(self.pedidos_list.rowCount() - 1, 2, QTableWidgetItem(metodo_pago))
        self.pedidos_list.setItem(self.pedidos_list.rowCount() - 1, 3, QTableWidgetItem("Pendiente"))
        total = cantidad * precio
        self.pedidos_list.setItem(self.pedidos_list.rowCount() - 1, 4, QTableWidgetItem(f"Q{total:.2f}"))

    def entregar_pedido(self):
        row = self.pedidos_list.currentRow()
        if row >= 0:
            restaurante.entregar_pedido(row)
            self.actualizar_listas()

    def actualizar_listas(self):
        self.pedidos_list.setRowCount(len(restaurante.pedidos))
        self.entregados_list.setRowCount(len([pedido for pedido in restaurante.pedidos if pedido.estado == "Entregado"]))

        for i, pedido in enumerate(restaurante.pedidos):
            self.pedidos_list.setItem(i, 0, QTableWidgetItem(pedido.cliente.telefono))
            items = " ".join([f"{item} ({cantidad})" for item, cantidad in pedido.items.items()])
            self.pedidos_list.setItem(i, 1, QTableWidgetItem(items))
            self.pedidos_list.setItem(i, 2, QTableWidgetItem(pedido.metodo_pago))
            self.pedidos_list.setItem(i, 3, QTableWidgetItem(pedido.estado))
            total = sum(restaurante.menus[item] * cantidad for item, cantidad in pedido.items.items())
            self.pedidos_list.setItem(i, 4, QTableWidgetItem(f"Q{total:.2f}"))

        j = 0
        for i, pedido in enumerate(restaurante.pedidos):
            if pedido.estado == "Entregado":
                self.entregados_list.setItem(j, 0, QTableWidgetItem(pedido.cliente.telefono))
                items = " ".join([f"{item} ({cantidad})" for item, cantidad in pedido.items.items()])
                self.entregados_list.setItem(j, 1, QTableWidgetItem(items))
                self.entregados_list.setItem(j, 2, QTableWidgetItem(pedido.metodo_pago))
                self.entregados_list.setItem(j, 3, QTableWidgetItem(pedido.estado))
                total = sum(restaurante.menus[item] * cantidad for item, cantidad in pedido.items.items())
                self.entregados_list.setItem(j, 4, QTableWidgetItem(f"Q{total:.2f}"))
                j += 1


app = QApplication(sys.argv)
restaurante = Restaurante()
window = RestauranteApp()
window.show()
sys.exit(app.exec_())
