# ARCHIVO: gestor.py
# AUTOR: Santiago Cañola Medina - Integrante 2 (Módulo 2)
# CLASE GESTORSISTEMA: administra clientes, servicios y reservas

from cliente import Cliente
from servicios import Servicio
from reserva import Reserva
from excepciones import (
    ErrorSistema,
    DatosInvalidosError,
    ClienteNoEncontradoError,
    ClienteDuplicadoError,
    ErrorServicio,
    ServicioNoEncontradoError,
    ReservaNoEncontradaError,
    ReservaDuplicadaError,
    ReservaInvalidaError,
    ejecutar_validado,
)
import logger  # Módulo de registro de eventos y errores


class GestorSistema:

    def __init__(self):
        # Listas internas: diccionarios cuya llave es el identificador
        self._clientes = {}
        self._servicios = {}
        self._reservas = {}

    # ---------- CLIENTES ----------

    def crear_cliente(self, identificador, nombre, documento, correo, telefono):
        try:
            # Se crea el cliente; si los datos son malos, se lanza DatosInvalidosError
            cliente = ejecutar_validado(
                Cliente, identificador, nombre, documento, correo, telefono,
                tipo="cliente"
            )
            self.registrar_cliente(cliente)
        except ErrorSistema as error:
            # Se guarda el error en el log y se vuelve a lanzar
            logger.registrar_error("No se pudo crear el cliente", error)
            raise
        else:
            # Si todo salió bien, se registra el evento
            logger.registrar_evento(f"Cliente registrado: {cliente.identificador}")
            return cliente
        finally:
            # Este bloque se ejecuta siempre
            logger.registrar_evento("Terminó la operación: crear cliente")

    def registrar_cliente(self, cliente):
        # Solo se aceptan objetos de la clase Cliente
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Solo se pueden registrar objetos Cliente.")

        # No se permiten identificadores repetidos
        if cliente.identificador in self._clientes:
            raise ClienteDuplicadoError(f"Ya existe el cliente {cliente.identificador}.")

        self._clientes[cliente.identificador] = cliente

    def buscar_cliente(self, identificador):
        try:
            return self._clientes[str(identificador).strip()]
        except KeyError as causa:
            # Se cambia el KeyError por una excepción propia (encadenamiento)
            raise ClienteNoEncontradoError(f"No existe el cliente {identificador}.") from causa

    def listar_clientes(self):
        return list(self._clientes.values())

    # ---------- SERVICIOS ----------

    def crear_servicio(self, clase_servicio, *datos, **opciones):
        # clase_servicio puede ser ReservaSala, AlquilerEquipo o AsesoriaEspecializada
        try:
            servicio = ejecutar_validado(clase_servicio, *datos, tipo="servicio", **opciones)
            self.registrar_servicio(servicio)
        except ErrorSistema as error:
            logger.registrar_error("No se pudo crear el servicio", error)
            raise
        else:
            logger.registrar_evento(f"Servicio registrado: {servicio.identificador}")
            return servicio
        finally:
            logger.registrar_evento("Terminó la operación: crear servicio")

    def registrar_servicio(self, servicio):
        # Solo se aceptan objetos de la clase Servicio
        if not isinstance(servicio, Servicio):
            raise ErrorServicio("Solo se pueden registrar objetos Servicio.")

        # No se permiten identificadores repetidos
        if servicio.identificador in self._servicios:
            raise ErrorServicio(f"Ya existe el servicio {servicio.identificador}.")

        self._servicios[servicio.identificador] = servicio

    def buscar_servicio(self, identificador):
        try:
            return self._servicios[str(identificador).strip()]
        except KeyError as causa:
            raise ServicioNoEncontradoError(f"No existe el servicio {identificador}.") from causa

    def listar_servicios(self):
        return list(self._servicios.values())

    def cambiar_disponibilidad(self, identificador, estado):
        # Habilita o deshabilita un servicio registrado
        servicio = self.buscar_servicio(identificador)
        ejecutar_validado(servicio.cambiar_disponibilidad, estado, tipo="servicio")
        logger.registrar_evento(f"Disponibilidad del servicio {identificador}: {estado}")

    # ---------- RESERVAS ----------

    def crear_reserva(self, id_reserva, id_cliente, id_servicio, duracion,
                      impuesto=0.19, descuento=0, cantidad=1):
        try:
            # Se comprueba que la reserva no exista
            if str(id_reserva).strip() in self._reservas:
                raise ReservaDuplicadaError(f"Ya existe la reserva {id_reserva}.")

            # Se buscan el cliente y el servicio (pueden no existir)
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)

            # Se crea y se guarda la reserva
            reserva = Reserva(id_reserva, cliente, servicio, duracion,
                              impuesto, descuento, cantidad)
            self._reservas[reserva.identificador] = reserva
        except ErrorSistema as error:
            logger.registrar_error(f"No se pudo crear la reserva {id_reserva}", error)
            raise
        else:
            logger.registrar_evento(
                f"Reserva creada: {reserva.identificador} | costo ${reserva.costo_total:,.2f}"
            )
            return reserva
        finally:
            logger.registrar_evento("Terminó la operación: crear reserva")

    def buscar_reserva(self, identificador):
        try:
            return self._reservas[str(identificador).strip()]
        except KeyError as causa:
            raise ReservaNoEncontradaError(f"No existe la reserva {identificador}.") from causa

    def confirmar_reserva(self, identificador):
        try:
            reserva = self.buscar_reserva(identificador)
            reserva.confirmar()
        except ErrorSistema as error:
            logger.registrar_error(f"No se pudo confirmar la reserva {identificador}", error)
            raise
        else:
            logger.registrar_evento(f"Reserva {identificador} confirmada")
            return reserva
        finally:
            logger.registrar_evento("Terminó la operación: confirmar reserva")

    def procesar_reserva(self, identificador):
        try:
            reserva = self.buscar_reserva(identificador)
            reserva.procesar()
        except ErrorSistema as error:
            logger.registrar_error(f"No se pudo procesar la reserva {identificador}", error)
            raise
        else:
            logger.registrar_evento(f"Reserva {identificador} procesada")
            return reserva
        finally:
            logger.registrar_evento("Terminó la operación: procesar reserva")

    def cancelar_reserva(self, identificador):
        try:
            reserva = self.buscar_reserva(identificador)
            reserva.cancelar()
        except ErrorSistema as error:
            logger.registrar_error(f"No se pudo cancelar la reserva {identificador}", error)
            raise
        else:
            logger.registrar_evento(f"Reserva {identificador} cancelada")
            return reserva
        finally:
            logger.registrar_evento("Terminó la operación: cancelar reserva")

    # ---------- CONSULTAS ----------

    def listar_reservas(self):
        return list(self._reservas.values())

    def reservas_de_cliente(self, id_cliente):
        cliente = self.buscar_cliente(id_cliente)
        resultado = []
        for reserva in self._reservas.values():
            if reserva.cliente is cliente:
                resultado.append(reserva)
        return resultado

    def reservas_por_estado(self, estado):
        estado = str(estado).upper()
        if estado not in (Reserva.PENDIENTE, Reserva.CONFIRMADA,
                          Reserva.PROCESADA, Reserva.CANCELADA):
            raise ReservaInvalidaError(f"Estado desconocido: {estado}.")

        resultado = []
        for reserva in self._reservas.values():
            if reserva.estado == estado:
                resultado.append(reserva)
        return resultado

    def total_procesado(self):
        # Suma el costo de todas las reservas procesadas
        total = 0
        for reserva in self.reservas_por_estado(Reserva.PROCESADA):
            total += reserva.costo_total
        return round(total, 2)
