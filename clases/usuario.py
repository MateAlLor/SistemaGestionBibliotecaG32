from datetime import date
from db.localdb import Database

class Usuario:
    def __init__(self, id : int, nombre : str, apellido : str, tipo : int):
        self._ID = id
        self._Nombre = nombre
        self._Apellido = apellido
        self._Tipo = tipo # Tipos de Usuario: 1=Estudiante; 2=Profesor
    
    def __str__(self):
        text = f'ID: {self._ID}'
        text += f'\n\tNombre: {self._Nombre}'
        text += f'\n\tApellido: {self._Apellido}'
        text += f'\n\tTipo: {self._Tipo}'
        return text
        
    @classmethod
    def init_from_json(cls, json_data):
        return cls(
            id=json_data['id'],
            nombre=json_data['nombre'],
            apellido=json_data['apellido'],
            tipo=json_data['tipo']
        )
    
    def convert_to_json(self):
        return {
            "id": self._ID,
            "nombre": self._Nombre,
            "apellido": self._Apellido,
            "tipo": self._Tipo
        }