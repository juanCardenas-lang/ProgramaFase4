# ARCHIVO: excepciones.py
# ERRORES QUE SE PUEDEN PRESENTAR EN EL SISTEMA

# Se crea una excepcion general para agrupar los errores del proyecto.
# Las demas excepciones heredan de esta clase.


class ErrorSistema(Exception):
    """Clase base de los errores controlados del proyecto."""


class ErrorCliente(ErrorSistema):
    """Error relacionado con clientes."""


class DatosInvalidosError(ErrorCliente):
    """Los datos de un cliente no son validos."""


class ClienteNoEncontradoError(ErrorCliente):
    """No se encontro un cliente."""


class ClienteDuplicadoError(ErrorCliente):
    """Ya existe un cliente con el identificador indicado."""


class ErrorServicio(ErrorSistema):
    """Error relacionado con servicios."""


class ServicioNoDisponibleError(ErrorServicio):
    """No se puede utilizar un servicio deshabilitado."""


class ServicioNoEncontradoError(ErrorServicio):
    """No se encontro un servicio."""


class ParametroInvalidoError(ErrorServicio):
    """Un parametro del servicio es incorrecto."""


class ErrorReserva(ErrorSistema):
    """Error relacionado con reservas."""


class ReservaNoEncontradaError(ErrorReserva):
    """No se encontro la reserva."""


class ReservaInvalidaError(ErrorReserva):
    """Los datos de la reserva son incorrectos."""


class ReservaDuplicadaError(ErrorReserva):
    """La reserva ya existe."""


class EstadoReservaError(ErrorReserva):
    """No se permite el cambio de estado solicitado."""


class ErrorDuracionInvalida(ErrorReserva):
    """La duracion de la reserva no es valida."""


class ErrorCalculoInvalido(ErrorSistema):
    """No es posible calcular el costo."""


class ErrorOperacionNoPermitida(ErrorSistema):
    """Operacion no autorizada por las reglas del sistema."""


class ErrorRegistro(ErrorSistema):
    """No se pudo escribir o consultar el archivo de eventos."""


# Funcion para comprobar que la duracion sea correcta.
def convertir_duracion(valor):

    # No se aceptan valores verdaderos o falsos como duracion.
    if isinstance(valor, bool):
        raise ErrorDuracionInvalida("La duracion no puede ser booleana.")

    try:
        # Comprobamos que no tenga decimales.
        if isinstance(valor, float) and not valor.is_integer():
            raise ValueError("No se admiten duraciones fraccionarias")

        # Convertimos el valor recibido a un numero entero.
        duracion = int(valor)

    # Si la conversion falla, se genera una excepcion personalizada.
    except (ValueError, TypeError) as causa:
        raise ErrorDuracionInvalida("La duracion debe ser un entero valido.") from causa

    # La duracion debe ser mayor que cero.
    if duracion <= 0:
        raise ErrorDuracionInvalida("La duracion debe ser mayor que cero.")

    return duracion


# Funcion para controlar los errores de clientes y servicios.
def ejecutar_validado(operacion, *datos, tipo="servicio", **opciones):

    # Comprobamos que tipo de operacion se va a realizar.
    if tipo not in ("cliente", "servicio"):
        raise ValueError("El tipo debe ser 'cliente' o 'servicio'.")

    try:
        # Ejecutamos la operacion que recibe la funcion.
        return operacion(*datos, **opciones)

    # Capturamos los errores de validacion de los otros programas.
    except ValueError as causa:

        # Guardamos el mensaje original del error.
        mensaje = str(causa)

        # Si el error corresponde a un cliente.
        if tipo == "cliente":
            raise DatosInvalidosError(mensaje) from causa

        # Comprobamos si el servicio no se encuentra disponible.
        if "no está disponible" in mensaje.lower() or "no esta disponible" in mensaje.lower():
            raise ServicioNoDisponibleError(mensaje) from causa

        # Si algun parametro del servicio es incorrecto.
        raise ParametroInvalidoError(mensaje) from causa


# Prueba individual del programa.
if __name__ == "__main__":

    try:
        convertir_duracion("texto")

    except ErrorDuracionInvalida as error:
        print("Error controlado:", error)
        print("Causa original:", type(error.__cause__).__name__)