# ARCHIVO: pruebas.py
# PRUEBAS DEL SISTEMA DE CLIENTES Y SERVICIOS

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada

from Excepciones import (
    DatosInvalidosError,
    ErrorDuracionInvalida,
    ParametroInvalidoError,
    ServicioNoDisponibleError,
    convertir_duracion,
    ejecutar_validado
)

from logger import (
    configurar_registro,
    registrar_evento,
    registrar_error
)


# Variables para contar las pruebas.
pruebas_realizadas = 0
pruebas_correctas = 0


# Funcion para mostrar los resultados.
def mostrar_resultado(nombre, resultado):

    global pruebas_realizadas
    global pruebas_correctas

    pruebas_realizadas += 1

    if resultado:
        pruebas_correctas += 1
        print("CORRECTO:", nombre)
        registrar_evento("Prueba correcta: " + nombre)

    else:
        print("INCORRECTO:", nombre)
        registrar_error("Prueba incorrecta: " + nombre)


# Funcion para comprobar una operacion correcta.
def probar_operacion(nombre, operacion, resultado_esperado):

    try:
        resultado = operacion()

    except Exception as error:
        registrar_error("Error en " + nombre, error)
        mostrar_resultado(nombre, False)

    else:
        mostrar_resultado(
            nombre,
            resultado == resultado_esperado
        )


# Funcion para comprobar un error esperado.
def probar_error(nombre, operacion, tipo_error):

    try:
        operacion()

    except tipo_error as error:
        registrar_error("Error controlado en " + nombre, error)
        mostrar_resultado(nombre, True)

    except Exception as error:
        registrar_error("Error inesperado en " + nombre, error)
        mostrar_resultado(nombre, False)

    else:
        mostrar_resultado(nombre, False)


# PRUEBA 1: Registrar un cliente.
def prueba_01():

    cliente = Cliente(
        "C1", "Ana Lopez", "12345678",
        "jorge@correo.com", "3001234567"
    )

    return cliente.nombre


# PRUEBA 2: Registrar un cliente sin nombre.
def prueba_02():

    ejecutar_validado(
        Cliente,
        "C2", "", "12345678",
        "jorge@correo.com", "3001234567",
        tipo="cliente"
    )


# PRUEBA 3: Actualizar el correo de un cliente.
def prueba_03():

    cliente = Cliente(
        "C3", "Carlos Perez", "87654321",
        "carlos@correo.com", "3007654321"
    )

    cliente.actualizar_correo("nuevo@correo.com")

    return cliente.correo


# PRUEBA 4: Crear una sala.
def prueba_04():

    sala = ReservaSala(
        "S1", "Sala A", 100, 12, "Piso 2"
    )

    return sala.nombre


# PRUEBA 5: Calcular el costo de una sala.
def prueba_05():

    sala = ReservaSala(
        "S2", "Sala B", 100, 10, "Piso 1"
    )

    return sala.calcular_costo(2)


# PRUEBA 6: Comprobar una capacidad incorrecta.
def prueba_06():

    ejecutar_validado(
        ReservaSala,
        "S3", "Sala C", 100, 0, "Piso 3"
    )


# PRUEBA 7: Comprobar una sala no disponible.
def prueba_07():

    sala = ReservaSala(
        "S4", "Sala D", 100, 15, "Piso 4"
    )

    sala.cambiar_disponibilidad(False)

    ejecutar_validado(
        sala.calcular_costo,
        2
    )


# PRUEBA 8: Crear un equipo.
def prueba_08():

    equipo = AlquilerEquipo(
        "E1", "Portatil", 50, "Computador"
    )

    return equipo.nombre


# PRUEBA 9: Calcular el alquiler de equipos.
def prueba_09():

    equipo = AlquilerEquipo(
        "E2", "Proyector", 50, "Proyector"
    )

    return equipo.calcular_costo(
        2,
        impuesto=0,
        cantidad=3
    )


# PRUEBA 10: Crear una asesoria.
def prueba_10():

    asesoria = AsesoriaEspecializada(
        "A1", "Asesoria", 80,
        "Sistemas", "virtual"
    )

    return asesoria.nombre


# PRUEBA 11: Comprobar una duracion correcta.
def prueba_11():

    return convertir_duracion("3")


# PRUEBA 12: Comprobar una duracion incorrecta.
def prueba_12():

    convertir_duracion("abc")


