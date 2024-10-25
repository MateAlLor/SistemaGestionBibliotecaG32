from utils.clases import Libro, Autor, Usuario, Prestamo
from db.localdb import Database # Cambiar el import a Database cuando dejemos de usar archivos
from typing import List
from datetime import date
import os

class LocalApi:
    def __init__(self) -> None:
        self.DATABASE = Database(os.path.join("data", "localdb")) # Para cuando usemos una DB

    # LECTURAS
    def get_autores(self) -> List[Autor]:
        vec = []
        autores = self.DATABASE.load_file('autores.json')
        for autor in autores:
            vec.append(Autor.init_from_json(autor))
        return vec
    
    def get_autor_byid(self, id) -> Autor:
        autores = self.get_autores()
        for autor in autores:
            if autor._ID == id:
                return autor
        return None
    
    def get_usuarios(self) -> List[Usuario]:
        vec = []
        usuarios = self.DATABASE.load_file('usuarios.json')
        for usuario in usuarios:
            vec.append(Usuario.init_from_json(usuario))
        return vec
    
    def get_usuario_byid(self, id) -> Usuario:
        usuarios = self.get_usuarios()
        for usuario in usuarios:
            if usuario._ID == id:
                return usuario
        return None

    def get_libros(self) -> List[Libro]:
        vec = []
        libros = self.DATABASE.load_file('libros.json')
        for libro in libros:
            vec.append(Libro.init_from_json(libro))
        return vec
    
    def get_libro_byisbn(self, isbn) -> Libro:
        libros = self.get_libros()
        for libro in libros:
            if libro._ISBN == isbn:
                return libro
        return None
    
    def get_prestamos(self) -> List[Prestamo]:
        vec = []
        prestamos = self.DATABASE.load_file('usuarios.json')
        for prestamo in prestamos:
            vec.append(Prestamo.init_from_json(prestamo))
        return vec
    
    def get_prestamo_byid(self, id) -> Prestamo:
        prestamos = self.get_prestamos()
        for prestamo in prestamos:
            if prestamo._ID == id:
                return prestamo
        return None
    
    # Obtener IDS Autoincrementales (El unico que no tiene ID autoincremental es el Libro)
    def get_autor_id(self) -> int:
        return self.DATABASE.obtener_id_ai('autores.json')
    def get_usuario_id(self) -> int:
        return self.DATABASE.obtener_id_ai('usuarios.json')
    def get_prestamo_id(self) -> int:
        return self.DATABASE.obtener_id_ai('prestamos.json')
    
    # Escrituras
    def add_libro(self, isbn : int, titulo : str, genero : str, anio : int, autor_id : int, cantidad : int) -> tuple[bool, str]:
        libros = self.get_libros()
        autores = self.get_autores()
        
        libros_json = []
        for book in libros:
            if book._ISBN == isbn:
                return False, "Ya hay un libro con ese ISBN"
            libros_json.append(book.convert_to_json())
        
        for autor in autores:
            if autor._ID == autor_id:
                libros_json.append({
                    "isbn": isbn,
                    "titulo": titulo,
                    "genero": genero,
                    "anio": anio,
                    "autor": autor_id,
                    "cantidad": cantidad
                })
                self.DATABASE.save_file('libros.json', libros_json)
                return True, "Libro registrado correctamente"
        return False, 'No hay ningún autor con ese ID'
    
    def add_autor(self, id : int, nombre : str, apellido : str, nacionalidad : str) -> tuple[bool, str]:
        autores = self.get_autores()
        autores_json = []
        for autor in autores:
            autores_json.append(autor.convert_to_json())
        autores_json.append({
            "id": id,
            "nombre": nombre,
            "apellido": apellido,
            "nacionalidad": nacionalidad
        })

        self.DATABASE.save_file('autores.json', autores_json)
        return True, "Autor registrado correctamente"
    
    def add_usuario(self, id : int, nombre : str, apellido : str, tipo : int) -> tuple[bool, str]:
        usuarios = self.get_usuarios()
        usuarios_json = []
        for usuario in usuarios:
            usuarios_json.append(usuario.convert_to_json())
        usuarios_json.append({
            "id": id,
            "nombre": nombre,
            "apellido": apellido,
            "tipo": tipo
        })

        self.DATABASE.save_file('usuarios.json', usuarios_json)
        return True, "Usuario registrado correctamente"
    