
"""
UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
Curso: Programación - 213023
Fase 4: Prácticas simuladas

Proyecto: Sistema Integral de Gestión de Clientes,
Servicios y Reservas - Software FJ.

Archivo: main.py

Descripción:
Este módulo integra las clases del sistema y permite
gestionar clientes, servicios y reservas mediante un
menú interactivo de consola.

Se aplican principios de programación orientada a
objetos, validaciones y manejo de excepciones.

La información se almacena temporalmente en memoria,
sin utilizar bases de datos.
"""

# ======================================================
# 1. IMPORTACIÓN DE CLASES Y EXCEPCIONES
# ======================================================

# Clase encargada de representar a los clientes.
from cliente import Cliente

# Clases que representan los servicios disponibles.
from sala import Sala
from equipo import Equipo
from asesoria import Asesoria

# Excepciones personalizadas utilizadas por el sistema.
from excepciones import ErrorSoftwareFJ, DatosInvalidosError

# Importamos la clase Reserva desarrollada en el proyecto.
from reserva import Reserva


# ======================================================
# 2. CLASE PRINCIPAL DEL SISTEMA
# ======================================================

class SistemaSoftwareFJ:
    """
    Coordina las operaciones de Software FJ.

    Gestiona clientes, servicios y reservas mediante
    diccionarios que almacenan objetos en memoria.

    También permite buscar registros, calcular costos
    y controlar identificadores duplicados.
    """

    def __init__(self):
        """
        Inicializa las colecciones del sistema.

        Cada diccionario utiliza identificadores únicos
        como claves para localizar los objetos.
        """

        # Almacena los clientes registrados.
        self.clientes = {}

        # Almacena las salas, equipos y asesorías.
        self.servicios = {}

        # Almacena las reservas realizadas.
        self.reservas = {}

    # --------------------------------------------------
    # 3. GESTIÓN DE CLIENTES
    # --------------------------------------------------

    def registrar_cliente(
        self, identificador, nombre, correo, telefono
    ):
        """
        Registra un nuevo cliente.

        Parámetros:
            identificador: Código único del cliente.
            nombre: Nombre completo.
            correo: Dirección de correo electrónico.
            telefono: Número de contacto.

        Retorna:
            Objeto Cliente registrado.

        Excepciones:
            DatosInvalidosError si el identificador
            está repetido o los datos no son válidos.
        """

        # Comprobamos que el cliente no esté registrado.
        if identificador in self.clientes:
            raise DatosInvalidosError(
                "Ya existe un cliente con ese identificador."
            )

        # Creamos el objeto utilizando la clase Cliente.
        # Las validaciones internas se ejecutan al crearlo.
        cliente = Cliente(
            identificador, nombre, correo, telefono
        )

        # Almacenamos el cliente con su identificador.
        self.clientes[cliente.identificador] = cliente

        return cliente

    # --------------------------------------------------
    # 4. GESTIÓN DE SERVICIOS
    # --------------------------------------------------

    def registrar_sala(
        self, identificador, nombre, tarifa, capacidad
    ):
        """
        Registra una sala disponible para reservas.

        Parámetros:
            identificador: Código único.
            nombre: Nombre de la sala.
            tarifa: Precio por hora.
            capacidad: Número máximo de personas.
        """

        # Creamos el objeto Sala.
        sala = Sala(
            identificador, nombre, tarifa, capacidad
        )

        # Guardamos el servicio y retornamos el objeto.
        return self._agregar_servicio(sala)

    def registrar_equipo(
        self, identificador, nombre, tarifa, tipo
    ):
        """
        Registra un equipo disponible para alquiler.

        Parámetros:
            identificador: Código único.
            nombre: Nombre del equipo.
            tarifa: Precio por hora.
            tipo: Categoría del equipo.
        """

        equipo = Equipo(
            identificador, nombre, tarifa, tipo
        )

        return self._agregar_servicio(equipo)

    def registrar_asesoria(
        self, identificador, nombre, tarifa, especialidad
    ):
        """
        Registra un servicio de asesoría especializada.

        Parámetros:
            identificador: Código único.
            nombre: Nombre de la asesoría.
            tarifa: Precio por hora.
            especialidad: Área de conocimiento.
        """

        asesoria = Asesoria(
            identificador, nombre, tarifa, especialidad
        )

        return self._agregar_servicio(asesoria)

    def _agregar_servicio(self, servicio):
        """
        Almacena un servicio previamente creado.

        Impide registrar servicios con identificadores
        repetidos.

        Se aplica polimorfismo porque este método puede
        recibir objetos Sala, Equipo o Asesoria.
        """

        if servicio.identificador in self.servicios:
            raise DatosInvalidosError(
                "Ya existe un servicio con ese identificador."
            )

        self.servicios[servicio.identificador] = servicio

        return servicio

    # --------------------------------------------------
    # 5. CÁLCULO DE COSTOS
    # --------------------------------------------------

    def calcular_costo(
        self, id_servicio, duracion,
        descuento=0, impuesto=0
    ):
        """
        Calcula el valor de un servicio.

        Parámetros:
            id_servicio: Identificador del servicio.
            duracion: Cantidad de horas.
            descuento: Porcentaje de descuento.
            impuesto: Porcentaje de impuesto.

        Retorna:
            Costo calculado del servicio.

        Los parámetros opcionales permiten simular
        diferentes variantes de cálculo de costos.
        """

        # Buscamos el servicio solicitado.
        servicio = self._obtener(
            self.servicios, id_servicio, "Servicio"
        )

        # Cada clase de servicio ejecuta su propia
        # implementación del método calcular_costo.
        # Esto demuestra polimorfismo.
        return servicio.calcular_costo(
            duracion, descuento, impuesto
        )

    # --------------------------------------------------
    # 6. GESTIÓN DE RESERVAS
    # --------------------------------------------------

    def crear_reserva(
        self, identificador, id_cliente,
        id_servicio, duracion
    ):
        """
        Crea una reserva asociada a un cliente.

        Parámetros:
            identificador: Código único de la reserva.
            id_cliente: Identificador del cliente.
            id_servicio: Identificador del servicio.
            duracion: Duración de la reserva en horas.

        Retorna:
            Objeto Reserva creado.

        La reserva comienza con estado Pendiente.
        """

        # Evitamos identificadores duplicados.
        if identificador in self.reservas:
            raise DatosInvalidosError(
                "Ya existe una reserva con ese identificador."
            )

        # Verificamos que el cliente exista.
        cliente = self._obtener(
            self.clientes, id_cliente, "Cliente"
        )

        # Verificamos que el servicio exista.
        servicio = self._obtener(
            self.servicios, id_servicio, "Servicio"
        )

        # Validamos la duración y disponibilidad.
        servicio.validar_parametros(duracion)

        # Creamos la reserva según el constructor
        # implementado en reserva.py.
        reserva = Reserva(
            cliente, servicio, duracion
        )

        # Guardamos el identificador en el diccionario
        # principal, sin modificar la clase Reserva.
        self.reservas[identificador] = reserva

        return reserva

    def confirmar_reserva(self, identificador):
        """
        Confirma una reserva existente.

        Parámetro:
            identificador: Código de la reserva.
        """

        # Recuperamos la reserva solicitada.
        reserva = self._obtener(
            self.reservas, identificador, "Reserva"
        )

        # Ejecutamos el método de la clase Reserva.
        return reserva.confirmar()

    def cancelar_reserva(self, identificador):
        """
        Cancela una reserva existente.

        Parámetro:
            identificador: Código de la reserva.
        """

        reserva = self._obtener(
            self.reservas, identificador, "Reserva"
        )

        return reserva.cancelar()

    # --------------------------------------------------
    # 7. BÚSQUEDA Y VALIDACIÓN DE REGISTROS
    # --------------------------------------------------

    @staticmethod
    def _obtener(coleccion, identificador, tipo):
        """
        Busca un elemento dentro de un diccionario.

        Parámetros:
            coleccion: Diccionario donde buscar.
            identificador: Clave del elemento.
            tipo: Nombre del tipo de registro.

        Retorna:
            Objeto encontrado.

        Utiliza encadenamiento de excepciones para
        convertir KeyError en DatosInvalidosError.
        """

        try:
            # Intentamos recuperar el objeto.
            return coleccion[identificador]

        except KeyError as error:
            # Transformamos el error original en una
            # excepción personalizada del sistema.
            raise DatosInvalidosError(
                f"{tipo} no encontrado: {identificador}"
            ) from error


