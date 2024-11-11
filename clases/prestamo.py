from datetime import date
from db.localdb import Database
from clases.libro import Libro
from clases.usuario import Usuario
import os

class Prestamo:
    def __init__(self, id : int, usuario : Usuario, libro : Libro, fecha_prestamo : date, fecha_devolucion : date):
        self._ID = id
        self._Usuario = usuario
        self._Libro = libro
        self._FechaPrestamo = fecha_prestamo
        self._FechaDevolucion = fecha_devolucion
    
    def __str__(self):
        text = f'ID: {self._ID}'

        text += f'\n\tUsuario:'
        text += f'\n\t\t{self._Usuario._Nombre} {self._Usuario._Apellido}'
        text += f'\n\t\tID: {self._Usuario._ID}'
        if self._Usuario._Tipo == 1:
            text += f'\n\t\tTipo: Estudiante'
        else:
            text += f'\n\t\tTipo: Profesor'

        text += f'\n\tLibro: '
        text += f'\n\t\tISBN: {self._Libro._ISBN}'
        text += f'\n\t\tTítulo: {self._Libro._Titulo}'
        text += f'\n\t\tAutor: {self._Libro._Autor._Nombre} {self._Libro._Autor._Apellido}'

        text += f'\n\tFecha del Préstamo: {self._FechaPrestamo}'
        if self._FechaDevolucion:
            text += f'\n\tFecha de Devolución: {self._FechaDevolucion}'
        else:
            text += f'\n\tNO DEVUELTO'
        return text
    
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
        
        fechadev = None
        if json_data['fecha_devolucion']:
            fechadev = date.fromisoformat(json_data['fecha_devolucion'])

        return cls(
            id=json_data['id'],
            usuario=usuario_final,
            libro=libro_final,
            fecha_prestamo=date.fromisoformat(json_data['fecha_prestamo']),
            fecha_devolucion=fechadev
        )
    
    def convert_to_json(self):
        fechadev = None
        if self._FechaDevolucion:
            fechadev = self._FechaDevolucion.isoformat()
        return {
            "id": self._ID,
            "usuario": self._Usuario._ID,
            "libro": self._Libro._ISBN,
            "fecha_prestamo": self._FechaPrestamo.isoformat(),
            "fecha_devolucion": fechadev
        }