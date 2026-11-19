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

# ==========================================
# APORTE DE SEBASTIAN AGUDELO - FASE 4
# CONTINUACION DEL SISTEMA DE RESERVAS
# ==========================================

from datetime import datetime, timedelta
from math import isfinite
from threading import RLock
from registro_logs import registrar_evento, registrar_error


class ReservaAvanzada(Reserva):
    """Amplia las funciones de reserva de Software FJ."""

    # Lista para almacenar las reservas avanzadas.
    _registro_reservas = []

    # Evita conflictos al confirmar reservas.
    _bloqueo = RLock()

    @staticmethod
    def _numero_valido(valor):
        """Comprueba que un numero sea valido."""
        return type(valor) in (int, float) and (
            type(valor) is int or isfinite(valor)
        )

    def __init__(
        self, cliente, servicio, duracion, fecha_inicio=None
    ):
        try:
            # Validar que la duracion sea positiva.
            if (
                not self._numero_valido(duracion)
                or duracion <= 0
            ):
                raise DatosInvalidosError(
                    "La duracion debe ser un numero positivo."
                )

            # Conservar el constructor original.
            super().__init__(cliente, servicio, duracion)

            # Convertir la fecha cuando sea texto.
            if isinstance(fecha_inicio, str):
                try:
                    fecha_inicio = datetime.fromisoformat(
                        fecha_inicio.strip()
                    )
                except ValueError as error:
                    raise DatosInvalidosError(
                        "Fecha invalida. Use AAAA-MM-DD HH:MM."
                    ) from error

            # Validar la fecha de inicio.
            if fecha_inicio is not None:

                if (
                    not isinstance(fecha_inicio, datetime)
                    or fecha_inicio.tzinfo is not None
                ):
                    raise DatosInvalidosError(
                        "La fecha debe ser local y valida."
                    )

                if fecha_inicio <= datetime.now():
                    raise DatosInvalidosError(
                        "La fecha de inicio debe ser futura."
                    )

                try:
                    fecha_fin = fecha_inicio + timedelta(
                        hours=duracion
                    )
                except (OverflowError, ValueError) as error:
                    raise DatosInvalidosError(
                        "La duracion genera una fecha invalida."
                    ) from error

            else:
                fecha_fin = None

            # Guardar los datos adicionales.
            self._fecha_inicio = fecha_inicio
            self._fecha_fin = fecha_fin
            self._costo_total = None

            # Registrar la reserva en memoria.
            with self._bloqueo:
                self._registro_reservas.append(self)

            registrar_evento(
                f"Reserva creada: "
                f"{servicio.identificador} - Pendiente"
            )

        except (
            DatosInvalidosError,
            ReservaInvalidaError
        ) as error:

            registrar_error(
                f"Error al crear reserva: {error}"
            )
            raise

    @property
    def costo_total(self):
        """Devuelve el costo total de la reserva."""
        return self._costo_total

    @staticmethod
    def _validar_porcentaje(valor, nombre):
        """Valida los descuentos y los impuestos."""

        if (
            not ReservaAvanzada._numero_valido(valor)
            or not 0 <= valor <= 100
        ):
            raise DatosInvalidosError(
                f"El {nombre} debe estar entre 0 y 100."
            )

    def esta_disponible(self):
        """Verifica la disponibilidad del servicio."""

        with self._bloqueo:

            # Revisar si el servicio esta disponible.
            if not self.servicio.disponible:
                return False

            # Identificar el servicio actual.
            clave_actual = (
                type(self.servicio),
                self.servicio.identificador
            )

            # Revisar las reservas existentes.
            for otra in self._registro_reservas:

                if (
                    otra is self
                    or otra.estado != "Confirmada"
                ):
                    continue

                clave_otra = (
                    type(otra.servicio),
                    otra.servicio.identificador
                )

                # Solo comparar el mismo servicio.
                if clave_actual != clave_otra:
                    continue

                # Sin horario, bloquear otra reserva activa.
                if (
                    self._fecha_inicio is None
                    or otra._fecha_inicio is None
                ):
                    return False

                # Verificar cruces de horarios.
                if (
                    self._fecha_inicio < otra._fecha_fin
                    and otra._fecha_inicio < self._fecha_fin
                ):
                    return False

            return True

    def confirmar(self, descuento=0, impuesto=0):
        """Confirma una reserva y calcula su precio."""

        try:
            with self._bloqueo:

                # Validar el estado de la reserva.
                if self.estado != "Pendiente":
                    raise ReservaInvalidaError(
                        "Solo se pueden confirmar "
                        "reservas pendientes."
                    )

                # Validar descuento e impuesto.
                self._validar_porcentaje(
                    descuento, "descuento"
                )

                self._validar_porcentaje(
                    impuesto, "impuesto"
                )

                # Comprobar que la fecha no haya pasado.
                if (
                    self._fecha_inicio is not None
                    and self._fecha_inicio <= datetime.now()
                ):
                    raise ReservaInvalidaError(
                        "La fecha de la reserva ya paso."
                    )

                # Comprobar disponibilidad.
                if not self.esta_disponible():
                    raise ServicioNoDisponibleError(
                        "El servicio no esta disponible."
                    )

                # Validar los parametros del servicio.
                self.servicio.validar_parametros(
                    self.duracion
                )

                # Aplicar polimorfismo.
                # Cada servicio calcula su propio costo.
                costo = self.servicio.calcular_costo(
                    self.duracion,
                    descuento,
                    impuesto
                )

                # Comprobar el resultado del calculo.
                if (
                    not self._numero_valido(costo)
                    or costo < 0
                ):
                    raise ReservaInvalidaError(
                        "El costo calculado es invalido."
                    )

                # Utilizar el metodo original del compañero.
                super().confirmar()

                # Guardar el precio final.
                self._costo_total = round(costo, 2)

                # Registrar la confirmacion.
                registrar_evento(
                    f"Reserva confirmada: "
                    f"{self.servicio.identificador}, "
                    f"total {self._costo_total}"
                )

                return self._costo_total

        except (
            DatosInvalidosError,
            ReservaInvalidaError,
            ServicioNoDisponibleError
        ) as error:

            registrar_error(
                f"Error al confirmar reserva: {error}"
            )
            raise

        except Exception as error:

            registrar_error(
                f"Error inesperado al confirmar: {error}"
            )

            raise ReservaInvalidaError(
                "No fue posible confirmar la reserva."
            ) from error

    def cancelar(self):
        """Cancela una reserva y libera el servicio."""

        with self._bloqueo:

            # Evitar cancelar dos veces.
            if self.estado == "Cancelada":

                registrar_error(
                    "Se intento cancelar una reserva cancelada."
                )

                raise ReservaInvalidaError(
                    "La reserva ya estaba cancelada."
                )

            # Utilizar el metodo original.
            super().cancelar()

            # Registrar la cancelacion.
            registrar_evento(
                f"Reserva cancelada: "
                f"{self.servicio.identificador}"
            )

            return True

    def procesar(self, descuento=0, impuesto=0):
        """Procesa la reserva con manejo de excepciones."""

        try:
            # Intentar confirmar la reserva.
            costo = self.confirmar(
                descuento,
                impuesto
            )

        except ServicioNoDisponibleError as error:

            # Cancelar si el servicio no esta disponible.
            self.cancelar()

            # Encadenamiento de excepciones.
            raise ReservaInvalidaError(
                "No se pudo procesar: "
                "servicio no disponible."
            ) from error

        else:
            # Devolver el costo si todo salio bien.
            return costo

        finally:
            # Registrar el estado final.
            registrar_evento(
                f"Proceso finalizado. "
                f"Estado: {self.estado}"
            )

    def mostrar_informacion(self):
        """Muestra los datos originales y adicionales."""

        # Mostrar la fecha de inicio.
        if self._fecha_inicio is not None:
            fecha = self._fecha_inicio.strftime(
                "%Y-%m-%d %H:%M"
            )
        else:
            fecha = "No especificada"

        # Mostrar el costo total.
        if self._costo_total is not None:
            total = f"${self._costo_total:,.2f}"
        else:
            total = "Pendiente"

        # Reutilizar el metodo del compañero.
        return (
            super().mostrar_informacion()
            + f"\nFecha de inicio: {fecha}"
            + f"\nCosto total: {total}"
        )


# ==========================================
# FIN DEL APORTE DE SEBASTIAN AGUDELO
# ==========================================
