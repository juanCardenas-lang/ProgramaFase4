# ARCHIVO : Entidades.py
# CLASE ABSTRACTA ENTIDAD

from abc import ABC, abstractmethod
class Entidad (ABC):

    def __init__(self, identificador):
        if not identificador or not  str(identificador).strip():
            raise ValueError("El identificador es obligatorio.")

        self._identificador = str(identificador).strip()

# Propiedad para consultar el identificador 
@property
def identificador(self):
    return self._identificador

# Método abstracto que deben implementar las clases hijas
@abstractmethod
def mostrar_infromacion(self):
    pass 
