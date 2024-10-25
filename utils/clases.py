from datetime import date
from db.localdb import Database
import os

# Los métodos init_from_json y convert_to_json no van a hacer falta cuando usemos DB. Vamos a necesitar uno que los arme a partir de la DB
class Autor:
    def __init__(self, id : int, nombre : str, apellido : str, nacionalidad : str):
        self._ID = id
        self._Nombre = nombre
        self._Apellido = apellido
        self._Nacionalidad = nacionalidad
    
    @classmethod
    def init_from_json(cls, json_data):
        return cls(
            id=json_data['id'],
            nombre=json_data['nombre'],
            apellido=json_data['apellido'],
            nacionalidad=json_data['apellido']
        )

    def convert_to_json(self):
        return {
            "id": self._ID,
            "nombre": self._Nombre,
            "apellido": self._Apellido,
            "nacionalidad": self._Nacionalidad
        }
        

class Usuario:
    def __init__(self, id : int, nombre : str, apellido : str, tipo : int):
        self._ID = id
        self._Nombre = nombre
        self._Apellido = apellido
        self._Tipo = tipo # Tipos de Usuario: 1=Estudiante; 2=Profesor
    
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

class Libro:
    def __init__(self, isbn : int, titulo : str, genero : str, anio : int, autor : Autor, cantidad : int):
        self._ISBN = isbn
        self._Titulo = titulo
        self._Genero = genero
        self._Anio = anio
        self._Autor = autor
        self._Cantidad = cantidad
    
    @classmethod
    def init_from_json(cls, json_data):
        print("ENTRA AL INIT FROM JSON DEL LIBRO")
        db = Database(os.path.join("data", "localdb"))
        autores_json = db.load_file('autores.json')
        print('LOS AUTORES JSON SON ESTOS:')
        print(autores_json)

        autor_final = None
        for autor_json in autores_json:
            if autor_json['id'] == json_data['autor']:
                autor_final = Autor.init_from_json(autor_json)
                break
        print("EL AUTOR FINAL ES ESTE:", autor_final)

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

class Prestamo:
    def __init__(self, id : int, usuario : Usuario, libro : Libro, fecha_prestamo : date, fecha_devolucion : date):
        self._ID = id
        self._Usuario = usuario
        self._Libro = libro
        self._FechaPrestamo = fecha_prestamo
        self._FechaDevolucion = fecha_devolucion
    
    @classmethod
    def init_from_json(cls, json_data):
        libro_isbn = json_data['libro']

        db = Database(os.path.join("data", "localdb"))
        usuarios_json = db.load_file('usuarios.json')
        libros_json = db.load_file('libros.json')

        usuario_final = None
        libro_final = None


        for usuario_json in usuarios_json:
            if usuario_json['id'] == json_data['usuario']:
                usuario_final = Usuario.init_from_json(usuario_json)
                break
        
        for libro_json in libros_json:
            if libro_json['isbn'] == json_data['libro']:
                libro_final = Libro.init_from_json(libro_json)
                break

        return cls(
            id=json_data['id'],
            usuario=usuario_final,
            libro=libro_final,
            fecha_prestamo=date.fromisoformat(json_data['fecha_prestamo']),
            fecha_devolucion=date.fromisoformat(json_data['fecha_devolucion'])
        )
    
    def convert_to_json(self):
        return {
            "id": self._ID,
            "usuario": self._Usuario._ID,
            "libro": self._Libro._ISBN,
            "fecha_prestamo": self._FechaPrestamo.isoformat(),
            "fecha_devolucion": self._FechaPrestamo.isoformat()
        }