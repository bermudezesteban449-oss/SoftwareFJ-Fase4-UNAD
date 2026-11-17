
from abc import abstractmethod
from entidad import Entidad
from excepciones import DatosInvalidosError, ServicioNoDisponibleError


class Servicio(Entidad):
    """Clase abstracta para todos los servicios de Software FJ."""

    def __init__(self, identificador, nombre, tarifa, disponible=True):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")

        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero.")

        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadera o falsa.")

        self._nombre = nombre.strip()
        self._tarifa = tarifa
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadera o falsa.")
        self._disponible = disponible

    def validar_parametros(self, duracion):
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise DatosInvalidosError("La duración debe ser mayor que cero.")

        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre} no está disponible."
            )

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def mostrar_informacion(self):
        return self.describir_servicio()
