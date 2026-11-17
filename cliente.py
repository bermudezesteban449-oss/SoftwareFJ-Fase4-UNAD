
import re

from entidad import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):
    """Representa un cliente de Software FJ."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del cliente no puede estar vacío."
            )

        if not isinstance(correo, str) or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", correo.strip()
        ):
            raise DatosInvalidosError(
                "El correo electrónico no es válido."
            )

        if not isinstance(telefono, str) or not telefono.isdigit():
            raise DatosInvalidosError(
                "El teléfono debe contener solamente números."
            )

        self._nombre = nombre.strip()
        self._correo = correo.strip()
        self._telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    def mostrar_informacion(self):
        return (
            f"ID: {self.identificador}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}"
        )
