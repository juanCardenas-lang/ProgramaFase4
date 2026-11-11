# ARCHIVO: servicios.py
# CLASE ABSTRACTA SERVICIO Y CLASES DERICADAS

from abc import abstractmethod
from entidades import Entidad
import math

# CLASE ABSTRACTA SERVICIO 
class Servicio(Entidad):
    def __init__(self, identificador, nombre, precio_base, disponible=True):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del servicio es obligatorio. ")

        if isinstance(precio_base, bool) or not isinstance(precio_base, (int, float)):
            raise ValueError("El precio debe ser númerico. ")
        
        if not math.isfinite(precio_base) or precio_base <= 0:
            raise ValueError("El precio debe ser un mayor que cero. ")

        if not isinstance(disponible, bool):
            raise ValueError("La disponibilidad debe ser verdadera o falsa.")

        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._disponible = disponible 

    @property 
    def nombre(self):
     return self._nombre

    @property 
    def precio_base(self):
     return self._precio_base

    @property 
    def disponible(self):
     return self._disponible

    def cambiar_disponibilidad(self, estado):
            if not isinstance(estado, bool):
                raise ValueError("El estado debe ser booleano.")

            self._disponible = estado

        # Validación común de los calculos

    def _calcular_total(self, duracion, impuesto, descuento):
            if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
                raise ValueError("La duración debe ser numérica. ")

            if not math.isfinite(duracion) or duracion <= 0:
                raise ValueError("La duración debe ser mayor que cero. ")

            if not isinstance(impuesto, (int, float)) or isinstance(impuesto, bool):
                raise ValueError("El impuesto debe ser numérico.")

            if not isinstance(descuento, (int, float)) or isinstance(descuento, bool):
                raise ValueError("El descuento debe ser numérico.")

            if not math.isfinite(impuesto) or not 0 <= impuesto <= 1:
                raise ValueError("El impuesto debe estar entre 0 y 1.")

            if not math.isfinite(descuento) or not 0 <= descuento <= 1:
                raise ValueError("El descuento debe estar entre 0 y 1.")

            subtotal = self._precio_base * duracion
            valor_descuento = subtotal * descuento
            subtotal_descuento = subtotal - valor_descuento
            total = subtotal_descuento * (1 + impuesto)
            return round(total, 2)

        # Métodos que deben  implementar los servicios especializados
        
    @abstractmethod 
    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):
     pass 

    @abstractmethod 
    def describir_servicio(self):
     pass 

    @abstractmethod 
    def validar_parametros(self):
     pass 
        
# SERVICIO 1: RESERVA DE SALAS

class ReservaSala(Servicio):

    def __init__(self, identificador, nombre, precio_base, capacidad, ubicacion, disponible=True):
        super().__init__(identificador, nombre, precio_base, disponible)
        self.capacidad = capacidad
        self.ubicacion = ubicacion

        self.validar_parametros()

    def validar_parametros(self):
        if isinstance(self.capacidad, bool) or not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ValueError("La capacidad debe ser un entero positivo. ")
        if not isinstance(self.ubicacion, str) or not self.ubicacion.strip():
            raise ValueError("La ubicación de la sala es obligatoria.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):

        if not self.disponible:
            raise ValueError("La sala no está disponible. ")

        return self._calcular_total(duracion, impuesto, descuento)

    def describir_servicio(self):
        return (
            f"Reserva de sala: {self.nombre}\n"
            f"Capacidad: {self.capacidad}\n"
            f"Ubicación: {self.ubicacion}\n"
            f"Precio por hora: ${self.precio_base:,.2f}"
        )
    def mostrar_informacion(self):
        return self.describir_servicio()


# SERVICIO 2: ALQUILER DE EQUIPOS

class AlquilerEquipo(Servicio):

    def __init__(self, identificador, nombre, precio_base, tipo_equipo, disponible=True):

        super().__init__(identificador, nombre, precio_base, disponible)
        self.tipo_equipo = tipo_equipo

        self.validar_parametros()

    def validar_parametros(self):
        if not isinstance(self.tipo_equipo, str) or not self.tipo_equipo.strip():
            raise ValueError("Debe especificar el tipo de equipo. ")

    # Se incorpora cantidad como parámetro opcional
    def calcular_costo(self, duracion, impuesto=0.19, descuento=0, cantidad=1):

        if not self.disponible:
            raise ValueError("El equipo no está disponible. ")

        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo. ")

        total = self._calcular_total(duracion, impuesto, descuento)
        return round(total * cantidad, 2)

    def describir_servicio(self):
        return (
            f"Alquiler de equipo: {self.nombre}\n"
            f"Tipo de equipo: {self.tipo_equipo}\n"
            f"Precio por hora: ${self.precio_base:,.2f}")

    def mostrar_informacion(self):
        return self.describir_servicio()


# SERVICIO 3: ASESORÍAS ESPECIALIZADAS

class AsesoriaEspecializada(Servicio):

    def __init__(self, identificador, nombre, precio_base, especialidad, modalidad, disponible=True):

        super().__init__(identificador, nombre, precio_base, disponible)

        self.especialidad = especialidad 
        self.modalidad = modalidad

        self.validar_parametros()

    def validar_parametros(self):

        if not isinstance(self.especialidad, str) or not self.especialidad.strip():
            raise ValueError("La especialidad es obligatoria. ")

        modalidades_validas = ["virtual", "presencial"]

        if not isinstance(self.modalidad, str) or self.modalidad.lower() not in modalidades_validas:
            raise ValueError("La modalidad debe ser virtual o presencial. ")

        self.modalidad = self.modalidad.lower()

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):
        if not self.disponible:
         raise ValueError("La asesoría no está disponible.")

        total = self._calcular_total(duracion, impuesto, descuento)

        # Las asesorías presenciales tienen un recargo del 10%

        if self.modalidad.lower() == "presencial":
           total *= 1.10

        return round(total, 2)

    def describir_servicio(self):

        return (
            f"Asesoría especializada: {self.nombre}\n"
            f"Especialidad: {self.especialidad}\n"
            f"Modalidad: {self.modalidad}\n"
            f"Precio por hora: ${self.precio_base:,.2f}")
        
    def mostrar_informacion(self):
        return self.describir_servicio()