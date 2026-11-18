"""Diez operaciones de prueba para Software FJ.

Ejecutar desde la raíz del repositorio: python pruebas.py
No utiliza bases de datos ni altera datos persistentes.
"""
from main import SistemaSoftwareFJ
from excepciones import ErrorSoftwareFJ


def ejecutar():
    sistema = SistemaSoftwareFJ()
    resultados = []

    def verificar(numero, descripcion, accion, debe_fallar=False):
        try:
            accion()
        except (ErrorSoftwareFJ, ValueError, TypeError, AssertionError) as exc:
            correcto = debe_fallar
            detalle = f'error controlado: {exc}'
        else:
            correcto = not debe_fallar
            detalle = 'operación aceptada'
        resultados.append(correcto)
        print(f'{numero:02}. {"OK" if correcto else "FALLO"} | {descripcion} | {detalle}')

    verificar(1, 'Cliente válido',
             lambda: sistema.registrar_cliente('C001', 'Ana Pérez', 'ana@correo.com', '3001234567'))
    verificar(2, 'Cliente inválido',
             lambda: sistema.registrar_cliente('C002', '', 'correo-invalido', '123'), True)
    verificar(3, 'Sala válida',
             lambda: sistema.registrar_sala('S001', 'Sala A', 50000, 8))
    verificar(4, 'Equipo válido',
             lambda: sistema.registrar_equipo('E001', 'Portátil', 20000, 'Computador'))
    verificar(5, 'Asesoría válida',
             lambda: sistema.registrar_asesoria('A001', 'Python', 80000, 'Programación'))
    verificar(6, 'Servicio con tarifa inválida',
             lambda: sistema.registrar_sala('S002', 'Sala B', -100, 5), True)
    verificar(7, 'Cálculo de costo correcto',
             lambda: _verificar_costo(sistema))
    verificar(8, 'Cálculo con duración inválida',
             lambda: sistema.calcular_costo('S001', -2), True)
    verificar(9, 'Reserva exitosa',
             lambda: sistema.crear_reserva('R001', 'C001', 'S001', 2))
    verificar(10, 'Reserva fallida (cliente inexistente)',
             lambda: sistema.crear_reserva('R002', 'NO_EXISTE', 'S001', 2), True)

    total = sum(resultados)
    print(f'\nResultado: {total}/{len(resultados)} operaciones conforme a lo esperado')
    if total != len(resultados):
        print('Revisa las operaciones marcadas FALLO y la integración de reserva.py.')
    return total == len(resultados)


def _verificar_costo(sistema):
    costo = sistema.calcular_costo('S001', 2, 10, 0)
    if costo != 90000:
        raise AssertionError(f'Se esperaban $90,000 y se obtuvo ${costo}')


if __name__ == '__main__':
    raise SystemExit(0 if ejecutar() else 1)