# ======================================================
# 8. FUNCIONES AUXILIARES DE LA CONSOLA
# ======================================================

def solicitar_numero(texto, entero=False):
    """
    Solicita un valor numérico al usuario.

    Si entero es verdadero, convierte a int.
    En caso contrario, convierte a float.

    Cuando la conversión falla, genera una excepción
    personalizada en lugar de cerrar la aplicación.
    """

    valor = input(texto).strip()

    try:
        if entero:
            return int(valor)

        return float(valor)

    except ValueError as error:
        raise DatosInvalidosError(
            "Debes escribir un número válido."
        ) from error


def mostrar_menu():
    """
    Presenta las opciones disponibles del sistema.
    """

    print("\n" + "=" * 55)
    print("       SOFTWARE FJ - SISTEMA DE GESTIÓN")
    print("=" * 55)

    print("1. Registrar cliente")
    print("2. Registrar sala")
    print("3. Registrar equipo")
    print("4. Registrar asesoría")
    print("5. Mostrar clientes y servicios")
    print("6. Calcular costo de servicio")
    print("7. Crear reserva")
    print("8. Confirmar reserva")
    print("9. Cancelar reserva")
    print("10. Mostrar reservas")
    print("0. Salir")


# ======================================================
# 9. EJECUCIÓN DE LAS OPCIONES
# ======================================================

