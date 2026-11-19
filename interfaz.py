"""
UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
Curso: Programación - 213023
Fase 4: Prácticas simuladas

Proyecto: Sistema Integral de Gestión de Clientes,
Servicios y Reservas - Software FJ.

Archivo: interfaz.py

Descripción:
Interfaz gráfica (Tkinter) del sistema. Reutiliza la clase
SistemaSoftwareFJ de main.py y registra eventos y errores
con las funciones de registro_logs.py.

Para ejecutarla: python interfaz.py
"""

# ======================================================
# 1. IMPORTACIONES
# ======================================================

# Librería estándar de Python para crear ventanas.
import tkinter as tk

# ttk trae widgets con aspecto más limpio; messagebox muestra avisos.
from tkinter import ttk, messagebox

# Cuadro de texto con barra de desplazamiento (para ver los logs).
from tkinter.scrolledtext import ScrolledText

# Os se usa para comprobar si el archivo de logs existe.
import os

# Clase con toda la lógica del sistema (clientes, servicios, reservas).
from main import SistemaSoftwareFJ

# Excepciones personalizadas del proyecto.
from excepciones import ErrorSoftwareFJ, DatosInvalidosError

# Funciones del grupo para escribir en el archivo de logs.
from registro_logs import registrar_evento, registrar_error

# Nombre del archivo donde registro_logs.py guarda los registros.
ARCHIVO_LOGS = "eventos.log"


# ======================================================
# 2. FUNCIONES AUXILIARES
# ======================================================

def leer_numero(texto, entero=False):
    """Convierte el texto de un cuadro a número.

    Si no se puede convertir, lanza DatosInvalidosError
    (encadenando el ValueError original).
    """
    # Quitamos espacios al inicio y al final.
    texto = texto.strip()
    try:
        # Si se pide entero, usamos int; si no, float.
        return int(texto) if entero else float(texto)
    except ValueError as error:
        # Convertimos el error en uno propio del sistema.
        raise DatosInvalidosError(
            "Debes escribir un número válido."
        ) from error


def ejecutar_seguro(accion, ventana=None):
    """Ejecuta una acción sin que la aplicación se cierre.

    Retorna una tupla (exito, resultado).
    Si hay error: lo registra en el log y muestra un aviso.
    """
    try:
        # Intentamos ejecutar la acción recibida.
        resultado = accion()
    except (ErrorSoftwareFJ, ValueError, TypeError) as error:
        # Errores controlados: se guardan en el log.
        registrar_error(f"{type(error).__name__}: {error}")
        # Se avisa al usuario con una ventanita.
        messagebox.showerror(
            "Operación rechazada", str(error), parent=ventana
        )
        return False, None
    except Exception as error:
        # Cualquier otro error inesperado tampoco cierra el programa.
        registrar_error(f"Error inesperado - {type(error).__name__}: {error}")
        messagebox.showerror(
            "Error inesperado", str(error), parent=ventana
        )
        return False, None
    else:
        # Si todo salió bien, devolvemos éxito y el resultado.
        return True, resultado


def crear_campo(padre, texto, fila):
    """Crea una etiqueta y un cuadro de texto en la fila indicada."""
    # Etiqueta a la izquierda.
    ttk.Label(padre, text=texto).grid(
        row=fila, column=0, sticky="e", padx=5, pady=4
    )
    # Cuadro de texto a la derecha.
    entrada = ttk.Entry(padre, width=30)
    entrada.grid(row=fila, column=1, padx=5, pady=4)
    return entrada


# ======================================================
# 3. VENTANA DE CLIENTES
# ======================================================

