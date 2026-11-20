# ARCHIVO: reserva.py
# AUTOR: Santiago Cañola Medina - Integrante 2 (Módulo 2)
# CLASE RESERVA: une un cliente con un servicio y controla su estado

# Se importan las clases creadas por los otros integrantes
from entidades import Entidad
from cliente import Cliente
from servicios import Servicio, AlquilerEquipo

# Se importan las excepciones personalizadas y funciones de apoyo
from Excepciones import (
    ReservaInvalidaError,
    EstadoReservaError,
    ServicioNoDisponibleError,
    convertir_duracion,
    ejecutar_validado,
)


# La clase Reserva hereda de Entidad (herencia)
class Reserva(Entidad):

    # Estados que puede tener una reserva
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"

    def __init__(self, identificador, cliente, servicio, duracion,
                 impuesto=0.19, descuento=0, cantidad=1):

        # Se valida el identificador con la clase padre (Entidad).
        # Si falla, se lanza una excepción propia encadenada con "from"
        try:
            super().__init__(identificador)
        except ValueError as causa:
            raise ReservaInvalidaError("El identificador de la reserva es obligatorio.") from causa

        # Se verifica que el cliente sea un objeto de la clase Cliente
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")

        # Se verifica que el servicio sea un objeto de la clase Servicio
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")

        # La cantidad solo se puede usar con el alquiler de equipos
        if not isinstance(servicio, AlquilerEquipo) and cantidad != 1:
            raise ReservaInvalidaError("La cantidad solo aplica al alquiler de equipos.")

        # Atributos protegidos (encapsulación)
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = convertir_duracion(duracion)  # Valida que sea un entero mayor que cero
        self._impuesto = impuesto
        self._descuento = descuento
        self._cantidad = cantidad
        self._estado = Reserva.PENDIENTE  # Toda reserva nueva empieza pendiente

        # Se calcula el costo al crear la reserva; si hay algún dato
        # incorrecto o el servicio no está disponible, aquí se detecta
        self._costo_total = self._calcular_costo()

    # ---------- Métodos para consultar los datos ----------

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    # ---------- Cálculo del costo ----------

    def _calcular_costo(self):
        # Polimorfismo: cada servicio calcula el costo a su manera
        if isinstance(self._servicio, AlquilerEquipo):
            # El alquiler de equipos también recibe la cantidad
            return ejecutar_validado(
                self._servicio.calcular_costo,
                self._duracion, self._impuesto, self._descuento,
                tipo="servicio", cantidad=self._cantidad
            )

        # Sala y asesoría usan solo duración, impuesto y descuento
        return ejecutar_validado(
            self._servicio.calcular_costo,
            self._duracion, self._impuesto, self._descuento,
            tipo="servicio"
        )

    # ---------- Control de estados ----------

    def confirmar(self):
        # Solo se puede confirmar una reserva pendiente
        if self._estado != Reserva.PENDIENTE:
            raise EstadoReservaError(f"No se puede confirmar una reserva {self._estado}.")

        # El servicio debe seguir disponible
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self._servicio.nombre} no está disponible."
            )

        self._estado = Reserva.CONFIRMADA

    def procesar(self):
        # Solo se puede procesar una reserva confirmada
        if self._estado != Reserva.CONFIRMADA:
            raise EstadoReservaError(f"No se puede procesar una reserva {self._estado}.")

        self._estado = Reserva.PROCESADA

    def cancelar(self):
        # No se puede cancelar una reserva procesada ni una ya cancelada
        if self._estado == Reserva.PROCESADA or self._estado == Reserva.CANCELADA:
            raise EstadoReservaError(f"No se puede cancelar una reserva {self._estado}.")

        self._estado = Reserva.CANCELADA

    # ---------- Método abstracto heredado de Entidad ----------

    def mostrar_informacion(self):
        return (
            f"Reserva: {self.identificador}\n"
            f"Cliente: {self._cliente.nombre}\n"
            f"Servicio: {self._servicio.nombre}\n"
            f"Duración: {self._duracion} hora(s)\n"
            f"Costo total: ${self._costo_total:,.2f}\n"
            f"Estado: {self._estado}"
        )
