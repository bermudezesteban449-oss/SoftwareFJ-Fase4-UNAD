
# Excepciones personalizadas del sistema Software FJ

class ErrorSoftwareFJ(Exception):
    """Excepción general del sistema."""
    pass


class DatosInvalidosError(ErrorSoftwareFJ):
    """Se produce cuando los datos no son válidos."""
    pass


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se produce cuando un servicio no está disponible."""
    pass


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se produce cuando una reserva es incorrecta."""
    pass
