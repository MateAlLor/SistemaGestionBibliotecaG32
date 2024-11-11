from db.localdb import Database
from clases.autor import Autor
import os

class Libro:
    def __init__(self, isbn : int, titulo : str, genero : str, anio : int, autor : Autor, cantidad : int):
        self._ISBN = isbn
        self._Titulo = titulo
        self._Genero = genero
        self._Anio = anio
        self._Autor = autor
        self._Cantidad = cantidad

    def __str__(self):
        text = f'ISBN: {self._ISBN}'
        text += f'\n\tGenero: {self._Titulo}'
        text += f'\n\tApellido: {self._Genero}'
        text += f'\n\tAnio: {self._Anio}'
        text += f'\n\tAutor: {self._Autor}'
        text += f'\n\tCantidad Disponible: {self._Cantidad}'
        return text

    def __eq__(self, obj2):
        if isinstance(obj2, Libro):
            return self._ISBN == obj2._ISBN
        return False
    
    @classmethod
    def init_from_json(cls, json_data):
        db = Database(os.path.join("data", "localdb"))
        autores_json = db.load_file('autores.json')

        autor_final = None
        for autor_json in autores_json:
            if autor_json['id'] == json_data['autor']:
                autor_final = Autor.init_from_json(autor_json)
                break

        return cls(
            isbn=json_data['isbn'],
            titulo=json_data['titulo'],
            genero=json_data['genero'],
            anio=json_data['anio'],
            autor=autor_final,
            cantidad=json_data['cantidad']
        )

    def convert_to_json(self):
        return {
            "isbn": self._ISBN,
            "titulo": self._Titulo,
            "genero": self._Genero,
            "anio": self._Anio,
            "autor": self._Autor._ID,
            "cantidad": self._Cantidad
        }