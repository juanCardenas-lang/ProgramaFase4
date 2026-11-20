# ARCHIVO: main.py
# SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ 
# ARCHIVO PRINCIPAL: INTEGRA TODOS LOS MODULOS

from gestor import GestorSistema
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from logger import configurar_registro

# FUNCIONES AUXILIARES

def leer_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor 
        print("Este campo no puede estar vacio.")

def leer_entero(mensaje):
    while True:
        try:
            valor = input(mensaje)
            return int(valor.strip())

        except ValueError:
            print("Debe ingresar un numero entero.")


def leer_decimal(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Debe ingresar un número válido.")


def mostrar_lista(elementos, metodo):
    if not elementos:
        print("\nNo hay registros disponibles.")
        return
    for elemento in elementos:
        print("\n" + "-" * 40)
        print(getattr(elemento, metodo )())


def ejecutar_accion(funcion):
    try:
        funcion()
    except Exception as error:
        print(f"\nNo se pudo completar la operación: {error}")


# MENÚ DE CLIENTES

def menu_clientes(gestor):
    while True:
        print("\n========== GESTION DE CLIENTES ==========")
        print("1. Registrar cliente")
        print("2. Buscar cliente")
        print("3. Listar clientes")
        print("4. Volver al menu principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            identificador = leer_texto("Identificador: ")
            nombre = leer_texto("Nombre: ")
            documento = leer_texto("Documento: ")
            correo = leer_texto("Correo electrónico: ")
            telefono = leer_texto("Teléfono: ")

            cliente = gestor.crear_cliente(identificador, nombre, documento, correo, telefono)
            print("\nCliente registrado correctamente.")
            print(cliente.mostrar_informacion())

        elif opcion == "2":
            identificador = leer_texto("Identificador del cliente: ")
            cliente = gestor.buscar_cliente(identificador)
            print("\n" + cliente.mostrar_informacion())

        elif opcion == "3":
            mostrar_lista(gestor.listar_clientes(), "mostrar_informacion")

        elif opcion == "4":
            break

        else:
            print("Opción no válida.")

# MENU DE SERVICIOS
def menu_servicios(gestor):
    while True:
        print("\n========== GESTION DE SERVICIOS ==========")
        print("1. Registrar servicio")
        print("2. Buscar servicio")
        print("3. Listar servicios")
        print("4. Cambiar disponibilidad")
        print("5. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":

            print("\nTipos de servicio:")
            print("1. Reserva de sala")
            print("2. Alquiler de equipo")
            print("3. Asesoria especializada")

            tipo = input("Seleccione el tipo de servicio: ").strip()

            identificador = leer_texto("Identificador: ")
            nombre = leer_texto("Nombre del servicio: ")
            precio = leer_decimal("Precio base por hora: ")

            if tipo == "1":
                capacidad = leer_entero("Capacidad de la sala: ")
                            

                ubicacion = leer_texto("Ubicacion: ")

                servicio = gestor.crear_servicio(
                    ReservaSala,
                    identificador,
                    nombre,
                    precio,
                    capacidad,
                    ubicacion
                )

            elif tipo == "2":
               tipo_equipo = leer_texto("Tipo de equipos: ")

               servicio = gestor.crear_servicio(
                   AlquilerEquipo,
                   identificador,
                   nombre,
                   precio,
                   tipo_equipo
    )
            elif tipo == "3":
                especialidad = leer_texto("Especialidad: ")
                modalidad = leer_texto(
                    "Modalidad (virtual/presencial): "
                )
                servicio = gestor.crear_servicio(
                    AsesoriaEspecializada, 
                    identificador,
                    nombre,
                    precio,
                    especialidad,
                    modalidad
                )

            else:
                print("Tipo de servicio no valido.")
                continue
            print("\nServicio registrado correctamente.")
            print(servicio.mostrar_informacion())

        elif opcion == "2":
            identificador = leer_texto("Identificador del servicio: ")
            servicio = gestor.buscar_servicio(identificador)
            print("\n" + servicio.mostrar_informacion())

        elif opcion == "3":
            mostrar_lista(gestor.listar_servicios(), "mostrar_informacion")

        elif opcion == "4":
            identificador = leer_texto("Identificador del servicio: ")

            estado = input (
                "¿El servicio estará disponible? (s/n): "
            ).strip().lower()

            if estado not in ("s", "n"):
                print("Debe responder s o n.")
                continue
            gestor.cambiar_disponibilidad(
                identificador, estado == "s"
            )

            print("Disponibilidad actulizada correctamente.")

        elif opcion == "5":
            break

        else: 
            print("Opción no válida.")



# MENU DE RESERVAS


def menu_reservas(gestor):
    while True:
        print("\n========== GESTION DE RESERVAS ==========")
        print("1. Crear reserva")
        print("2. Confirmar reserva")
        print("3. Procesar reserva")
        print("4. Cancelar reserva")
        print("5. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            id_reserva = leer_texto("Identificador de la reserva: ")
            id_cliente = leer_texto("Identificador del cliente: ")
            id_servicio = leer_texto("Identificador del servicio: ")

            duracion = leer_entero("Duracion en horas enteras: ")

            descuento = leer_decimal(
                "Descuento en porcentaje (ejemplo 10 para 10%): "
            ) / 100

            servicio = gestor.buscar_servicio(id_servicio)

            cantidad = 1

            if isinstance(servicio, AlquilerEquipo):
                cantidad = leer_entero("Cantidad de equipos: ")

            reserva = gestor.crear_reserva(
                id_reserva,
                id_cliente,
                id_servicio,
                duracion,
                impuesto=0.19,
                descuento=descuento,
                cantidad=cantidad
            )

            print("\nReserva creada correctamente.")
            print(reserva.mostrar_informacion())

        elif opcion == "2":
            identificador = leer_texto("Identificador de la reserva: ")
            reserva = gestor.confirmar_reserva(identificador)
            print("\nReserva confirmada correctamente.")
            print(reserva.mostrar_informacion())

        elif opcion == "3":
            identificador = leer_texto("Identificador de la reserva: ")
            reserva = gestor.procesar_reserva(identificador)
            print("\nReserva procesada correctamente.")
            print(reserva.mostrar_informacion())

        elif opcion == "4":
            identificador = leer_texto("Identificador de la reserva: ")
            reserva = gestor.cancelar_reserva(identificador)
            print("\nReserva cancelada correctamente.")
            print(reserva.mostrar_informacion())

        elif opcion == "5":
            break

        else:
            print("Opcion no valida.")



# MENU DE CONSULTAS


def menu_consultas(gestor):
    while True:
        print("\n========== CONSULTAS DEL SISTEMA ==========")
        print("1. Listar todas las reservas")
        print("2. Consultar reservas de un cliente")
        print("3. Consultar reservas por estado")
        print("4. Consultar total procesado")
        print("5. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            mostrar_lista(
                gestor.listar_reservas(),
                "mostrar_informacion"
            )

        elif opcion == "2":
            identificador = leer_texto("Identificador del cliente: ")

            reservas = gestor.reservas_de_cliente(identificador)

            mostrar_lista(reservas, "mostrar_informacion")

        elif opcion == "3":
            print("\nEstados disponibles:")
            print("1. Pendiente")
            print("2. Confirmada")
            print("3. Procesada")
            print("4. Cancelada")

            estados = {
                "1": Reserva.PENDIENTE,
                "2": Reserva.CONFIRMADA,
                "3": Reserva.PROCESADA,
                "4": Reserva.CANCELADA
            }

            seleccion = input("Seleccione el estado: ").strip()

            if seleccion not in estados:
                print("Estado no valido.")
                continue

            reservas = gestor.reservas_por_estado(
                estados[seleccion]
            )

            mostrar_lista(reservas, "mostrar_informacion")

        elif opcion == "4":
            total = gestor.total_procesado()

            print("\n================================")
            print(f"TOTAL PROCESADO: ${total:,.2f}")
            print("================================")

        elif opcion == "5":
            break

        else:
            print("Opcion no valida.")



# MENU PRINCIPAL


def main():
    # Configuracion del registro de eventos
    configurar_registro()

    # Creacion del gestor principal
    gestor = GestorSistema()

    print("\n==========================================")
    print("             SOFTWARE FJ")
    print(" SISTEMA INTEGRAL DE GESTION")
    print("==========================================")

    while True:
        print("\n=============== MENU PRINCIPAL ===============")
        print("1. Gestion de clientes")
        print("2. Gestion de servicios")
        print("3. Gestion de reservas")
        print("4. Consultas del sistema")
        print("5. Salir")
        print("==============================================")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            ejecutar_accion(lambda: menu_clientes(gestor))

        elif opcion == "2":
            ejecutar_accion(lambda: menu_servicios(gestor))

        elif opcion == "3":
            ejecutar_accion(lambda: menu_reservas(gestor))

        elif opcion == "4":
            ejecutar_accion(lambda: menu_consultas(gestor))

        elif opcion == "5":
            print("\nGracias por utilizar el sistema Software FJ.")
            print("Finalizando el programa...")
            break

        else:
            print("\nOpcion no valida. Intente nuevamente.")



# PUNTO DE ENTRADA DEL PROGRAMA


if __name__ == "__main__":
    main()
