# ARCHIVO: cliente.py
# CLASE CLIENTE QUE HEREDA DE ENTIDAD

import re 
from entidades import Entidad

# SE DEFINE LA CLASE CLIENTE
class Cliente(Entidad):

    def __init__(self, identificador, nombre, documento, correo, telefono):

        super().__init__(identificador)

        # Validación del nombre 
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]+", nombre.strip()):
            raise ValueError("El nombre contiene caracteres inválidos.")

        # Validación del documento
        if not str(documento).isdigit():
            raise ValueError("El documento debe contener solo números.")

        if len(str(documento)) < 5:
            raise ValueError("El documento debe tener minimo 5 digitos.")

        # Validación del correo electrónico 
        patron_correo = r"^[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}$"
        if not isinstance(correo, str) or not re.fullmatch(patron_correo, correo.strip()):
            raise ValueError("El correo electrónico no es válido.")

        # Validación del telefóno
        if not str(telefono).isdigit() or len(str(telefono)) < 7:
            raise ValueError("El número de teléfono no es válido.")

        # Atributos privados
        self.__nombre = nombre.strip()
        self.__documento = str(documento)
        self.__correo = correo.strip().lower()
        self.__telefono = str(telefono)

        # Métodos de consultas de datos privados 
        @property
        def nombre(self):
            return self.__nombre

        @property
        def documento(self):
            return self.__documento

        @property
        def correo(self):
            return self.__correo

        @property
        def telefono(self):
            return self.__telefono

        # Método para mostrar información
        def mostrar_información(self):
            return (
                f"ID: {self.identificador}\n"
                f"Nombre: {self.nombre}\n"
                f"Documento: {self.documento}\n"
                f"Correo: {self.correo}\n"
                f"Teléfono: {self.telefono}"
            )

        # Método para actualizar el correo
        def actualizar_correo(self, nuevo_correo):

            patron = r"^[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}$"

            if not isinstance(nuevo_correo, str) or not re.fullmatch(patron, nuevo_correo.strip()):
                raise ValueError("El nuevo correo no es válido.")

            self.__correo = nuevo_correo.strip().lower()
            