# PRUEBA 13: Describir un servicio.
def prueba_13():

    sala = ReservaSala(
        "S5", "Sala Principal", 100, 20, "Piso 1"
    )

    descripcion = sala.describir_servicio()

    return "Sala Principal" in descripcion


# PRUEBA 14: Mostrar informacion de un servicio.
def prueba_14():

    equipo = AlquilerEquipo(
        "E3", "Computador", 50, "Portatil"
    )

    informacion = equipo.mostrar_informacion()

    return "Precio por hora" in informacion


# PRUEBA 15: Validar los parametros de un servicio.
def prueba_15():

    sala = ReservaSala(
        "S6", "Sala de reuniones", 100, 10, "Piso 2"
    )

    # Cambiamos la capacidad para comprobar la validacion.
    sala.capacidad = 0

    ejecutar_validado(
        sala.validar_parametros
    )


# PRUEBA 16: Comprobar un precio incorrecto.
def prueba_16():

    ejecutar_validado(
        ReservaSala,
        "S7", "Sala B", -100, 10, "Piso 1"
    )


# PRUEBA 17: Comprobar una modalidad incorrecta.
def prueba_17():

    ejecutar_validado(
        AsesoriaEspecializada,
        "A2", "Asesoria", 80,
        "Sistemas", "otra"
    )


# PRUEBA 18: Comprobar un descuento incorrecto.
def prueba_18():

    sala = ReservaSala(
        "S8", "Sala C", 100, 10, "Piso 3"
    )

    ejecutar_validado(
        sala.calcular_costo,
        2,
        descuento=1.5
    )


# Funcion para ejecutar todas las pruebas.
def realizar_pruebas():

    print("======================================")
    print("       PRUEBAS DEL SISTEMA")
    print("======================================")
    print()

    # Pruebas de clientes.
    probar_operacion(
        "1. Registrar cliente",
        prueba_01,
        "Ana Lopez"
    )

    probar_error(
        "2. Nombre incorrecto",
        prueba_02,
        DatosInvalidosError
    )

    probar_operacion(
        "3. Actualizar correo",
        prueba_03,
        "nuevo@correo.com"
    )

    # Pruebas de salas.
    probar_operacion(
        "4. Crear sala",
        prueba_04,
        "Sala A"
    )

    probar_operacion(
        "5. Calcular costo de sala",
        prueba_05,
        238
    )

    probar_error(
        "6. Capacidad incorrecta",
        prueba_06,
        ParametroInvalidoError
    )

    probar_error(
        "7. Sala no disponible",
        prueba_07,
        ServicioNoDisponibleError
    )

    # Pruebas de equipos.
    probar_operacion(
        "8. Crear equipo",
        prueba_08,
        "Portatil"
    )

    probar_operacion(
        "9. Calcular alquiler de equipos",
        prueba_09,
        300
    )

    # Pruebas de asesorias.
    probar_operacion(
        "10. Crear asesoria",
        prueba_10,
        "Asesoria"
    )

    # Pruebas de duracion.
    probar_operacion(
        "11. Duracion correcta",
        prueba_11,
        3
    )

    probar_error(
        "12. Duracion incorrecta",
        prueba_12,
        ErrorDuracionInvalida
    )

    # Pruebas adicionales de servicios.
    probar_operacion(
        "13. Describir servicio",
        prueba_13,
        True
    )

    probar_operacion(
        "14. Mostrar informacion",
        prueba_14,
        True
    )

    probar_error(
        "15. Validar parametros",
        prueba_15,
        ParametroInvalidoError
    )

    probar_error(
        "16. Precio incorrecto",
        prueba_16,
        ParametroInvalidoError
    )

    probar_error(
        "17. Modalidad incorrecta",
        prueba_17,
        ParametroInvalidoError
    )

    probar_error(
        "18. Descuento incorrecto",
        prueba_18,
        ParametroInvalidoError
    )


# Inicio del programa.
if __name__ == "__main__":

    try:
        configurar_registro()

        realizar_pruebas()

    except Exception as error:
        print("Ocurrio un problema:", error)
        registrar_error("Error general del sistema", error)

    else:
        print()
        print("======================================")
        print("          RESULTADOS FINALES")
        print("======================================")

        print("Pruebas realizadas:", pruebas_realizadas)
        print("Pruebas correctas:", pruebas_correctas)
        print(
            "Pruebas incorrectas:",
            pruebas_realizadas - pruebas_correctas
        )

    finally:
        print()
        print("Finalizo la ejecucion de las pruebas.")