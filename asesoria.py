
from servicio import Servicio
from excepciones import DatosInvalidosError


class Asesoria(Servicio):
    """Servicio de asesorías especializadas."""

    def __init__(self, identificador, nombre, tarifa, especialidad):
        super().__init__(identificador, nombre, tarifa)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("Debe indicar la especialidad.")

        self._especialidad = especialidad.strip()

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        if not 0 <= descuento <= 100 or not 0 <= impuesto <= 100:
            raise DatosInvalidosError("Descuento e impuesto deben estar entre 0 y 100.")

        subtotal = self.tarifa * duracion
        subtotal -= subtotal * descuento / 100
        return round(subtotal * (1 + impuesto / 100), 2)

    def describir_servicio(self):
        return f"Asesoría: {self.nombre} | Especialidad: {self._especialidad}"

