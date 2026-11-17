
from servicio import Servicio
from excepciones import DatosInvalidosError


class Sala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, identificador, nombre, tarifa, capacidad):
        super().__init__(identificador, nombre, tarifa)

        if type(capacidad) is not int or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo.")

        self._capacidad = capacidad

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        if not 0 <= descuento <= 100 or not 0 <= impuesto <= 100:
            raise DatosInvalidosError("Descuento e impuesto deben estar entre 0 y 100.")

        subtotal = self.tarifa * duracion
        subtotal -= subtotal * descuento / 100
        return round(subtotal * (1 + impuesto / 100), 2)

    def describir_servicio(self):
        return f"Sala: {self.nombre} | Capacidad: {self._capacidad} personas"
