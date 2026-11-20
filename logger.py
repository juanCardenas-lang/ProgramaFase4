# ARCHIVO: logger.py
# REGISTRO DE OPERACIONES Y ERRORES DEL SISTEMA

import logging
from Excepciones import ErrorRegistro


# Funcion para preparar el archivo de registros.
def configurar_registro():

    try:
        # Configuramos el archivo donde se guardaran los mensajes.
        logging.basicConfig(filename="sistema.log",
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            encoding="utf-8",
            force=True)

    except OSError as causa:
        raise ErrorRegistro("No se pudo crear el archivo de registros.") from causa

    else:
        print("El registro del sistema esta preparado.")

    finally:
        print("Finalizo la configuracion del registro.")


# Funcion para guardar las operaciones correctas.
def registrar_evento(mensaje):

    logging.info(mensaje)


# Funcion para guardar advertencias.
def registrar_advertencia(mensaje):

    logging.warning(mensaje)


# Funcion para registrar los errores del sistema.
def registrar_error(mensaje, error=None):

    if error is None:
        logging.error(mensaje)

    else:
        logging.error(mensaje + " | " + str(error))


# Funcion para guardar una excepcion.
def registrar_excepcion(mensaje):

    logging.exception(mensaje)


# Funcion para consultar los registros.
def consultar_registros():

    try:
        # Abrimos el archivo para leer los mensajes guardados.
        with open("sistema.log", "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

    except FileNotFoundError:
        return "Todavia no existen registros."

    except OSError as causa:
        raise ErrorRegistro("No se pudo leer el archivo de registros.") from causa

    else:
        return contenido


# Prueba individual del programa.
if __name__ == "__main__":

    configurar_registro()

    registrar_evento("Se inicio el sistema.")
    registrar_advertencia("Se presento una advertencia.")
    registrar_error("Se presento un error de ejemplo.")

    print()
    print("REGISTROS GUARDADOS:")
    print(consultar_registros())