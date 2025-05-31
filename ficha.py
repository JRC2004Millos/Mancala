class Ficha:
    def __init__(self, cantidad=1):
        self.cantidad = cantidad

    def agregar(self, cantidad: int):
        self.cantidad += cantidad

    def remover(self):
        cantidad_removida = self.cantidad
        self.cantidad = 0
        return cantidad_removida

    def getCantidad(self):
        return self.cantidad
