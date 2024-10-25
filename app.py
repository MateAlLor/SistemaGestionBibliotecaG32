from api import LocalApi
from flask import Flask, render_template, redirect, url_for, request
from utils.clases import Usuario, Autor, Libro
import threading
import webview

class FlaskApp:
    def __init__(self):
        # Construcción de la APP en FLASK
        template_folder = 'web_interface/templates' # Definir ruta donde van a ir las plantillas HTML
        static_folder = 'web_interface/static' # Definir ruta donde van a ir los elementos estáticos (como el CSS)
        self.APP = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
       
        # Construir API local (A partir de esta se obtienen/guardan los datos del archivo o DB)
        self.LocalApi = LocalApi()

        self.create_interface() # Crea las rutas de la interfaz
        self.create_post_routes() # Crea las rutas que van a llamarse desde los formularios para registrar

    # Rutas que solo sirven de interfaz
    def create_interface(self):
        # Ruta de Inicio
        @self.APP.route('/home')
        def home():
            return render_template('home.html')
        
        # Rutas de Autores
        @self.APP.route('/autores')
        def autores():
            return render_template('autores/menu.html')
        
        @self.APP.route('/autores/registrar')
        def autores_registrar():
            alert = request.args.get('alert')
            id = self.LocalApi.get_autor_id()
            return render_template('autores/registrar.html', id=id, alert=alert)
        
        
        @self.APP.route('/autores/listar')
        def autores_listar():
            autores = self.LocalApi.get_autores()
            return render_template('autores/listar.html', autores=autores)
        
        # Rutas de Usuarios
        @self.APP.route('/usuarios')
        def usuarios():
            return render_template('usuarios/menu.html')
        
        @self.APP.route('/usuarios/registrar')
        def usuarios_registrar():
            alert = request.args.get('alert')
            id = self.LocalApi.get_usuario_id()
            return render_template('usuarios/registrar.html', id=id, alert=alert)
        
        @self.APP.route('/usuarios/listar')
        def usuarios_listar():
            usuarios = self.LocalApi.get_usuarios()
            return render_template('usuarios/listar.html', usuarios=usuarios)
        
        # Rutas de Libros
        @self.APP.route('/libros')
        def libros():
            return render_template('libros/menu.html')
        
        @self.APP.route('/libros/registrar')
        def libros_registrar():
            alert = request.args.get('alert')
            
            return render_template('libros/registrar.html', alert=alert)
        
        @self.APP.route('/libros/listar')
        def libros_listar():
            libros = self.LocalApi.get_libros()
            return render_template('libros/listar.html', libros=libros)
        
    
    # Rutas que Crean, Actualizan o Eliminan elementos de la DB/Archivo
    def create_post_routes(self):
        @self.APP.route('/autores/registrar', methods=['POST'])
        def autores_registrar_post():
            # Tomar datos de formulario
            id = int(request.form['id'])
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            nacionalidad = request.form['nacionalidad']
            
            isSuccess, alert = self.LocalApi.add_autor(id, nombre, apellido, nacionalidad)

            return self.APP.redirect(url_for('autores_registrar', alert=alert))
        
        
        @self.APP.route('/usuarios/registrar', methods=['POST'])
        def usuarios_registrar_post():
            id = int(request.form['id'])
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            tipo = int(request.form['tipo'])


            isSuccess, alert = self.LocalApi.add_usuario(id, nombre, apellido, tipo)


            return self.APP.redirect(url_for('usuarios_registrar', alert=alert))

            
        
        @self.APP.route('/libros/registrar', methods=['POST'])
        def libros_registrar_post():
            isbn = int(request.form['isbn'])
            titulo = request.form['titulo']
            genero = request.form['genero']
            anio = int(request.form['anio'])
            autor_id = int(request.form['autor'])
            cantidad = int(request.form['cantidad'])
            
            isSuccess, alert = self.LocalApi.add_libro(isbn, titulo, genero, anio, autor_id, cantidad)

            return self.APP.redirect(url_for('libros_registrar', alert=alert))
                

    
    # Inicializar APP
    def run_app(self):
        def start_server():
            self.APP.run(host='0.0.0.0', port=80)

        # Se inicializa Flask en un hilo aparte (el hilo se cierra solo una vez se cierre el hilo principal, es decir la interfaz)
        flask_thread = threading.Thread(target=start_server)
        flask_thread.daemon = True
        flask_thread.start()
        
        # Se renderiza la interfaz en el hilo principal
        webview.create_window('Software de Gestión', 'http://localhost/home')
        webview.start()



if __name__ == '__main__':
    AppTPI = FlaskApp()
    AppTPI.run_app()