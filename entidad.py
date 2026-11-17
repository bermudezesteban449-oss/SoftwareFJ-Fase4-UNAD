
from abc import ABC, abstractmethod

from excepciones import DatosInvalidosError


class Entidad(ABC):
    """Clase abstracta general del sistema."""

    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError(
                "El identificador debe ser un texto no vacío."
            )

        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        """Devuelve la información de la entidad."""
        pass
