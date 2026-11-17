
from sala import Sala
from equipo import Equipo
from asesoria import Asesoria

servicios = [
    Sala("S001", "Sala de reuniones", 50000, 10),
    Equipo("E001", "Portátil Dell", 20000, "Computador"),
    Asesoria("A001", "Asesoría Python", 80000, "Programación")
]

for servicio in servicios:
    print(servicio.describir_servicio())
    print(f"Costo por 2 horas: ${servicio.calcular_costo(2):,.0f}")
    print("-" * 40)
