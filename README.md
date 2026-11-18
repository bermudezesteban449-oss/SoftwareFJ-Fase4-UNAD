# Software FJ — Fase 4 (UNAD)

Sistema integral de gestión de clientes, servicios y reservas, desarrollado en Python para el componente práctico de Programación (213023).

## Objetivo

Aplicar abstracción, herencia, polimorfismo, encapsulación y manejo avanzado de excepciones. Los datos de clientes, servicios y reservas permanecen en memoria; **no se usa base de datos**.

## Requisitos

- Python 3.10 o superior (recomendación del equipo; verificar la versión instalada).
- Archivos del proyecto en la misma carpeta: `main.py`, `cliente.py`, `entidad.py`, `servicio.py`, `sala.py`, `equipo.py`, `asesoria.py`, `reserva.py`, `excepciones.py`, `registro_logs.py` y `pruebas.py`.
- No se requieren librerías externas para la interfaz de consola.

## Cómo ejecutar

En la terminal, desde la carpeta del proyecto:

```powershell
python main.py
```

Para las diez operaciones de verificación:

```powershell
python pruebas.py
```

## Funciones del programa

Registrar clientes; registrar salas, equipos y asesorías; visualizar clientes y servicios; calcular costos; crear, confirmar, cancelar y consultar reservas.

## Integración pendiente con los compañeros

El programa principal **espera** que `reserva.py` defina `Reserva(identificador, cliente, servicio, duracion)`, la propiedad `estado` y los métodos `confirmar()`, `cancelar()` y `procesar()`. Si la clase de la compañera utiliza otros nombres o parámetros, se debe ajustar la integración en `main.py` antes de dar el proyecto por terminado.

La compañera responsable de las excepciones conectará el registro de eventos y errores en `registro_logs.py`. Quedan por verificar `try/except/else`, `try/except/finally`, encadenamiento de excepciones y los requisitos del Anexo 3.

## Trabajo colaborativo

Cada integrante debe trabajar desde su cuenta y registrar aportes propios en GitHub. Antes de empezar se recomienda `git pull origin main` y, de ser posible, usar ramas y solicitudes de incorporación (*pull requests*).

## Evidencia grupal

Según la guía de la Fase 4, se entrega un PDF con portada, introducción, enlace al repositorio de GitHub, conclusiones y referencias en normas APA.
