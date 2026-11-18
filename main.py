"""Interfaz de consola y coordinación del Sistema Software FJ.

Responsabilidad de integración: no redefine las clases de dominio de compañeros.
Contrato acordado con reserva.py:
    Reserva(identificador, cliente, servicio, duracion)
    .confirmar(), .cancelar(), .procesar()
    .estado (propiedad)
La implementación de Reserva corresponde a otra integrante del grupo.
"""

from cliente import Cliente
from sala import Sala
from equipo import Equipo
from asesoria import Asesoria
from excepciones import ErrorSoftwareFJ, DatosInvalidosError

try:
    from reserva import Reserva
except ImportError:
    Reserva = None


class SistemaSoftwareFJ:
    """Mantiene colecciones en memoria; no utiliza bases de datos."""

    def __init__(self):
        self.clientes = {}
        self.servicios = {}
        self.reservas = {}

    def registrar_cliente(self, identificador, nombre, correo, telefono):
        if identificador in self.clientes:
            raise DatosInvalidosError('Ya existe un cliente con ese identificador.')
        cliente = Cliente(identificador, nombre, correo, telefono)
        self.clientes[cliente.identificador] = cliente
        return cliente

    def registrar_sala(self, identificador, nombre, tarifa, capacidad):
        return self._agregar_servicio(Sala(identificador, nombre, tarifa, capacidad))

    def registrar_equipo(self, identificador, nombre, tarifa, tipo):
        return self._agregar_servicio(Equipo(identificador, nombre, tarifa, tipo))

    def registrar_asesoria(self, identificador, nombre, tarifa, especialidad):
        return self._agregar_servicio(Asesoria(identificador, nombre, tarifa, especialidad))

    def _agregar_servicio(self, servicio):
        if servicio.identificador in self.servicios:
            raise DatosInvalidosError('Ya existe un servicio con ese identificador.')
        self.servicios[servicio.identificador] = servicio
        return servicio

    def calcular_costo(self, id_servicio, duracion, descuento=0, impuesto=0):
        servicio = self._obtener(self.servicios, id_servicio, 'Servicio')
        return servicio.calcular_costo(duracion, descuento, impuesto)

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion):
        if Reserva is None:
            raise ErrorSoftwareFJ('Falta integrar reserva.py de la compañera.')
        if identificador in self.reservas:
            raise DatosInvalidosError('Ya existe una reserva con ese identificador.')
        cliente = self._obtener(self.clientes, id_cliente, 'Cliente')
        servicio = self._obtener(self.servicios, id_servicio, 'Servicio')
        # La compañera valida duración/disponibilidad también dentro de Reserva.
        servicio.validar_parametros(duracion)
        reserva = Reserva(cliente, servicio, duracion)
        self.reservas[identificador] = reserva
        return reserva

    def confirmar_reserva(self, identificador):
        reserva = self._obtener(self.reservas, identificador, 'Reserva')
        return reserva.confirmar()

    def cancelar_reserva(self, identificador):
        reserva = self._obtener(self.reservas, identificador, 'Reserva')
        return reserva.cancelar()

    @staticmethod
    def _obtener(coleccion, identificador, tipo):
        try:
            return coleccion[identificador]
        except KeyError as exc:
            raise DatosInvalidosError(f'{tipo} no encontrado: {identificador}') from exc


def solicitar_numero(texto, entero=False):
    valor = input(texto).strip()
    try:
        return int(valor) if entero else float(valor)
    except ValueError as exc:
        raise DatosInvalidosError('Debes escribir un número válido.') from exc


def mostrar_menu():
    print('\n=== SOFTWARE FJ | Gestión de clientes, servicios y reservas ===')
    print('1. Registrar cliente')
    print('2. Registrar sala')
    print('3. Registrar equipo')
    print('4. Registrar asesoría')
    print('5. Mostrar clientes y servicios')
    print('6. Calcular costo de servicio')
    print('7. Crear reserva')
    print('8. Confirmar reserva')
    print('9. Cancelar reserva')
    print('10. Mostrar reservas')
    print('0. Salir')


def ejecutar_opcion(sistema, opcion):
    if opcion == '1':
        cliente = sistema.registrar_cliente(input('ID: ').strip(), input('Nombre: ').strip(),
                                            input('Correo: ').strip(), input('Teléfono: ').strip())
        print('Cliente registrado:', cliente.nombre)
    elif opcion in ('2', '3', '4'):
        identificador = input('ID del servicio: ').strip()
        nombre = input('Nombre del servicio: ').strip()
        tarifa = solicitar_numero('Tarifa por hora: ')
        if opcion == '2':
            servicio = sistema.registrar_sala(identificador, nombre, tarifa,
                                              solicitar_numero('Capacidad: ', entero=True))
        elif opcion == '3':
            servicio = sistema.registrar_equipo(identificador, nombre, tarifa,
                                                input('Tipo de equipo: ').strip())
        else:
            servicio = sistema.registrar_asesoria(identificador, nombre, tarifa,
                                                  input('Especialidad: ').strip())
        print('Servicio registrado:', servicio.describir_servicio())
    elif opcion == '5':
        print('\nCLIENTES')
        for cliente in sistema.clientes.values():
            print(cliente.mostrar_informacion(), '\n---')
        print('\nSERVICIOS')
        for servicio in sistema.servicios.values():
            print(servicio.describir_servicio())
    elif opcion == '6':
        identificador = input('ID del servicio: ').strip()
        duracion = solicitar_numero('Duración (horas): ')
        descuento = solicitar_numero('Descuento (%; 0 si no aplica): ')
        impuesto = solicitar_numero('Impuesto (%; 0 si no aplica): ')
        print(f'Costo: ${sistema.calcular_costo(identificador, duracion, descuento, impuesto):,.2f}')
    elif opcion == '7':
        reserva = sistema.crear_reserva(input('ID reserva: ').strip(),
                                       input('ID cliente: ').strip(),
                                       input('ID servicio: ').strip(),
                                       solicitar_numero('Duración (horas): '))
        print('Reserva creada con estado:', reserva.estado)
    elif opcion == '8':
        sistema.confirmar_reserva(input('ID reserva: ').strip())
        print('Reserva confirmada.')
    elif opcion == '9':
        sistema.cancelar_reserva(input('ID reserva: ').strip())
        print('Reserva cancelada.')
    elif opcion == '10':
        for identificador, reserva in sistema.reservas.items():
            print(f'{identificador}: {reserva.estado}')
    else:
        print('Opción no reconocida.')


def main():
    sistema = SistemaSoftwareFJ()
    while True:
        try:
            mostrar_menu()
            opcion = input('Selecciona una opción: ').strip()
            if opcion == '0':
                print('Hasta pronto.')
                break
            ejecutar_opcion(sistema, opcion)
        except (ErrorSoftwareFJ, ValueError, TypeError) as exc:
            # La compañera de logs debe conectar aquí el registro en archivo.
            print('Operación rechazada:', exc)
        except (KeyboardInterrupt, EOFError):
            print('\nSesión finalizada.')
            break


if __name__ == '__main__':
    main()
