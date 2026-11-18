
from sala import Sala
from equipo import Equipo
from asesoria import Asesoria
from cliente import Cliente 
from reserva import Reserva
from excepciones import DatosInvalidosError
from registro_logs import registrar_evento, registrar_error

servicios = [
    Sala("S001", "Sala de reuniones", 50000, 10),
    Equipo("E001", "Portátil Dell", 20000, "Computador"),
    Asesoria("A001", "Asesoría Python", 80000, "Programación")
]

for servicio in servicios:
    print(servicio.describir_servicio())
    print(f"Costo por 2 horas: ${servicio.calcular_costo(2):,.0f}")
    print("-" * 40)
#prueba de reserva

cliente = Cliente(
    "c001",
    "Natalia Giraldo",
    "natalia@gmail.com",
    "3001234567"
)

reserva = Reserva(
    cliente,
    servicios[0],
    2
)

print("\n=== prueba de Reserva ===")
print(reserva.mostrar_informacion())

costo = reserva.procesar()

print(f"costo total: ${costo:,.0f}")
print(f"estado: {reserva.estado}")

registrar_evento("prueba de reserva ejecutada correctamente.")

print("\n=== prueba de error cliente ===")

try:
  Cliente(
        "C002",
        "",
        "correo",
        "abc"

    )

except DatosInvalidosError as error:
    registrar_error(str(error))
    print("Error detectado:", error)

print("\n=== PRUEBA SERVICIO NO DISPONIBLE ===")

try:
    sala_error = Sala(
        "S002",
        "Sala Ejecutiva",
        50000,
        20
    )

    sala_error.cambiar_disponibilidad(False)

    sala_error.calcular_costo(2)

except Exception as error:
    registrar_error(str(error))
    print("Error detectado:", error)