class VentanaClientes(tk.Toplevel):
    """Ventana para registrar y listar clientes."""

    def __init__(self, principal, sistema):
        super().__init__(principal)
        self.sistema = sistema
        self.title("Clientes")
        self.resizable(False, False)

        # Marco del formulario.
        formulario = ttk.Frame(self, padding=10)
        formulario.pack()

        # Cuadros de texto del cliente.
        self.e_id = crear_campo(formulario, "ID:", 0)
        self.e_nombre = crear_campo(formulario, "Nombre:", 1)
        self.e_correo = crear_campo(formulario, "Correo:", 2)
        self.e_telefono = crear_campo(formulario, "Teléfono:", 3)

        # Botón que dispara el registro.
        ttk.Button(
            formulario, text="Registrar", command=self.registrar
        ).grid(row=4, column=0, columnspan=2, pady=8)

        # Tabla con los clientes registrados.
        self.tabla = ttk.Treeview(
            self, columns=("id", "nombre", "correo", "telefono"),
            show="headings", height=7
        )
        for columna, titulo in (
            ("id", "ID"), ("nombre", "Nombre"),
            ("correo", "Correo"), ("telefono", "Teléfono"),
        ):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=120)
        self.tabla.pack(padx=10, pady=(0, 10))

        # Mostramos los clientes que ya existan.
        self.refrescar()

    def registrar(self):
        """Lee los cuadros y registra el cliente."""
        ok, cliente = ejecutar_seguro(
            lambda: self.sistema.registrar_cliente(
                self.e_id.get().strip(),
                self.e_nombre.get().strip(),
                self.e_correo.get().strip(),
                self.e_telefono.get().strip(),
            ),
            self,
        )
        if ok:
            # Guardamos el evento en el log.
            registrar_evento(f"Cliente registrado: {cliente.identificador}")
            # Limpiamos los cuadros.
            for entrada in (self.e_id, self.e_nombre,
                            self.e_correo, self.e_telefono):
                entrada.delete(0, tk.END)
            self.refrescar()

    def refrescar(self):
        """Vuelve a llenar la tabla con los clientes actuales."""
        self.tabla.delete(*self.tabla.get_children())
        for c in self.sistema.clientes.values():
            self.tabla.insert(
                "", tk.END,
                values=(c.identificador, c.nombre, c.correo, c.telefono)
            )


# ======================================================
# 4. VENTANA DE SERVICIOS
# ======================================================

class VentanaServicios(tk.Toplevel):
    """Ventana para registrar salas, equipos y asesorías."""

    # Texto del último campo según el tipo de servicio.
    ETIQUETAS = {
        "Sala": "Capacidad:",
        "Equipo": "Tipo de equipo:",
        "Asesoría": "Especialidad:",
    }

    def __init__(self, principal, sistema):
        super().__init__(principal)
        self.sistema = sistema
        self.title("Servicios")
        self.resizable(False, False)

        formulario = ttk.Frame(self, padding=10)
        formulario.pack()

        # Selector del tipo de servicio.
        ttk.Label(formulario, text="Tipo:").grid(
            row=0, column=0, sticky="e", padx=5, pady=4
        )
        self.tipo = ttk.Combobox(
            formulario, values=list(self.ETIQUETAS),
            state="readonly", width=27
        )
        self.tipo.current(0)
        self.tipo.grid(row=0, column=1, padx=5, pady=4)
        # Cuando cambia el tipo, cambia la etiqueta del último campo.
        self.tipo.bind("<<ComboboxSelected>>", self.cambiar_etiqueta)

        # Campos comunes a los tres servicios.
        self.e_id = crear_campo(formulario, "ID:", 1)
        self.e_nombre = crear_campo(formulario, "Nombre:", 2)
        self.e_tarifa = crear_campo(formulario, "Tarifa por hora:", 3)

        # Campo especial que depende del tipo.
        self.lbl_extra = ttk.Label(formulario, text="Capacidad:")
        self.lbl_extra.grid(row=4, column=0, sticky="e", padx=5, pady=4)
        self.e_extra = ttk.Entry(formulario, width=30)
        self.e_extra.grid(row=4, column=1, padx=5, pady=4)

        ttk.Button(
            formulario, text="Registrar", command=self.registrar
        ).grid(row=5, column=0, columnspan=2, pady=8)

        # Tabla con los servicios registrados.
        self.tabla = ttk.Treeview(
            self, columns=("id", "descripcion"),
            show="headings", height=7
        )
        self.tabla.heading("id", text="ID")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.column("id", width=80)
        self.tabla.column("descripcion", width=380)
        self.tabla.pack(padx=10, pady=(0, 10))

        self.refrescar()

    def cambiar_etiqueta(self, _evento=None):
        """Actualiza el texto del último campo según el tipo."""
        self.lbl_extra.config(text=self.ETIQUETAS[self.tipo.get()])

    def registrar(self):
        """Crea el servicio según el tipo elegido."""
        def accion():
            tipo = self.tipo.get()
            identificador = self.e_id.get().strip()
            nombre = self.e_nombre.get().strip()
            tarifa = leer_numero(self.e_tarifa.get())
            extra = self.e_extra.get().strip()

            if tipo == "Sala":
                # La capacidad debe ser un número entero.
                return self.sistema.registrar_sala(
                    identificador, nombre, tarifa,
                    leer_numero(extra, entero=True)
                )
            if tipo == "Equipo":
                return self.sistema.registrar_equipo(
                    identificador, nombre, tarifa, extra
                )
            return self.sistema.registrar_asesoria(
                identificador, nombre, tarifa, extra
            )

        ok, servicio = ejecutar_seguro(accion, self)
        if ok:
            registrar_evento(f"Servicio registrado: {servicio.identificador}")
            for entrada in (self.e_id, self.e_nombre,
                            self.e_tarifa, self.e_extra):
                entrada.delete(0, tk.END)
            self.refrescar()

    def refrescar(self):
        """Vuelve a llenar la tabla de servicios."""
        self.tabla.delete(*self.tabla.get_children())
        for s in self.sistema.servicios.values():
            # describir_servicio es polimórfico: cada clase responde distinto.
            self.tabla.insert(
                "", tk.END,
                values=(s.identificador, s.describir_servicio())
            )