def ejecutar_opcion(sistema, opcion):
    """
    Ejecuta la operación seleccionada por el usuario.

    Recibe:
        sistema: Instancia de SistemaSoftwareFJ.
        opcion: Opción elegida desde el menú.
    """

    # OPCIÓN 1: REGISTRAR CLIENTE
    if opcion == "1":

        identificador = input("ID: ").strip()
        nombre = input("Nombre: ").strip()
        correo = input("Correo: ").strip()
        telefono = input("Teléfono: ").strip()

        cliente = sistema.registrar_cliente(
            identificador, nombre, correo, telefono
        )

        print("Cliente registrado:", cliente.nombre)

    # OPCIONES 2, 3 Y 4: REGISTRAR SERVICIOS
    elif opcion in ("2", "3", "4"):

        identificador = input(
            "ID del servicio: "
        ).strip()

        nombre = input(
            "Nombre del servicio: "
        ).strip()

        tarifa = solicitar_numero(
            "Tarifa por hora: "
        )

        if opcion == "2":

            capacidad = solicitar_numero(
                "Capacidad: ", entero=True
            )

            servicio = sistema.registrar_sala(
                identificador, nombre, tarifa, capacidad
            )

        elif opcion == "3":

            tipo = input(
                "Tipo de equipo: "
            ).strip()

            servicio = sistema.registrar_equipo(
                identificador, nombre, tarifa, tipo
            )

        else:

            especialidad = input(
                "Especialidad: "
            ).strip()

            servicio = sistema.registrar_asesoria(
                identificador, nombre,
                tarifa, especialidad
            )

        print(
            "Servicio registrado:",
            servicio.describir_servicio()
        )

    # OPCIÓN 5: CONSULTAR CLIENTES Y SERVICIOS
    elif opcion == "5":

        print("\nCLIENTES REGISTRADOS")

        for cliente in sistema.clientes.values():
            print(cliente.mostrar_informacion())
            print("---")

        print("\nSERVICIOS REGISTRADOS")

        for servicio in sistema.servicios.values():
            print(servicio.describir_servicio())

    # OPCIÓN 6: CALCULAR COSTOS
    elif opcion == "6":

        identificador = input(
            "ID del servicio: "
        ).strip()

        duracion = solicitar_numero(
            "Duración (horas): "
        )

        descuento = solicitar_numero(
            "Descuento (%; 0 si no aplica): "
        )

        impuesto = solicitar_numero(
            "Impuesto (%; 0 si no aplica): "
        )

        costo = sistema.calcular_costo(
            identificador,
            duracion,
            descuento,
            impuesto
        )

        print(f"Costo: ${costo:,.2f}")

    # OPCIÓN 7: CREAR RESERVA
    elif opcion == "7":

        identificador = input(
            "ID reserva: "
        ).strip()

        id_cliente = input(
            "ID cliente: "
        ).strip()

        id_servicio = input(
            "ID servicio: "
        ).strip()

        duracion = solicitar_numero(
            "Duración (horas): "
        )

        reserva = sistema.crear_reserva(
            identificador,
            id_cliente,
            id_servicio,
            duracion
        )

        print(
            "Reserva creada con estado:",
            reserva.estado
        )

    # OPCIÓN 8: CONFIRMAR RESERVA
    elif opcion == "8":

        identificador = input(
            "ID reserva: "
        ).strip()

        sistema.confirmar_reserva(identificador)

        print("Reserva confirmada.")

    # OPCIÓN 9: CANCELAR RESERVA
    elif opcion == "9":

        identificador = input(
            "ID reserva: "
        ).strip()

        sistema.cancelar_reserva(identificador)

        print("Reserva cancelada.")

    # OPCIÓN 10: MOSTRAR RESERVAS
    elif opcion == "10":

        print("\nRESERVAS REGISTRADAS")

        for identificador, reserva in sistema.reservas.items():
            print(
                f"{identificador}: {reserva.estado}"
            )

    # CONTROL DE OPCIONES NO RECONOCIDAS
    else:
        print("Opción no reconocida.")


