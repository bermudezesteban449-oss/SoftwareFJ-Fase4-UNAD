
from servicio import Servicio
from excepciones import DatosInvalidosError


class Equipo(Servicio):
    """Servicio de alquiler de equipos."""

    def __init__(self, identificador, nombre, tarifa, tipo_equipo):
        super().__init__(identificador, nombre, tarifa)

        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise DatosInvalidosError("Debe indicar el tipo de equipo.")

        self._tipo_equipo = tipo_equipo.strip()

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        if not 0 <= descuento <= 100 or not 0 <= impuesto <= 100:
            raise DatosInvalidosError("Descuento e impuesto deben estar entre 0 y 100.")

        subtotal = self.tarifa * duracion
        subtotal -= subtotal * descuento / 100
        return round(subtotal * (1 + impuesto / 100), 2)

    def describir_servicio(self):
        return f"Alquiler: {self.nombre} | Tipo: {self._tipo_equipo}"