# ======================================================
# 5. VENTANA DE CÁLCULO DE COSTOS
# ======================================================

class VentanaCosto(tk.Toplevel):
    """Ventana para calcular el costo de un servicio."""

    def __init__(self, principal, sistema):
        super().__init__(principal)
        self.sistema = sistema
        self.title("Calcular costo")
        self.resizable(False, False)

        formulario = ttk.Frame(self, padding=10)
        formulario.pack()

        # Lista desplegable con los servicios existentes.
        ttk.Label(formulario, text="Servicio:").grid(
            row=0, column=0, sticky="e", padx=5, pady=4
        )
        self.servicio = ttk.Combobox(
            formulario, values=list(sistema.servicios.keys()),
            state="readonly", width=27
        )
        self.servicio.grid(row=0, column=1, padx=5, pady=4)

        self.e_duracion = crear_campo(formulario, "Duración (horas):", 1)
        self.e_descuento = crear_campo(formulario, "Descuento (%):", 2)
        self.e_impuesto = crear_campo(formulario, "Impuesto (%):", 3)
        # Valores por defecto cuando no aplican.
        self.e_descuento.insert(0, "0")
        self.e_impuesto.insert(0, "0")

        ttk.Button(
            formulario, text="Calcular", command=self.calcular
        ).grid(row=4, column=0, columnspan=2, pady=8)

        # Etiqueta donde se muestra el resultado.
        self.resultado = ttk.Label(formulario, text="Costo: -")
        self.resultado.grid(row=5, column=0, columnspan=2)

    def calcular(self):
        """Calcula y muestra el costo."""
        ok, costo = ejecutar_seguro(
            lambda: self.sistema.calcular_costo(
                self.servicio.get(),
                leer_numero(self.e_duracion.get()),
                leer_numero(self.e_descuento.get()),
                leer_numero(self.e_impuesto.get()),
            ),
            self,
        )
        if ok:
            self.resultado.config(text=f"Costo: ${costo:,.2f}")
            registrar_evento(
                f"Costo calculado para {self.servicio.get()}: {costo}"
            )


# ======================================================
# 6. VENTANA DE RESERVAS
# ======================================================

class VentanaReservas(tk.Toplevel):
    """Ventana para crear, confirmar y cancelar reservas."""

    def __init__(self, principal, sistema):
        super().__init__(principal)
        self.sistema = sistema
        self.title("Reservas")
        self.resizable(False, False)

        formulario = ttk.Frame(self, padding=10)
        formulario.pack()

        self.e_id = crear_campo(formulario, "ID reserva:", 0)

        # Listas desplegables de clientes y servicios.
        ttk.Label(formulario, text="Cliente:").grid(
            row=1, column=0, sticky="e", padx=5, pady=4
        )
        self.cliente = ttk.Combobox(
            formulario, values=list(sistema.clientes.keys()),
            state="readonly", width=27
        )
        self.cliente.grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(formulario, text="Servicio:").grid(
            row=2, column=0, sticky="e", padx=5, pady=4
        )
        self.servicio = ttk.Combobox(
            formulario, values=list(sistema.servicios.keys()),
            state="readonly", width=27
        )
        self.servicio.grid(row=2, column=1, padx=5, pady=4)

        self.e_duracion = crear_campo(formulario, "Duración (horas):", 3)

        ttk.Button(
            formulario, text="Crear reserva", command=self.crear
        ).grid(row=4, column=0, columnspan=2, pady=8)

        # Tabla de reservas.
        self.tabla = ttk.Treeview(
            self, columns=("id", "estado"), show="headings", height=7
        )
        self.tabla.heading("id", text="ID reserva")
        self.tabla.heading("estado", text="Estado")
        self.tabla.column("id", width=180)
        self.tabla.column("estado", width=180)
        self.tabla.pack(padx=10)

        # Botones para cambiar el estado de la reserva seleccionada.
        botones = ttk.Frame(self, padding=10)
        botones.pack()
        ttk.Button(
            botones, text="Confirmar", command=self.confirmar
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            botones, text="Cancelar", command=self.cancelar
        ).pack(side=tk.LEFT, padx=5)

        self.refrescar()

    def crear(self):
        """Crea una reserva nueva con los datos del formulario."""
        ok, reserva = ejecutar_seguro(
            lambda: self.sistema.crear_reserva(
                self.e_id.get().strip(),
                self.cliente.get(),
                self.servicio.get(),
                leer_numero(self.e_duracion.get()),
            ),
            self,
        )
        if ok:
            registrar_evento(f"Reserva creada: {self.e_id.get().strip()}")
            self.e_id.delete(0, tk.END)
            self.e_duracion.delete(0, tk.END)
            self.refrescar()

    def _seleccionada(self):
        """Devuelve el ID de la reserva elegida en la tabla."""
        seleccion = self.tabla.selection()
        if not seleccion:
            # Si no eligió ninguna, lanzamos un error del sistema.
            raise DatosInvalidosError("Selecciona una reserva de la lista.")
        return self.tabla.item(seleccion[0])["values"][0]

    def confirmar(self):
        """Confirma la reserva seleccionada."""
        def accion():
            identificador = str(self._seleccionada())
            self.sistema.confirmar_reserva(identificador)
            return identificador

        ok, identificador = ejecutar_seguro(accion, self)
        if ok:
            registrar_evento(f"Reserva confirmada: {identificador}")
            self.refrescar()

    def cancelar(self):
        """Cancela la reserva seleccionada."""
        def accion():
            identificador = str(self._seleccionada())
            self.sistema.cancelar_reserva(identificador)
            return identificador

        ok, identificador = ejecutar_seguro(accion, self)
        if ok:
            registrar_evento(f"Reserva cancelada: {identificador}")
            self.refrescar()

    def refrescar(self):
        """Vuelve a llenar la tabla de reservas."""
        self.tabla.delete(*self.tabla.get_children())
        for identificador, reserva in self.sistema.reservas.items():
            self.tabla.insert(
                "", tk.END, values=(identificador, reserva.estado)
            )


