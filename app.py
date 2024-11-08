from api import LocalApi
# from flask import Flask, render_template, redirect, url_for, request
import dearpygui.dearpygui as dpg
from utils.clases import Usuario, Autor, Libro

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

            print(f'AUTOR: Nombre: {nombre}, Apell: {apellido}, Nac: {nacionalidad}')

            # Intenta cargar los elementos en el archivo
            isSuccess, alert = self.LocalApi.add_autor(id, nombre, apellido, nacionalidad)

            create_autores_registrar(alert=alert)# Esto sirve para refrescar la ventana, y que se muestren un mensaje de error si algo pasó
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

            isSuccess, alert = self.LocalApi.add_usuario(id, nombre, apellido, nac_int)
            create_usuarios_registrar(alert=alert)
            create_usuarios_listar(show=False)
            self.establecer_estilos_globales()
        
        def libros_form_submit(id):
            isbn = int(dpg.get_value("form.libro.isbn"))
            titulo = dpg.get_value("form.libro.titulo")
            genero = dpg.get_value("form.libro.genero")
            anio = int(dpg.get_value("form.libro.anio"))
            autor_id = int(dpg.get_value("form.libro.autorid"))
            cantidad = int(dpg.get_value("form.libro.cantidad"))

            isSuccess, alert = self.LocalApi.add_libro(isbn, titulo, genero, anio, autor_id, cantidad)
            create_libros_registrar(alert=alert)
            create_libros_listar(show=False)
            self.establecer_estilos_globales()


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
        
        # INTERFAZ DE AUTORES
        def create_autores_interfaz(show=True, alert=None):
            dpg.delete_item("autores")

            with dpg.window(label="Autores", tag="autores", show=show):
                if alert:
                    dpg.add_text(alert, tag='autores.alert')
                dpg.add_button(label="Registrar", callback=lambda:cambiar_ventana('autores', 'autores.registrar'))
                dpg.add_button(label="Listar", callback=lambda:cambiar_ventana('autores', 'autores.listar'))
                dpg.add_button(label="Volver al Inicio", callback=lambda:cambiar_ventana('autores', 'inicio'))

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
        
        # INTERFAZ DE USUARIOS
        def create_usuarios(show=True, alert=None):
            dpg.delete_item("usuarios")

            with dpg.window(label="Usuarios", tag="usuarios", show=show):
                if alert:
                    dpg.add_text(alert, tag='usuarios.alert')
                dpg.add_button(label="Registrar", callback=lambda:cambiar_ventana('usuarios', 'usuarios.registrar'))
                dpg.add_button(label="Listar", callback=lambda:cambiar_ventana('usuarios', 'usuarios.listar'))
                dpg.add_button(label="Volver al Inicio", callback=lambda:cambiar_ventana('usuarios', 'inicio'))
        

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
        
        # INTERFAZ DE LIBROS
        def create_libros(show=True, alert=None):
            dpg.delete_item("libros")

            with dpg.window(label="Libros", tag="libros", show=show):
                if alert:
                    dpg.add_text(alert, tag='libros.alert')
                dpg.add_button(label="Registrar", callback=lambda:cambiar_ventana('libros', 'libros.registrar'))
                dpg.add_button(label="Listar", callback=lambda:cambiar_ventana('libros', 'libros.listar'))
                dpg.add_button(label="Volver al Inicio", callback=lambda:cambiar_ventana('libros', 'inicio'))

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

        def create_libros_listar(show=True, alert=None):
            dpg.delete_item("libros.listar")

            with dpg.window(label="Libros", tag="libros.listar", show=show):
                if alert:
                    dpg.add_text(alert, tag='libros.listar.alert')
                libros = self.LocalApi.get_libros() # Obtener listado de Libros
                with dpg.child_window(no_scrollbar=False):
                    for libro in libros:
                        dpg.add_text(str(libro))
                dpg.add_button(label="Volver", callback=lambda:cambiar_ventana('libros.listar', 'libros'))
        
        # Crear todos los elementos
        create_inicio()
        create_autores_interfaz(show=False)
        create_autores_registrar(show=False)
        create_autores_listar(show=False)
        create_usuarios(show=False)
        create_usuarios_registrar(show=False)
        create_usuarios_listar(show=False)
        create_libros(show=False)
        create_libros_registrar(show=False)
        create_libros_listar(show=False)
        

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
        dpg.create_viewport(title='Gestión de Biblioteca', width=400, height=300)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()



if __name__ == '__main__':
    AppTPI = GestionApp()
    AppTPI.run_app()