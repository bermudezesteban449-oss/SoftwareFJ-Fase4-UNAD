from cliente import Cliente
from servicio import Servicio
from excepciones import (
    DatosInvalidosError,
    ReservaInvalidaError,
    ServicioNoDisponibleError
)


class Reserva:
    """Representa una reserva de un cliente para un servicio."""

    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "Debe proporcionar un cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "Debe proporcionar un servicio válido."
            )

        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise DatosInvalidosError(
                "La duración debe ser mayor que cero."
            )

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        self._estado = "Confirmada"

    def cancelar(self):
        self._estado = "Cancelada"

    def procesar(self):
        try:
            costo = self._servicio.calcular_costo(
                self._duracion
            )

        except ServicioNoDisponibleError as error:
            self.cancelar()
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva."
            ) from error

        else:
            self.confirmar()
            return costo

        finally:
            print(
                f"Reserva procesada. Estado: {self._estado}"
            )

    def mostrar_informacion(self):
        return (
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Duración: {self.duracion}\n"
            f"Estado: {self.estado}"
        )