# ======================================================
# 7. VENTANA DE LOGS
# ======================================================

class VentanaLogs(tk.Toplevel):
    """Ventana que muestra el contenido del archivo de logs."""

    def __init__(self, principal):
        super().__init__(principal)
        self.title("Registro de eventos y errores")

        # Cuadro de texto con barra de desplazamiento.
        self.texto = ScrolledText(self, width=90, height=25)
        self.texto.pack(padx=10, pady=10)

        ttk.Button(self, text="Actualizar", command=self.cargar).pack(
            pady=(0, 10)
        )
        self.cargar()

    def cargar(self):
        """Lee el archivo de logs y lo muestra."""
        self.texto.config(state=tk.NORMAL)
        self.texto.delete("1.0", tk.END)
        if os.path.exists(ARCHIVO_LOGS):
            # Leemos el archivo completo.
            with open(ARCHIVO_LOGS, encoding="utf-8", errors="replace") as archivo:
                self.texto.insert(tk.END, archivo.read())
        else:
            self.texto.insert(tk.END, "Aún no hay registros.")
        # Solo lectura: el usuario no puede editar los logs.
        self.texto.config(state=tk.DISABLED)


# ======================================================
# 8. VENTANA PRINCIPAL
# ======================================================

class Aplicacion(tk.Tk):
    """Ventana principal con los botones del sistema."""

    def __init__(self):
        super().__init__()
        self.title("Software FJ - Sistema de Gestión")
        self.geometry("360x400")
        self.resizable(False, False)

        # Un único sistema compartido por todas las ventanas.
        self.sistema = SistemaSoftwareFJ()

        ttk.Label(
            self, text="SOFTWARE FJ", font=("Arial", 18, "bold")
        ).pack(pady=(20, 2))
        ttk.Label(self, text="Gestión de clientes, servicios y reservas").pack(
            pady=(0, 15)
        )

        # Cada botón abre su ventana correspondiente.
        botones = (
            ("Clientes", lambda: VentanaClientes(self, self.sistema)),
            ("Servicios", lambda: VentanaServicios(self, self.sistema)),
            ("Calcular costo", lambda: VentanaCosto(self, self.sistema)),
            ("Reservas", lambda: VentanaReservas(self, self.sistema)),
            ("Ver logs", lambda: VentanaLogs(self)),
            ("Salir", self.salir),
        )
        for texto, comando in botones:
            ttk.Button(self, text=texto, command=comando, width=28).pack(
                pady=6, ipady=4
            )

        # Registramos el inicio del sistema.
        registrar_evento("Interfaz gráfica iniciada")

    def salir(self):
        """Registra el cierre y termina el programa."""
        registrar_evento("Interfaz gráfica cerrada")
        self.destroy()


# ======================================================
# 9. PUNTO DE ENTRADA
# ======================================================

if __name__ == "__main__":
    Aplicacion().mainloop()