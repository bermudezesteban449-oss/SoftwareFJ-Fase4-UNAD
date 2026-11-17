
from cliente import Cliente
from excepciones import DatosInvalidosError

try:
    cliente = Cliente(
        "C001",
        "Juan Esteban",
        "esteban@correo.com",
        "3001234567"
    )

    print("CLIENTE REGISTRADO CORRECTAMENTE")
    print(cliente.mostrar_informacion())

except DatosInvalidosError as error:
    print(f"ERROR: {error}")

