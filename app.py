from api import LocalApi
# from flask import Flask, render_template, redirect, url_for, request
import dearpygui.dearpygui as dpg
from datetime import date

from clases.autor import Autor
from clases.libro import Libro
from clases.prestamo import Prestamo
from clases.usuario import Usuario

import utils.reportes as REPORTES

class GestionApp:
    def __init__(self):
        # Construcción de la APP en DearPygui
        dpg.create_context()
       
        # Construir API local (A partir de esta se obtienen/guardan los datos del archivo o DB)
        self.LocalApi = LocalApi()

        self.create_interface() # Crea las rutas de la interfaz

    # Rutas que solo sirven de interfaz
    def create_interface(self):
        def cambiar_ventana(origen, destino): # Esta función sirve para esconder una ventana y mostrar otra
            dpg.hide_item(origen)
            dpg.show_item(destino)
        
        # Submit de los Forms
        def autores_form_submit(id):
            # Tomar datos del formulario
            nombre = dpg.get_value("form.autor.nombre")
            apellido = dpg.get_value("form.autor.apellido")
            nacionalidad = dpg.get_value("form.autor.nacionalidad")

            # Intenta cargar los elementos en el archivo
            newAutor = Autor(id, nombre, apellido, nacionalidad)
            isSuccess, alert = self.LocalApi.add_autor(newAutor)
            # isSuccess, alert = self.LocalApi.add_autor(id, nombre, apellido, nacionalidad)
            
            create_autores_registrar(alert=alert, show=False)
            ir_a_interfaz_mensaje(titulo="Autor", origen="autores.registrar", mensaje=alert)
            # Esto sirve para refrescar la ventana, y que se muestren un mensaje de error si algo pasó
            create_autores_listar(show=False) # Hay que reconstruir la ventana del listado para que tenga los datos actualizados. Pasandole show=False para que no se muestre en el momento
            self.establecer_estilos_globales() # Hay que llamar a esta función después de usar un create, así se actualizan los estilos
            # Todo esto aplica para todos los form de registro

        def usuarios_form_submit(id):
            nombre = dpg.get_value("form.usuario.nombre")
            apellido = dpg.get_value("form.usuario.apellido")
            tipo = dpg.get_value("form.usuario.tipo")

            nac_int = 1
            if tipo == "Profesor":
                nac_int = 2
            
            newUser = Usuario(id, nombre, apellido, nac_int)

            isSuccess, alert = self.LocalApi.add_usuario(newUser)
            create_usuarios_registrar(alert=alert, show=False)
            ir_a_interfaz_mensaje(titulo="Usuario", origen="usuarios.registrar", mensaje=alert)
            create_usuarios_listar(show=False)
            self.establecer_estilos_globales()
        
        def libros_form_submit(id):
            isbn = int(dpg.get_value("form.libro.isbn"))
            titulo = dpg.get_value("form.libro.titulo")
            genero = dpg.get_value("form.libro.genero")
            anio = int(dpg.get_value("form.libro.anio"))
            autor_id = int(dpg.get_value("form.libro.autorid"))
            cantidad = int(dpg.get_value("form.libro.cantidad"))

            libro_autor = self.LocalApi.get_autor_byid(autor_id)

            new_libro = Libro(isbn, titulo, genero, anio, libro_autor, cantidad)

            isSuccess, alert = self.LocalApi.add_libro(new_libro)
            create_libros_registrar(alert=alert, show=False)
            ir_a_interfaz_mensaje(titulo="Libro", origen="libros.registrar", mensaje=alert)
            create_libros_listar(show=False)
            self.establecer_estilos_globales()
        
        def prestamo_form_submit(id, libro, usuario, origen):
            fecha_actual = date.today()
            newPrestamo = Prestamo(id, usuario, libro, fecha_actual, None)
            isSuccess, alert = self.LocalApi.add_prestamo(newPrestamo)
            new_libro = libro
            if isSuccess:
                new_libro, alerta = self.LocalApi.libro_modify_add_cantidad(libro, -1)
            create_libro_detalles(libro_aux=new_libro, origen='libros.listar')
            ir_a_interfaz_mensaje(titulo='Préstamo', origen='prestamo.register', destino=origen, mensaje=alert)
            # create_prestamos_listar(show=False)
            self.establecer_estilos_globales()
        
        def prestamo_devolver(prestamo, origen, estaEnCondiciones=True):
            new_prestamo, alert = self.LocalApi.prestamo_modify_devolver(prestamo, estaEnCondiciones)
            create_prestamo_detalles(prestamo=new_prestamo, origen=origen)
            self.establecer_estilos_globales()

        
        # Otras
        # def ir_a_libro(origen, libro):
        def ir_a_libro(origen, libro):
            create_libro_detalles(libro_aux=libro, origen="libros.listar")
            cambiar_ventana(origen, "libro.detalles")
            self.establecer_estilos_globales()
        
        def ir_a_prestamo(origen, prestamo):
            create_prestamo_detalles(prestamo=prestamo, origen=origen)
            cambiar_ventana(origen, "prestamo.detalles")
            self.establecer_estilos_globales()
        
        def ir_a_prestamo_registrar(origen, libro):
            create_prestamo_register(libro=libro, origen=origen)
            cambiar_ventana(origen, "prestamo.register")
            self.establecer_estilos_globales()
        
        def ir_a_interfaz_mensaje(titulo=None, origen=None, destino=None, mensaje=None):
            dest = destino
            if not destino:
                dest = origen
            create_mensaje_interfaz(titulo=titulo, destino=dest, mensaje=mensaje)
            cambiar_ventana(origen, "interfaz.mensaje")
            self.establecer_estilos_globales()
        
        def ir_a_reportes_prestvencidos():
            create_reportes_prestamosvencidos(show=False)
            cambiar_ventana('reportes', 'reportes.prestamos.vencidos')
            self.establecer_estilos_globales()
        
        def ir_a_reportes_librosmasprestados():
            create_reportes_librosmasprestados(show=False)
            cambiar_ventana('reportes', 'reportes.librosmasprestados')
            self.establecer_estilos_globales()
        
        def ir_a_reportes_usuarios_con_mas_prestamos():
            create_reportes_usuarios_con_mas_prestamos(show=False)
            cambiar_ventana('reportes', 'reportes.usuariosconmasprestamos')
            self.establecer_estilos_globales()

        # INTERFAZ DE MENSAJE
        def create_mensaje_interfaz(show=True, titulo=None, destino=None, mensaje=None):
            dpg.delete_item("interfaz.mensaje")

            with dpg.window(label=titulo, tag="interfaz.mensaje", show=show):
                dpg.add_text(mensaje, tag='interfaz.mensaje.alert')

                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('interfaz.mensaje', destino))

        # Las funciones que crean las interfaces tienen por parámetro: show (si se muestra o no inicialmente : bool), alert (Un mensaje extra si hace falta : str)
        # Ruta de Inicio
        def create_inicio(show=True, alert=None):
            dpg.delete_item("inicio")

            with dpg.window(label="Inicio", tag="inicio", show=show):
                if alert: # Si hay una alerta muestra el mensaje en pantalla
                    dpg.add_text(alert, tag='inicio.alert')
                dpg.add_button(label="Autores", callback=lambda:cambiar_ventana('inicio', 'autores'))
                dpg.add_button(label="Usuarios", callback=lambda:cambiar_ventana('inicio', 'usuarios'))
                dpg.add_button(label="Libros", callback=lambda:cambiar_ventana('inicio', 'libros'))
                dpg.add_button(label="Reportes", callback=lambda:cambiar_ventana('inicio', 'reportes'))
        create_inicio()
        
        # INTERFAZ DE AUTORES
        def create_autores_interfaz(show=True, alert=None):
            dpg.delete_item("autores")

            with dpg.window(label="Autores", tag="autores", show=show):
                if alert:
                    dpg.add_text(alert, tag='autores.alert')
                dpg.add_button(label="Registrar", callback=lambda:cambiar_ventana('autores', 'autores.registrar'))
                dpg.add_button(label="Listar", callback=lambda:cambiar_ventana('autores', 'autores.listar'))
                dpg.add_button(label="Volver al Inicio", callback=lambda:cambiar_ventana('autores', 'inicio'))
        
        create_autores_interfaz(show=False)

        # Registrar Autor
        def create_autores_registrar(show=True, alert=None):
            dpg.delete_item("autores.registrar") # Si existe eliminarlo

            with dpg.window(label="Registrar Autor", tag="autores.registrar", show=show):
                if alert:
                    dpg.add_text(alert, tag='autores.registrar.alert')
                id = self.LocalApi.get_autor_id() # Para precargar el ID autoincremental
                dpg.add_text(f"ID del Autor {id}", tag='form.autor.id')
                dpg.add_text("Ingrese los datos del Autor a continuación:")
                dpg.add_input_text(label="Nombre", tag="form.autor.nombre", hint="Escribe el nombre del autor")
                dpg.add_input_text(label="Apellido", tag="form.autor.apellido", hint="Escribe el apellido del autor")
                dpg.add_input_text(label="Nacionalidad", tag="form.autor.nacionalidad", hint="Escribe la nacionalidad del autor")
                dpg.add_button(label="Registrar", callback=lambda:autores_form_submit(id))
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('autores.registrar', 'autores'))
        create_autores_registrar(show=False, alert=None)
        
        # Listar Autores
        def create_autores_listar(show=True, alert=None):
            dpg.delete_item("autores.listar")
            
            with dpg.window(label="Listar Autores", tag="autores.listar", show=show):
                if alert:
                    dpg.add_text(alert, tag='autores.listar.alert')
                autores = self.LocalApi.get_autores() # Obtener autores
                with dpg.child_window(no_scrollbar=False):
                    for autor in autores:
                        dpg.add_text(str(autor))
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('autores.listar', 'autores'))
        create_autores_listar(show=False, alert=None)
        
        # INTERFAZ DE USUARIOS
        def create_usuarios(show=True, alert=None):
            dpg.delete_item("usuarios")

            with dpg.window(label="Usuarios", tag="usuarios", show=show):
                if alert:
                    dpg.add_text(alert, tag='usuarios.alert')
                dpg.add_button(label="Registrar", callback=lambda:cambiar_ventana('usuarios', 'usuarios.registrar'))
                dpg.add_button(label="Listar", callback=lambda:cambiar_ventana('usuarios', 'usuarios.listar'))
                dpg.add_button(label="Volver al Inicio", callback=lambda:cambiar_ventana('usuarios', 'inicio'))
        create_usuarios(show=False, alert=None)
        

        def create_usuarios_registrar(show=True, alert=None):
            dpg.delete_item("usuarios.registrar")

            with dpg.window(label="Registrar Usuario", tag="usuarios.registrar", show=show):
                if alert:
                    dpg.add_text(alert, tag='usuarios.registrar.alert')
                id = self.LocalApi.get_usuario_id() # Para precargar el ID autoincremental
                dpg.add_text(f"ID del Usuario {id}", tag='form.usuario.id')
                dpg.add_text("Ingrese los datos del Usuario a continuación")
                dpg.add_input_text(label="Nombre", tag="form.usuario.nombre", hint="Escribe el nombre del usuario")
                dpg.add_input_text(label="Apellido", tag="form.usuario.apellido", hint="Escribe el apellido del usuario")
                dpg.add_combo(label="Tipo", tag="form.usuario.tipo", items=["Estudiante", "Profesor"])
                dpg.add_button(label="Registrar", callback=lambda:usuarios_form_submit(id))
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('usuarios.registrar', 'usuarios'))
        create_usuarios_registrar(show=False, alert=None)

        def create_usuarios_listar(show=True, alert=None):
            dpg.delete_item("usuarios.listar")

            with dpg.window(label="Usuarios", tag="usuarios.listar", show=show):
                if alert:
                    dpg.add_text(alert, tag='usuarios.listar.alert')
                usuarios = self.LocalApi.get_usuarios()
                with dpg.child_window(no_scrollbar=False):
                    for user in usuarios:
                        dpg.add_text(str(user))
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('usuarios.listar', 'usuarios'))
        create_usuarios_listar(show=False, alert=None)
        
        
        # INTERFAZ DE LIBROS
        def create_libros(show=True, alert=None):
            dpg.delete_item("libros")

            with dpg.window(label="Libros", tag="libros", show=show):
                if alert:
                    dpg.add_text(alert, tag='libros.alert')
                dpg.add_button(label="Registrar", callback=lambda:cambiar_ventana('libros', 'libros.registrar'))
                dpg.add_button(label="Listar", callback=lambda:cambiar_ventana('libros', 'libros.listar'))
                dpg.add_button(label="Volver al Inicio", callback=lambda:cambiar_ventana('libros', 'inicio'))
        create_libros(show=False)
        

        def create_libros_registrar(show=True, alert=None):
            dpg.delete_item("libros.registrar")

            with dpg.window(label="Libros", tag="libros.registrar", show=show):
                if alert:
                    dpg.add_text(alert, tag='libros.registrar.alert')
                dpg.add_text("Ingrese los datos del Libro a continuación")
                dpg.add_input_int(label="ISBN", tag="form.libro.isbn", min_value=0)
                dpg.add_input_text(label="Título", tag="form.libro.titulo", hint="Escribe el título del libro")
                dpg.add_input_text(label="Genero", tag="form.libro.genero", hint="Escribe el género del libro")
                dpg.add_input_int(label="Año", tag="form.libro.anio", min_value=0)
                dpg.add_input_int(label="ID del Autor", tag="form.libro.autorid", min_value=0)
                dpg.add_input_int(label="Cantidad", tag="form.libro.cantidad", min_value=0)

                dpg.add_button(label="Registrar", callback=lambda:libros_form_submit(id))
                
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('libros.registrar', 'libros'))
        create_libros_registrar(show=False, alert=None)

        def create_libros_listar(show=True, alert=None):
            dpg.delete_item("libros.listar")

            with dpg.window(label="Libros", tag="libros.listar", show=show):
                if alert:
                    dpg.add_text(alert, tag='libros.listar.alert')
                libros = self.LocalApi.get_libros() # Obtener listado de Libros
                with dpg.child_window(no_scrollbar=False):
                    for libro in libros:
                        libro_label = f'ISBN: {libro._ISBN}, Título: {libro._Titulo}, Autor: {libro._Autor._Nombre} {libro._Autor._Apellido}' 
                        dpg.add_button(label=libro_label, callback=lambda s, a, lib: ir_a_libro('libros.listar', lib), user_data=libro)
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('libros.listar', 'libros'))
        create_libros_listar(show=False)
        
        def create_libro_detalles(show=True, alert=None, libro_aux=None, origen='libros'):
            dpg.delete_item("libro.detalles")

            libro = self.LocalApi.get_libro_byisbn(libro_aux._ISBN)

            with dpg.window(label="Detalles del Libro", tag="libro.detalles", show=show):
                if alert:
                    dpg.add_text(alert, tag='libro.detalles.alert')

                dpg.add_text(str(libro))
                dpg.add_text("Prestamos de este Libro:")


                prestamos_libro = self.LocalApi.get_prestamos_byisbn(libro._ISBN)

                with dpg.child_window(no_scrollbar=False):
                    if libro._Cantidad > 0:
                        dpg.add_button(label="NUEVO PRÉSTAMO", callback=lambda:ir_a_prestamo_registrar('libro.detalles', libro))
                    else:
                        dpg.add_button(label="NUEVO PRÉSTAMO\n(SIN DISPONIBILIDAD)", enabled=False)
                    for prestamo_libro in prestamos_libro:
                        botontext = f"Usuario: [{prestamo_libro._Usuario._ID}] - {prestamo_libro._Usuario._Nombre} {prestamo_libro._Usuario._Apellido}\n"
                        botontext += f"Fecha Préstamo: {prestamo_libro._FechaPrestamo}\n"
                        if prestamo_libro._FechaDevolucion:
                            botontext += f"Fecha Devolución: {prestamo_libro._FechaDevolucion}\n"
                        else:
                            botontext += f"NO DEVUELTO"
                        # dpg.add_button(label=botontext, callback=lambda:ir_a_prestamo(prestamo_libro))
                        dpg.add_button(label=botontext, callback=lambda s, a, par: ir_a_prestamo(prestamo=par['prestamo'], origen=par['origen']), user_data={"prestamo":prestamo_libro, "origen":origen})
                    

                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('libro.detalles', origen))

        def create_prestamo_detalles(show=True, alert=None, prestamo=None, origen='inicio'):
            dpg.delete_item("prestamo.detalles")

            with dpg.window(label="Detalles del Prestamo", tag="prestamo.detalles", show=show):
                if alert:
                    dpg.add_text(alert, tag='prestamo.detalles.alert')

                dpg.add_text(str(prestamo))
                
                if not prestamo._FechaDevolucion:
                    dpg.add_button(label="Marcar como devuelto", callback=lambda s, a, par: prestamo_devolver(par['prestamo'], par['origen'], estaEnCondiciones=par['condiciones']), user_data={"prestamo":prestamo, "origen":origen, "condiciones":True})
                    dpg.add_button(label="Marcar como devuelto en malas condiciones (No se contará como disponible)", callback=lambda s, a, par: prestamo_devolver(par['prestamo'], par['origen'], estaEnCondiciones=par['condiciones']), user_data={"prestamo":prestamo, "origen":origen, "condiciones":False})
                    

                # dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('prestamo.detalles', origen))
                dpg.add_button(label="Volver", callback=lambda:ir_a_libro('prestamo.detalles', prestamo._Libro))
        
        def create_prestamo_register(show=True, alert=None, libro=None, origen='prestamo.buscar'):
            dpg.delete_item("prestamo.register")

            with dpg.window(label="Registrar Préstamo", tag="prestamo.register", show=show):
                if alert:
                    dpg.add_text(alert, tag='libro.detalles.alert')
                
                id = self.LocalApi.get_prestamo_id()

                dpg.add_text(f"ID del Préstamo a registrar: {id}")
                dpg.add_text(f"Libro a Prestar:\n{libro}")
                dpg.add_text("Elige el Usuario al cual se le prestará el Libro:")

                usuarios_prest = self.LocalApi.get_usuarios()

                with dpg.child_window(no_scrollbar=False):
                    for usuario_prest in usuarios_prest:
                        dpg.add_button(label=str(usuario_prest), callback=lambda s, a, par: prestamo_form_submit(par['id'], par['libro'], par['usuario'], par['origen']), user_data={"id":id, "libro":libro, "usuario":usuario_prest, "origen":origen})
                    

                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('prestamo.register', origen))
        
        # REPORTES
        def create_reportes(show=True, alert=None):
            dpg.delete_item("reportes")

            with dpg.window(label="Reportes", tag="reportes", show=show):
                if alert:
                    dpg.add_text(alert, tag='reportes.alert')
                dpg.add_button(label="Préstamos Vencidos", callback=lambda:ir_a_reportes_prestvencidos())
                dpg.add_button(label="Libros más Prestados", callback=lambda:ir_a_reportes_librosmasprestados())
                dpg.add_button(label="Usuarios con más Préstamos pedidos", callback=lambda:ir_a_reportes_usuarios_con_mas_prestamos())

                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('reportes', 'inicio'))

        create_reportes(show=False, alert=None)

        def create_reportes_prestamosvencidos(show=True, alert=None):
            def generar_reporte(prestamos):
                REPORTES.generar_reporte_prestamos_vencidos(prestamos)
                ir_a_interfaz_mensaje(titulo="Reporte", origen="reportes.prestamos.vencidos", mensaje="Reporte Generado Correctamente")

            dpg.delete_item("reportes.prestamos.vencidos")

            with dpg.window(label="Préstamos", tag="reportes.prestamos.vencidos", show=show):
                if alert:
                    dpg.add_text(alert, tag='reportes.prestamos.vencidos.alert')
                prestamos = self.LocalApi.get_prestamos_vencidos() # Obtener listado de Libros
                with dpg.child_window(no_scrollbar=False):
                    for prestamo in prestamos:
                        dpg.add_text(str(prestamo))

                dpg.add_button(label="Generar PDF con Tabla", callback=lambda:generar_reporte(prestamos))
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('reportes.prestamos.vencidos', 'reportes'))
        create_reportes_prestamosvencidos(show=False)

        def create_reportes_librosmasprestados(show=True):
            def generar_reporte(tuplas, tipo_reporte):
                REPORTES.generar_reporte_librosmasprestados(tuplas, tipo_reporte)
                ir_a_interfaz_mensaje(titulo="Reporte", origen="reportes.librosmasprestados", mensaje="Reporte Generado Correctamente")

            dpg.delete_item("reportes.librosmasprestados")

            with dpg.window(label="Libros más prestados", tag="reportes.librosmasprestados", show=show):
                tuplas = self.LocalApi.get_libros_mas_prestados() # Obtener listado de Libros
                with dpg.child_window(no_scrollbar=False):
                    for tup in tuplas:
                        libro = tup[0]
                        cant = tup[1]

                        texto = f"Libro: {libro._Titulo}\n"
                        texto += f"\tISBN: {libro._ISBN}\n"
                        texto += f"\tAutor: {libro._Autor._Nombre} {libro._Autor._Apellido}\n"
                        texto += f"\tCantidad de Préstamos: {cant}"

                        dpg.add_text(texto)
                dpg.add_button(label="Generar PDF con Tabla", callback=lambda:generar_reporte(tuplas, 0))
                dpg.add_button(label="Generar PDF con Gráfico", callback=lambda:generar_reporte(tuplas, 1))
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('reportes.librosmasprestados', 'reportes'))
        
        def create_reportes_usuarios_con_mas_prestamos(show=True):
            def generar_reporte(tuplas, tipo_reporte):
                REPORTES.generar_reporte_usuarios_con_mas_prestamos(tuplas, tipo_reporte)
                ir_a_interfaz_mensaje(titulo="Reporte", origen="reportes.usuariosconmasprestamos", mensaje="Reporte Generado Correctamente")
            
            dpg.delete_item("reportes.usuariosconmasprestamos")

            with dpg.window(label="Libros más prestados", tag="reportes.usuariosconmasprestamos", show=show):
                tuplas = self.LocalApi.get_usuarios_con_mas_prestamos() # Obtener listado de Libros
                with dpg.child_window(no_scrollbar=False):
                    for tup in tuplas:
                        usuario = tup[0]
                        cant = tup[1]

                        texto = f"Usuario: {usuario._Nombre} {usuario._Apellido}\n"
                        texto += f"\tID: {usuario._ID}\n"
                        if usuario._Tipo == 1:
                            texto += f"\tTipo: Estudiante\n"
                        else:
                            texto += f"\tTipo: Profesor\n"
                
                        texto += f"\tCantidad de Préstamos: {cant}"
                        

                        dpg.add_text(texto)
                dpg.add_button(label="Generar PDF con Tabla", callback=lambda:generar_reporte(tuplas, 0))
                dpg.add_button(label="Generar PDF con Gráfico", callback=lambda:generar_reporte(tuplas, 1))
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('reportes.usuariosconmasprestamos', 'reportes'))

        
    def establecer_estilos_globales(self): # Asigna el estilo de los objetos, un "CSS" acá
            ancho = dpg.get_viewport_width()
            alto = dpg.get_viewport_height()
            button_ancho, button_alto = int(ancho * 0.98), int(alto * 0.1)
            scroll_ancho, scroll_alto = int(ancho * 0.98), int(alto * 0.5)
            field_ancho = int(ancho * 0.7)

            for item in dpg.get_all_items():
                item_type = dpg.get_item_type(item)

                if item_type == "mvAppItemType::mvWindowAppItem":
                    dpg.set_item_width(item, ancho)
                    dpg.set_item_height(item, alto) 

                if item_type == "mvAppItemType::mvButton":
                    dpg.set_item_width(item, button_ancho)
                    dpg.set_item_height(item, button_alto) 

                elif item_type == "mvAppItemType::mvChildWindow":
                    dpg.set_item_width(item, scroll_ancho)
                    dpg.set_item_height(item, scroll_alto)
                elif item_type == "mvAppItemType::mvInputText" or item_type == "mvAppItemType::mvInputInt":
                    dpg.set_item_width(item, field_ancho) # Los Input Text e Int no tienen para cambiar el alto
                else:
                    # print(dpg.get_item_type(item))
                    pass
    
    # Inicializar APP
    def run_app(self):
        dpg.set_viewport_resize_callback(lambda sender, app_data: self.establecer_estilos_globales())
        dpg.create_viewport(title='Gestión de Biblioteca', width=1280, height=800)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

if __name__ == '__main__':

    AppTPI = GestionApp()
    AppTPI.run_app()