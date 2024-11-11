from db.localdb import Database
from typing import List, Tuple
from datetime import date
import os
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from clases.autor import Autor
from clases.libro import Libro
from clases.prestamo import Prestamo
from clases.usuario import Usuario

class LocalApi:
    def __init__(self) -> None:
        self.DATABASE = Database(os.path.join("data", "localdb"))

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
        prestamos = self.DATABASE.load_file('prestamos.json')
        for prestamo in prestamos:
            vec.append(Prestamo.init_from_json(prestamo))
        return vec
    
    def get_prestamo_byid(self, id) -> Prestamo:
        prestamos = self.get_prestamos()
        for prestamo in prestamos:
            if prestamo._ID == id:
                return prestamo
        return None
    
    def get_prestamos_byisbn(self, isbn) -> List[Prestamo]: # Obtener todos los préstamos de un Libro
        prestamos = self.get_prestamos()
        prestamos_por_libro = []
        for prestamo in prestamos:
            if prestamo._Libro._ISBN == isbn:
                prestamos_por_libro.append(prestamo)
        
        return prestamos_por_libro

    def get_prestamos_vencidos(self) -> List[Prestamo]:
        prestamos = self.get_prestamos()
        prestamos_vencidos = []
        for prestamo in prestamos:
            fecha_prest = prestamo._FechaPrestamo
            today = date.today()
            fecha_estimada = fecha_prest + relativedelta(months=1)
            
            if not prestamo._FechaDevolucion and fecha_estimada < today:
                prestamos_vencidos.append(prestamo)
        return prestamos_vencidos
    
    def get_libros_mas_prestados(self) -> List[Tuple[Libro, int]]:
        prestamos = self.get_prestamos()
        lista_libros = []
        for prestamo in prestamos:
            pr_fecha = prestamo._FechaPrestamo
            today_fecha = date.today()

            if pr_fecha.year == today_fecha.year and pr_fecha.month == today_fecha.month:
                pr_libro = prestamo._Libro

                found, ind, cant = False, 0, 1
                for ind_aux, tupla in enumerate(lista_libros):
                    if pr_libro == tupla[0]:
                        ind = ind_aux
                        cant = tupla[1] + 1
                        found = True
                        break

                new_tupla = (pr_libro, cant)
                
                if found:
                    for i in range(ind, -1, -1):
                        for_tupla = lista_libros[i]
                        if (new_tupla[1] <= for_tupla[1]) or i==0:
                            del lista_libros[ind]
                            lista_libros.insert(i, new_tupla)
                            break
                else:
                    lista_libros.append((pr_libro, 1))

        return lista_libros
    
    def get_usuarios_con_mas_prestamos(self) -> List[Tuple[Usuario, int]]:
        prestamos = self.get_prestamos()

        lista_usuarios = []

        for prestamo in prestamos:
            pr_user = prestamo._Usuario

            found, ind, cant = False, 0, 1
            for ind_aux, tupla in enumerate(lista_usuarios):
                if pr_user == tupla[0]:
                    ind = ind_aux
                    cant = tupla[1] + 1
                    found = True
                    break

            new_tupla = (pr_user, cant)
            
            if found:
                for i in range(ind, -1, -1):
                    for_tupla = lista_usuarios[i]
                    if (new_tupla[1] <= for_tupla[1]) or i==0:
                        del lista_usuarios[ind]
                        lista_usuarios.insert(i, new_tupla)
                        break
            else:
                lista_usuarios.append((pr_user, 1))
        
        return lista_usuarios


                
    # Obtener IDS Autoincrementales (El unico que no tiene ID autoincremental es el Libro)
    def get_autor_id(self) -> int:
        return self.DATABASE.obtener_id_ai('autores.json')
    def get_usuario_id(self) -> int:
        return self.DATABASE.obtener_id_ai('usuarios.json')
    def get_prestamo_id(self) -> int:
        return self.DATABASE.obtener_id_ai('prestamos.json')
    
    # Escrituras
    def add_libro(self, libro_param : Libro) -> tuple[bool, str]:
        isbn = libro_param._ISBN
        titulo = libro_param._Titulo
        genero = libro_param._Genero
        anio = libro_param._Anio
        autor_id = libro_param._Autor._ID
        cantidad = libro_param._Cantidad

        if isbn == None or titulo.replace(' ', '') == "" or genero.replace(' ', '') == "" or anio == None or autor_id == None or cantidad == None:
            return False, 'No puede haber ningún atributo vacío'
            
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
    
    def libro_modify_add_cantidad(self, libro_param : Libro, cantidad_aniadida : int):
        libro_param_isbn = libro_param._ISBN
        libros = self.get_libros()
        libros_json = []
        new_libro = None
        for libro in libros:
            if libro_param_isbn == libro._ISBN:
                libro._Cantidad += cantidad_aniadida
                new_libro = libro
            libros_json.append(libro.convert_to_json())
        self.DATABASE.save_file('libros.json', libros_json)
        return new_libro, 'Cantidad de Libros disponibles modificada correctamente'

    def prestamo_modify_devolver(self, prestamo_param : Prestamo, estaEnCondiciones = True):
        if estaEnCondiciones:
            self.libro_modify_add_cantidad(prestamo_param._Libro, 1) # Añadir uno a cantidad disponible
        
        # Agregar fecha de devolución
        prestamos = self.get_prestamos()
        prestamos_json = []
        new_prestamo = prestamo_param
        for prestamo in prestamos:
            if prestamo._ID == prestamo_param._ID:
                prestamo._FechaDevolucion = date.today()
                new_prestamo = prestamo
            prestamos_json.append(prestamo.convert_to_json())
        self.DATABASE.save_file('prestamos.json', prestamos_json)
        return new_prestamo, 'Prestamo devuelto correctamente'
        

    def add_autor(self, autor : Autor) -> tuple[bool, str]:
        id = autor._ID
        nombre = autor._Nombre
        apellido = autor._Apellido
        nacionalidad = autor._Nacionalidad
        if id == None or nombre.replace(' ', '') == '' or apellido.replace(' ', '') == '' or nacionalidad.replace(' ', '') == '':
            return False, 'No puede haber ningún atributo vacío'

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
    

    def add_usuario(self, usuario : Usuario) -> tuple[bool, str]:
        id = usuario._ID
        nombre = usuario._Nombre
        apellido = usuario._Apellido
        tipo = usuario._Tipo
        if id == None or nombre.replace(' ', '') == '' or apellido.replace(' ', '') == '' or tipo == None:
            return False, 'No puede haber ningún atributo vacío'

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


    def add_prestamo(self, prestamo : Prestamo) -> tuple[bool, str]:
        id = prestamo._ID
        id_usuario = prestamo._Usuario._ID
        isbn_libro = prestamo._Libro._ISBN
        fecha_prestamo = prestamo._FechaPrestamo
        fecha_devolucion = prestamo._FechaDevolucion

        if id == None or id_usuario == None or isbn_libro == None or not fecha_prestamo:
            return False, 'No puede haber ningún atributo vacío'

        prestamos = self.get_prestamos()
        prestamos_json = []
        for prestamo_aux in prestamos:
            prestamos_json.append(prestamo_aux.convert_to_json())
        prestamos_json.append(prestamo.convert_to_json())


        self.DATABASE.save_file('prestamos.json', prestamos_json)
        return True, "Préstamo registrado correctamente"
    