# ======================================================
# 10. FUNCIÓN PRINCIPAL DE LA APLICACIÓN
# ======================================================

def main():
    """
    Inicia el sistema y mantiene activo el menú.

    Usa manejo de excepciones para evitar que los
    errores de operación terminen la ejecución.
    """

    # Creamos la instancia principal del sistema.
    sistema = SistemaSoftwareFJ()

    # Ciclo que mantiene el programa en ejecución.
    while True:

        try:
            # Mostramos el menú de operaciones.
            mostrar_menu()

            # Recibimos la opción del usuario.
            opcion = input(
                "Selecciona una opción: "
            ).strip()

            # Finalizamos cuando el usuario elige 0.
            if opcion == "0":
                print("Hasta pronto.")
                break

            # Ejecutamos la operación solicitada.
            ejecutar_opcion(sistema, opcion)

        except (
            ErrorSoftwareFJ,
            ValueError,
            TypeError
        ) as error:

            # Capturamos errores controlados y
            # mantenemos la aplicación activa.
            # El registro en archivo se integrará
            # con el módulo de logs del grupo.
            print("Operación rechazada:", error)

        except (KeyboardInterrupt, EOFError):

            # Permite finalizar ordenadamente cuando
            # se interrumpe la entrada de consola.
            print("\nSesión finalizada.")
            break


# ======================================================
# 11. PUNTO DE ENTRADA DEL PROGRAMA
# ======================================================

# Ejecuta el menú solamente cuando este archivo se
# inicia directamente. Al importarlo desde pruebas.py,
# no se ejecuta automáticamente el menú.

if __name__ == "__main__":
    main()
